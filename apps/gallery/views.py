from django.views.generic import ListView, DetailView
from .models import Album, Photo, HistoricalPeriod


class GalleryHomeView(ListView):
    template_name = 'gallery/home.html'
    context_object_name = 'albums_by_period'
    model = Album

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        periods = []
        for code, label in HistoricalPeriod.choices:
            albums = Album.objects.filter(period=code, published=True).prefetch_related('photos')
            if albums.exists():
                periods.append({'code': code, 'label': label, 'albums': albums})
        ctx['periods'] = periods
        ctx['random_photos'] = Photo.objects.filter(published=True).order_by('?')[:16]
        return ctx


class AlbumDetailView(DetailView):
    template_name = 'gallery/album_detail.html'
    model = Album
    context_object_name = 'album'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['photos'] = self.object.photos.filter(published=True)
        ctx['other_albums'] = Album.objects.filter(
            period=self.object.period, published=True
        ).exclude(pk=self.object.pk)[:4]
        return ctx
