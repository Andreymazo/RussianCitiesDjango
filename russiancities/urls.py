from russiancities.apps import RussiancitiesConfig
from django.urls import path

from russiancities.views import  rus_city

app_name = RussiancitiesConfig.name

urlpatterns = [
    path('rus_cities', rus_city, name='home'),
   
]
