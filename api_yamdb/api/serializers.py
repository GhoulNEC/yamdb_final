from django.core.validators import MaxValueValidator, MinValueValidator
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from reviews.models import Category, Comment, Genre, Review, Title
from reviews.validators import validate_year
from users.models import User


class SignUpSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=254, required=True)
    username = serializers.CharField(max_length=150, required=True)

    def validate_username(self, data):
        if data.lower() == 'me':
            raise serializers.ValidationError('Нельзя использовать логин me')
        return data

    class Meta:
        fields = ('username', 'email')


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150, required=True)
    confirmation_code = serializers.CharField(required=True)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role'
        )


class MeSerializer(serializers.ModelSerializer):
    role = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role'
        )


class GenresSerializer(serializers.ModelSerializer):
    """Жанры, описание."""

    class Meta:
        model = Genre
        fields = ('name', 'slug')


class CategoriesSerializer(serializers.ModelSerializer):
    """Категории, описание."""

    class Meta:
        model = Category
        fields = ('name', 'slug')


class TitlesSerializer(serializers.ModelSerializer):
    """Основной метод записи информации."""

    category = serializers.SlugRelatedField(
        slug_field='slug', many=False, queryset=Category.objects.all()
    )
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        many=True,
        required=False,
        queryset=Genre.objects.all()
    )

    class Meta:
        fields = '__all__'
        model = Title

    def validate_year(self, value):
        validate_year(value)
        return value


class TitlesViewSerializer(serializers.ModelSerializer):
    """Основной метод получения информации."""

    category = CategoriesSerializer(many=False, required=True)
    genre = GenresSerializer(many=True, required=False)
    rating = serializers.IntegerField()

    class Meta:
        fields = (
            'id',
            'name',
            'year',
            'rating',
            'description',
            'genre',
            'category'
        )
        model = Title
        read_only_fields = (
            'id',
            'name',
            'year',
            'rating',
            'description',
            'genre',
            'category'
        )


class ReviewsSerializer(serializers.ModelSerializer):
    """Ревью для произведений"""
    author = serializers.SlugRelatedField(
        slug_field='username',
        default=serializers.CurrentUserDefault(),
        read_only=True
    )
    score = serializers.IntegerField(validators=[
        MaxValueValidator(10, message='Оценка не может быть выше "10"'),
        MinValueValidator(1, message='Оценка не может быть ниже "1"')
    ])

    class Meta:
        fields = '__all__'
        model = Review
        read_only_fields = ['title']

    def validate(self, data):
        if self.context['request'].method == 'POST':
            title_id = (
                self.context['request'].parser_context['kwargs']['title_id']
            )
            user = self.context['request'].user
            if user.reviews.filter(title_id=title_id).exists():
                raise serializers.ValidationError(
                    'Нельзя оставить отзыв на одно произведение дважды'
                )
        return data


class CommentsSerializer(serializers.ModelSerializer):
    """Комментарии на отзывы"""

    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date')
        model = Comment
