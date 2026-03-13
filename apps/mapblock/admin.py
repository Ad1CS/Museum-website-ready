from django.contrib import admin
from django.utils.html import format_html
from .models import Building


@admin.register(Building)
class BuildingAdmin(admin.ModelAdmin):
    list_display  = ['map_preview_thumb', 'name', 'built_years',
                     'pos_display', 'order', 'published']
    list_display_links = ['map_preview_thumb', 'name']
    list_editable = ['order', 'published']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    filter_horizontal   = ['photos']
    readonly_fields     = ['map_live_preview']
    save_on_top = True

    fieldsets = (
        ('Основное', {
            'fields': ('name', 'slug', 'built_years', 'description', 'published'),
        }),
        ('📐 Позиция на карте (%)', {
            'fields': (
                ('map_left', 'map_top'),
                ('map_width', 'map_height'),
                'order',
                'map_live_preview',
            ),
            'description': (
                'Все значения — в процентах от размера карты (0–100). '
                '<b>Левый верхний угол</b> задаётся полями «Слева» и «Сверху». '
                '<b>Размер</b> — «Ширина» и «Высота». '
                'Предпросмотр обновляется после сохранения.'
            ),
        }),
        ('Фотографии', {
            'fields': ('photos',),
        }),
    )

    # ── List display helpers ─────────────────────────────────────────────

    def map_preview_thumb(self, obj):
        """Mini map thumbnail showing where the building sits."""
        return format_html(
            '<div style="position:relative;width:80px;height:50px;'
            'background:#222;border:1px solid #333;border-radius:2px;overflow:hidden;">'
            '<div style="position:absolute;left:{l}%;top:{t}%;width:{w}%;height:{h}%;'
            'background:rgba(192,57,43,0.5);border:1px solid #e74c3c;box-sizing:border-box;">'
            '</div></div>',
            l=obj.map_left, t=obj.map_top,
            w=obj.map_width, h=obj.map_height,
        )
    map_preview_thumb.short_description = 'Позиция'

    def pos_display(self, obj):
        return format_html(
            '<span style="font-family:monospace;font-size:11px;color:#aaa">'
            'L:{} T:{} &nbsp; {}×{}</span>',
            obj.map_left, obj.map_top, obj.map_width, obj.map_height,
        )
    pos_display.short_description = 'L / T / W×H'

    # ── Full-size live preview in change form ────────────────────────────

    def map_live_preview(self, obj):
        """Rendered preview of the map with this building highlighted."""
        return format_html(
            '''<div style="margin-top:12px;">
              <div style="font-size:11px;color:#888;margin-bottom:6px;
                font-family:Oswald,sans-serif;letter-spacing:.1em;text-transform:uppercase;">
                Предпросмотр позиции на карте
              </div>
              <div style="position:relative;width:340px;height:200px;
                background:#1a1a1a;border:1px solid #333;overflow:hidden;">
                <div style="position:absolute;left:{l}%;top:{t}%;width:{w}%;height:{h}%;
                  background:rgba(192,57,43,0.35);border:2px solid #e74c3c;box-sizing:border-box;
                  display:flex;align-items:center;justify-content:center;">
                  <span style="background:rgba(0,0,0,.85);color:#f0ede8;
                    font-family:Oswald,sans-serif;font-size:9px;letter-spacing:.06em;
                    text-transform:uppercase;padding:2px 5px;white-space:nowrap;
                    border:1px solid #8b1a1a;">{name}</span>
                </div>
                <span style="position:absolute;bottom:4px;right:6px;
                  font-family:monospace;font-size:10px;color:#444;">
                  L:{l}% T:{t}% &nbsp; {w}%×{h}%
                </span>
              </div>
              <p style="font-size:11px;color:#666;margin-top:6px;">
                Измените значения выше и нажмите «Сохранить» — предпросмотр обновится.
              </p>
            </div>''',
            l=obj.map_left, t=obj.map_top,
            w=obj.map_width, h=obj.map_height,
            name=obj.name,
        )
    map_live_preview.short_description = ''
