from api.views import (CategoriesViewSet, CommentViewSet, GenresViewSet,
                       ReviewViewSet, TitlesViewSet, UserViewSet, signup_post,
                       token_post)
from django.urls import include, path
from rest_framework.routers import DefaultRouter

app_name = 'api'

router = DefaultRouter()
router.register('users', UserViewSet, basename='users')
router.register('titles', TitlesViewSet, basename='titles')
router.register('genres', GenresViewSet, basename='genres')
router.register('categories', CategoriesViewSet, basename='categories')
router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews'
)

router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments',
)
auth_urlpatterns = [
    path('token/', token_post, name='token'),
    path('signup/', signup_post, name='signup'),
]
urlpatterns = [
    path('v1/auth/', include(auth_urlpatterns)),
    path('v1/', include(router.urls)),
]
