from django.db import models
from django.urls import reverse


class Building(models.Model):
    slug = models.SlugField('Slug', unique=True)
    name = models.CharField('Название', max_length=300)
    built_years = models.CharField('Год постройки', max_length=100, blank=True)
    description = models.TextField('Описание')
    # Map position (percentage from top-left of the map image)
    map_left = models.FloatField('Позиция слева (%)', default=10)
    map_top = models.FloatField('Позиция сверху (%)', default=10)
    map_width = models.FloatField('Ширина (%)', default=15)
    map_height = models.FloatField('Высота (%)', default=15)

    photos = models.ManyToManyField('gallery.Photo', blank=True,
                                     related_name='buildings', verbose_name='Фотографии')
    order = models.PositiveIntegerField('Порядок', default=0)
    published = models.BooleanField('Опубликовано', default=True)

    class Meta:
        verbose_name = 'Здание'
        verbose_name_plural = 'Здания на карте'
        ordering = ['order', 'name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('mapblock:building', args=[self.slug])
