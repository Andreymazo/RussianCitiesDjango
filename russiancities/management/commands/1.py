from django.core.management import BaseCommand

from russiancities.models import RusCity
from django.contrib.gis.geos import Point

# from users.managers import CustomUserManager
from shapely.geometry import Point, linestring
import csv
from django.core.management import BaseCommand



# """Найдем расстояние между двумя точками"""
# def dist_between():
#     ppto_a = Profile.objects.last().location
#     ppto_b = Profile.objects.first().location
#     # print(ppto_a)
#     dist = ppto_a.distance(ppto_b)*100
#     print('distance in km', dist)

class Command(BaseCommand):
    def handle(self, *args, **options):
        qs=RusCity.objects.all().filter(id__lt=4)#.values_list('name', 'location')
        # print(qs[0][1][0], qs[0][1][1])
        dist=qs.first().location.distance(qs.last().location)*100
        print(dist)
        # try:
        #     d= RusCity.objects.get(name='ппппппппппg')
        #     print(d.id)
        # #    City.objects.create(name='zzz', location=Point(50,33))
        #     # d= City.objects.filter(name='www')
        #     d.delete()
        #     print(d)
        # except RusCity.DoesNotExist as e:
        #     print(e)

# https://django.readthedocs.io/en/5.1.x/ref/contrib/gis/gdal.html