from django.contrib import admin
from django.utils.html import format_html
from .models import StaffMember


@admin.register(StaffMember)
class StaffMemberAdmin(admin.ModelAdmin):
    list_display  = ['photo_thumb', 'full_name', 'role', 'years_worked',
                     'personal_fund', 'fond_items_count', 'photos_count', 'published']
    list_display_links = ['photo_thumb', 'full_name']
    list_filter   = ['published']
    list_editable = ['published']
    search_fields = ['last_name', 'first_name', 'patronymic', 'role', 'biography']
    readonly_fields = ['photo_preview', 'created_at',
                       'fond_items_links', 'photos_links']
    save_on_top = True

    fieldsets = (
        ('ФИО', {
            'fields': ('last_name', 'first_name', 'patronymic'),
        }),
        ('Сведения', {
            'fields': ('role', 'years_worked', 'biography'),
        }),
        ('Фотография', {
            'fields': ('photo', 'photo_preview'),
        }),
        ('🔗 Связи с другими разделами', {
            'fields': ('personal_fund', 'fond_items_links', 'photos_links'),
            'description': (
                '<b>Личный фонд</b> — выберите фонд, который принадлежит этому сотруднику.<br>'
                '<b>Предметы фонда и фотографии</b> отображаются ниже автоматически — '
                'они привязываются со стороны своих разделов: '
                'предметы через «Фонд → Предметы», фото через «Галерея → Фотографии».'
            ),
        }),
        ('Публикация', {
            'fields': ('published', 'created_at'),
        }),
    )

    # ── Thumbnails ──────────────────────────────────────────────────────────

    def photo_thumb(self, obj):
        if obj.photo:
            return format_html(
                '<img src="{}" style="width:32px;height:40px;object-fit:cover;'
                'object-position:top;border-radius:2px;" />', obj.photo.url)
        return format_html('<span style="color:#555;font-size:11px">нет</span>')
    photo_thumb.short_description = ''

    def photo_preview(self, obj):
        if obj.photo:
            return format_html(
                '<img src="{}" style="max-width:220px;max-height:280px;object-fit:cover;'
                'object-position:top;border:1px solid #333;background:#1a1a1a;padding:4px;" />',
                obj.photo.url)
        return '—'
    photo_preview.short_description = 'Превью'

    # ── Counters ────────────────────────────────────────────────────────────

    def fond_items_count(self, obj):
        c = obj.fond_items.count()
        return format_html('<b style="color:{}">{}</b>', '#e74c3c' if c else '#555', c)
    fond_items_count.short_description = '📦 Предм.'

    def photos_count(self, obj):
        c = obj.photos.count()
        return format_html('<b style="color:{}">{}</b>', '#e74c3c' if c else '#555', c)
    photos_count.short_description = '📷 Фото'

    # ── Cross-link read-only displays ────────────────────────────────────────

    def fond_items_links(self, obj):
        if not obj.pk:
            return '—'
        items = obj.fond_items.all()
        if not items:
            return format_html(
                '<span style="color:#666">Предметы не привязаны. Откройте нужный предмет '
                'в разделе «Фонд → Предметы фонда» и выберите этого сотрудника '
                'в поле «Связанные сотрудники».</span>')
        rows = []
        for item in items[:10]:
            url = f'/admin/fond/fonditem/{item.pk}/change/'
            rows.append(f'<a href="{url}" target="_blank" style="color:#e74c3c">↗ {item.title[:60]}</a>')
        if items.count() > 10:
            rows.append(f'<span style="color:#666">...ещё {items.count()-10}</span>')
        return format_html('<br>'.join(rows))
    fond_items_links.short_description = 'Предметы фонда, связанные с этим сотрудником'

    def photos_links(self, obj):
        if not obj.pk:
            return '—'
        photos = obj.photos.all()
        if not photos:
            return format_html(
                '<span style="color:#666">Фотографии не привязаны. Откройте нужную фотографию '
                'в разделе «Галерея → Фотографии» и выберите этого сотрудника '
                'в поле «Изображённые сотрудники».</span>')
        rows = []
        for p in photos[:8]:
            url   = f'/admin/gallery/photo/{p.pk}/change/'
            label = (p.caption or f'Фото #{p.pk}')[:55]
            rows.append(f'<a href="{url}" target="_blank" style="color:#e74c3c">↗ {label}</a>')
        if photos.count() > 8:
            rows.append(f'<span style="color:#666">...ещё {photos.count()-8}</span>')
        return format_html('<br>'.join(rows))
    photos_links.short_description = 'Фотографии в галерее, связанные с этим сотрудником'
