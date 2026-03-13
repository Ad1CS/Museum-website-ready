from django.db import models
from django.urls import reverse


class HistoricalPeriod(models.TextChoices):
    PRE_SOVIET   = 'pre-soviet',   'Досоветский период (1900–1930)'
    CONSTRUCTION = 'construction', 'Проектирование и строительство (1930–1933)'
    PREWAR       = 'prewar',       'Довоенный период (1933–1941)'
    BLOCKADE     = 'blockade',     'Блокадный период (1941–1944)'
    GOLDEN       = 'golden',       'Период расцвета (1944–1992)'
    POST_SOVIET  = 'post-soviet',  'Постсоветский период (1992–2007)'
    MODERN       = 'modern',       'Современность (2007–н/д)'


class Album(models.Model):
    title       = models.CharField('Название', max_length=300)
    period      = models.CharField('Период', max_length=30, choices=HistoricalPeriod.choices)
    description = models.TextField('Описание', blank=True)
    cover       = models.ImageField('Обложка', upload_to='gallery/covers/', blank=True, null=True)
    order       = models.PositiveIntegerField('Порядок', default=0)
    published   = models.BooleanField('Опубликован', default=True)
    created_at  = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Альбом'
        verbose_name_plural = 'Альбомы'
        ordering = ['period', 'order', 'title']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('gallery:album_detail', args=[self.pk])


class Photo(models.Model):
    album   = models.ForeignKey(Album, on_delete=models.CASCADE,
                                related_name='photos', verbose_name='Альбом')
    image   = models.ImageField('Изображение', upload_to='gallery/photos/')
    caption = models.CharField('Подпись', max_length=500, blank=True)
    date_text = models.CharField('Дата (текст)', max_length=100, blank=True)

    # ── Cross-links ──────────────────────────────────────────────────────────
    # Link to a physical fond item (if the photo has a physical copy in the fund)
    fond_item = models.ForeignKey(
        'fond.FondItem', on_delete=models.SET_NULL, null=True, blank=True,
        related_name='gallery_photos', verbose_name='Предмет фонда (оригинал)'
    )
    # People depicted in or associated with this photo
    linked_staff = models.ManyToManyField(
        'staff.StaffMember', blank=True,
        related_name='photos', verbose_name='Изображённые сотрудники'
    )

    order      = models.PositiveIntegerField('Порядок', default=0)
    published  = models.BooleanField('Опубликовано', default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Фотография'
        verbose_name_plural = 'Фотографии'
        ordering = ['album', 'order']

    def __str__(self):
        return self.caption or f'Фото #{self.pk}'
