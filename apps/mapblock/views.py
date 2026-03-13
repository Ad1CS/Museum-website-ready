from django.views.generic import TemplateView, DetailView
from .models import Building


class MapView(TemplateView):
    template_name = 'mapblock/map.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['buildings'] = Building.objects.filter(published=True)
        return ctx


class BuildingDetailView(DetailView):
    template_name = 'mapblock/building.html'
    model = Building
    context_object_name = 'building'
    slug_url_kwarg = 'slug'
