from collections import defaultdict

from django.views.generic import ListView
from django.views.generic.detail import DetailView

from buses.models import Stop, Route


class StopListView(ListView):
    model = Stop
    template_name = 'stops.html'
    context_object_name = 'stops'
    paginate_by = 20

    def get_queryset(self, **kwargs):
        queryset = super().get_queryset(**kwargs) 
        order_by = self.request.GET.get('order_by', 'intersection')
        return queryset.with_annotations().order_by(order_by)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_sort'] = self.request.GET.get('order_by', 'intersection')
        return context


class RouteListView(ListView):
    model = Route
    template_name = 'routes.html'
    context_object_name = 'routes'
    paginate_by = 20

    def get_queryset(self, **kwargs):
        queryset = super().get_queryset(**kwargs) 
        order_by = self.request.GET.get('order_by', 'default')
        if order_by == 'default':
            order_by_list = ['stripped_id', 'id']
        elif order_by == '-default' :
            order_by_list = ['-stripped_id', '-id']
        else:
            order_by_list = [order_by]
        return queryset.with_annotations().order_by(*order_by_list)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_sort'] = self.request.GET.get('order_by', 'default')
        for route in context['routes']:
            street_stop_count = defaultdict(int)
            for street in route.stop_streets:
                street_stop_count[street] += 1
            route.street_stop_list = sorted(list(street_stop_count.items()))
        return context
