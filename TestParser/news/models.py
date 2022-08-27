from django.db import models


class Tag(models.Model):
    name = models.CharField('Название', max_length=50)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'
        constraints = (
            models.UniqueConstraint(
                fields=['name'], name='unique tag',
            ),)

    def __str__(self):
        return self.name


class News(models.Model):
    title = models.CharField('Заголовок', max_length=200)
    resource = models.URLField('Ресурс', max_length=200)
    body = models.TextField('Текст новости')
    created_at = models.DateTimeField()
    tags = models.ManyToManyField(
        Tag, blank=True, related_name='news', verbose_name='Тег'
    )

    class Meta:
        ordering = ('-created_at',)
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'
        constraints = (
            models.UniqueConstraint(
                fields=['title'],
                name='unique news'
            ),)

    def __str__(self):
        return self.title


