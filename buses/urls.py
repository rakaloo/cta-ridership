from django.urls import include, path

from buses.views import StopListView, RouteDetailView

urlpatterns = [
    path('stops/', StopListView.as_view(), name='stops'),
    path('route/<pk>', RouteDetailView.as_view(), name='route')
]