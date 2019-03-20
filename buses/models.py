from django.db import models
from django.contrib.postgres import fields


class Stop(models.Model):
    on_street = models.CharField(max_length=255)
    cross_street = models.CharField(max_length=255)
    routes_array = fields.ArrayField(models.CharField(max_length=5))
    boardings = models.DecimalField(max_digits=6, decimal_places=1)
    alightings = models.DecimalField(max_digits=6, decimal_places=1)
    month_beginning = models.DateField()
    daytype = models.CharField(max_length=10)
    location = models.CharField(max_length=255)

    class Meta:
        db_table='stops'

    def __str__(self):
        return f'{self.on_street} & {self.cross_street}'


class RouteQuerySet(models.QuerySet):
    def with_annotations(self):
        return self.annotate(
                total_stops=COUNT(stops),
                # main_route=
            )
        # .annotate(
        #         avg_boarding=SUM(stops.,
        #         avg_alightings=,
        #     )


class Route(models.Model):
    id = models.CharField(max_length=5, primary_key=True, db_column='route_id')
    stops = models.ManyToManyField(Stop, through='RouteStop')
    objects = RouteQuerySet.as_manager()

    class Meta:
        db_table='routes'

    def __str__(self):
        return id


class RouteStop(models.Model):
    route_id = models.ForeignKey(Route, on_delete=models.CASCADE)
    stop_id = models.ForeignKey(Stop, on_delete=models.CASCADE)

    class Meta:
        db_table='route_stops'
