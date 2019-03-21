from django.urls import include, path

from buses.views import StopListView, RouteListView

urlpatterns = [
    path('stops/', StopListView.as_view(), name='stops'),
    path('routes', RouteListView.as_view(), name='routes')
]