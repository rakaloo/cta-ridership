from django.views.generic import ListView
from django.views.generic.detail import DetailView

from buses.models import Stop, Route


class StopListView(ListView):
    model = Stop
    template_name = 'stops.html'
    context_object_name = 'stops'
    paginate_by = 100


class RouteDetailView(DetailView):
    model = Route
    template_name = 'route.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

