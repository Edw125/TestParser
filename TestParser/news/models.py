from django.db import models


class Tag(models.Model):
    name = models.CharField('Name', max_length=50)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'
        constraints = (
            models.UniqueConstraint(
                fields=['name'], name='unique tag',
            ),)

    def __str__(self):
        return self.name


class News(models.Model):
    title = models.CharField('Title', max_length=200)
    resource = models.URLField('URL', max_length=200)
    body = models.TextField('News Text')
    created_at = models.DateTimeField()
    tags = models.ManyToManyField(
        Tag, blank=True, related_name='news', verbose_name='Tag'
    )

    class Meta:
        ordering = ('-created_at',)
        verbose_name = 'News'
        verbose_name_plural = 'News'
        constraints = (
            models.UniqueConstraint(
                fields=['title'],
                name='unique news'
            ),)

    def __str__(self):
        return self.title


