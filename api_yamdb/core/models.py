from django.db import models


class CreatedModel(models.Model):
    """Абстрактная модель. Добавляет дату и время создания."""
    pub_date = models.DateTimeField('Дата и время публикации',
                                    auto_now_add=True
                                    )

    class Meta:
        abstract = True
