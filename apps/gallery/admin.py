from django.contrib import admin
from django.utils.html import format_html
from .models import Album, Photo


class PhotoInline(admin.TabularInline):
    model  = Photo
    extra  = 0
    fields = ['thumb_preview', 'image', 'caption', 'date_text', 'order', 'published']
    readonly_fields = ['thumb_preview']
    show_change_link = True

    def thumb_preview(self, obj):
        if obj.pk and obj.image:
            return format_html(
                '<img src="{}" style="height:44px;width:60px;object-fit:cover;" />', obj.image.url)
        return '—'
    thumb_preview.short_description = ''


@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    list_display  = ['cover_thumb', 'title', 'period', 'photo_count', 'published', 'order']
    list_display_links = ['cover_thumb', 'title']
    list_filter   = ['period', 'published']
    list_editable = ['published', 'order']
    search_fields = ['title', 'description']
    inlines       = [PhotoInline]
    save_on_top   = True

    def cover_thumb(self, obj):
        if obj.cover:
            return format_html(
                '<img src="{}" style="width:52px;height:38px;object-fit:cover;border-radius:2px;" />',
                obj.cover.url)
        return format_html('<span style="color:#555;font-size:11px">—</span>')
    cover_thumb.short_description = ''

    def photo_count(self, obj):
        return obj.photos.count()
    photo_count.short_description = 'Фото'


@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display  = ['thumb', 'caption', 'album_link', 'date_text',
                     'fond_item_badge', 'staff_badge', 'published']
    list_display_links = ['thumb', 'caption']
    list_filter   = ['album__period', 'album', 'published']
    list_editable = ['published']
    search_fields = ['caption', 'date_text']
    # fond_item: raw_id for fast lookup across many items
    raw_id_fields     = ['fond_item']
    # linked_staff: horizontal widget for comfortable M2M
    filter_horizontal = ['linked_staff']
    readonly_fields   = ['thumb_large', 'fond_item_link', 'staff_links_display']
    save_on_top = True

    fieldsets = (
        ('Фотография', {
            'fields': ('album', 'image', 'thumb_large', 'caption', 'date_text', 'order', 'published'),
        }),
        ('🔗 Связи с другими разделами', {
            'fields': ('fond_item', 'fond_item_link', 'linked_staff', 'staff_links_display'),
            'description': (
                '<b>Предмет фонда</b> — если у этой фотографии есть физический оригинал '
                '(негатив, отпечаток) в архивном фонде, укажите его здесь. '
                'На странице фото появится кнопка «→ В фонд».<br>'
                '<b>Изображённые сотрудники</b> — выберите людей, которые изображены '
                'на фото или с ним связаны. На страницах этих сотрудников появится эта фотография.'
            ),
        }),
    )

    # ── Thumbnails ──────────────────────────────────────────────────────────

    def thumb(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="width:52px;height:38px;object-fit:cover;border-radius:2px;" />',
                obj.image.url)
        return '—'
    thumb.short_description = ''

    def thumb_large(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-width:300px;max-height:300px;object-fit:contain;'
                'border:1px solid #333;background:#1a1a1a;padding:4px;" />',
                obj.image.url)
        return '—'
    thumb_large.short_description = 'Превью'

    # ── List badges ─────────────────────────────────────────────────────────

    def album_link(self, obj):
        url = f'/admin/gallery/album/{obj.album_id}/change/'
        return format_html('<a href="{}">{}</a>', url, obj.album)
    album_link.short_description = 'Альбом'

    def fond_item_badge(self, obj):
        if obj.fond_item_id:
            return format_html('<span style="color:#e74c3c">✓ фонд</span>')
        return format_html('<span style="color:#444">—</span>')
    fond_item_badge.short_description = 'Фонд'

    def staff_badge(self, obj):
        if not obj.pk:
            return '—'
        c = obj.linked_staff.count()
        if c:
            return format_html('<span style="color:#e74c3c">✓ {}</span>', c)
        return format_html('<span style="color:#444">—</span>')
    staff_badge.short_description = 'Сотр.'

    # ── Cross-link read-only displays ────────────────────────────────────────

    def fond_item_link(self, obj):
        if not obj.fond_item_id:
            return format_html(
                '<span style="color:#666">Не выбран. Выберите предмет выше, чтобы '
                'создать ссылку с карточки фото на страницу архивного предмета.</span>')
        url = f'/admin/fond/fonditem/{obj.fond_item_id}/change/'
        return format_html(
            '<a href="{}" target="_blank" style="color:#e74c3c">↗ Открыть в разделе «Фонд»: {}</a>',
            url, obj.fond_item)
    fond_item_link.short_description = 'Ссылка на предмет фонда'

    def staff_links_display(self, obj):
        if not obj.pk:
            return '—'
        people = obj.linked_staff.all()
        if not people:
            return format_html(
                '<span style="color:#666">Сотрудники не выбраны. Используйте виджет выше.</span>')
        rows = []
        for s in people:
            url = f'/admin/staff/staffmember/{s.pk}/change/'
            rows.append(f'<a href="{url}" target="_blank" style="color:#e74c3c">↗ {s}</a>')
        return format_html('<br>'.join(rows))
    staff_links_display.short_description = 'Ссылки на страницы сотрудников'
