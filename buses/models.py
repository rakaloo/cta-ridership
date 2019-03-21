from django.db import models
from django.db.models import Count, ExpressionWrapper, Func, F, Sum, Value
from django.db.models.functions import Cast, Concat
from django.contrib.postgres import fields
from django.contrib.postgres.aggregates import ArrayAgg


class StopQuerySet(models.QuerySet):
    def with_annotations(self):
        return self.annotate(
                intersection=Concat('on_street', 'cross_street'),
                total_routes=Count('routes')
            )


class Stop(models.Model):
    on_street = models.CharField(max_length=255)
    cross_street = models.CharField(max_length=255)
    routes_array = fields.ArrayField(models.CharField(max_length=5))
    boardings = models.DecimalField(max_digits=6, decimal_places=1)
    alightings = models.DecimalField(max_digits=6, decimal_places=1)
    month_beginning = models.DateField()
    daytype = models.CharField(max_length=10)
    location = models.CharField(max_length=255)
    routes = models.ManyToManyField('Route', through='RouteStop', related_name='stops')

    objects = StopQuerySet.as_manager()

    class Meta:
        db_table='stops'

    def __str__(self):
        return f'{self.on_street} & {self.cross_street}'


class RegexSubstring(Func):
    function = 'SUBSTRING'

    def __init__(self, expression, regex, **extras):
        expressions = [expression, Value(regex)]
        super(RegexSubstring, self).__init__(*expressions, **extras)


class RouteQuerySet(models.QuerySet):
    def with_annotations(self):
        return self.annotate(
                stripped_id=Cast(RegexSubstring('id', '[0-9]+'), models.IntegerField()),
                total_stops=Count('stops'),
                on_streets=ArrayAgg('stops__on_street', distinct=True),
                stop_streets=ArrayAgg('stops__on_street')
            ).annotate(
                avg_boardings=ExpressionWrapper(
                    Sum('stops__boardings')/F('total_stops'),
                    output_field=models.DecimalField()
                ),
                avg_alightings=ExpressionWrapper(
                    Sum('stops__alightings')/F('total_stops'),
                    output_field=models.DecimalField()
                )
            )


class Route(models.Model):
    id = models.CharField(max_length=5, primary_key=True, db_column='route_id')

    objects = RouteQuerySet.as_manager()

    class Meta:
        db_table='routes'

    def __str__(self):
        return self.id


class RouteStop(models.Model):
    route = models.ForeignKey(Route, on_delete=models.CASCADE)
    stop = models.ForeignKey(Stop, on_delete=models.CASCADE)

    class Meta:
        db_table='route_stops'
