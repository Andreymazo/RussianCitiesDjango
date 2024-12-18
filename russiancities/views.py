import json
import re
from django.http import HttpResponse
import requests
from rest_framework.decorators import api_view, permission_classes, renderer_classes, authentication_classes
from rest_framework import status, permissions
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer, BrowsableAPIRenderer
from russiancities.models import RusCity
# from django.core.paginator import Paginator
from rest_framework.pagination import PageNumberPagination
from drf_spectacular.utils import extend_schema
from russiancities.serializers import CityCreateSerializer, CitySerializer
from django.views.decorators.csrf import csrf_exempt
from django.contrib.gis.db.models import PointField
from django.contrib.gis.geos import Point
# from shapely.geometry import Point, linestring
from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.measure import D 

def values_to_param(filter_query, param):
    if not re.compile(f"{param}=(.*)&"):
      param = re.compile(f"{param}=(\d+)&")
    param = re.compile(f"{param}=(\d+)")
    param = param.findall(filter_query)
    return param

# напишем функцию для получения второго элемента
def sort_key(e):
    return e[1]

"""Найдем ближайшее расстояне к введенному из кверисета"""
def get_closest_to_dt(qs, dt):
    
    # greater = qs.filter(location__gte=dt).order_by("location").first()
    greater = qs.filter(location__gte=dt).order_by("location").first()
    less = qs.filter(location__lte=dt).order_by("-location").first()
    
    if greater and less:
        # return greater if abs(greater.location - dt) < abs(less.location - dt) else less
        return greater if greater.location.distance(dt) < less.location.distance(dt) else less
    else:
        return greater or less
"""На входе слово-пароль и координаты, на выходе список городов"""
@csrf_exempt
@api_view(('POST',))
@renderer_classes((JSONRenderer, BrowsableAPIRenderer))#TemplateHTMLRenderer, 
def rus_city(request):
    print('We at testbase home')
    # print('request.META.cookies', request.META.cookies)
    print('request.__dict__', request.__dict__)
    
    #Здесь проверяем чтобы в куках был емэйл и они пришли по правильному установленными
    try:
        text = request.META['HTTP_COOKIE']
        three_elem_tuple= text.partition("=")
        print('three_elem_tuple[0], three_elem_tuple[1], three_elem_tuple[2]', three_elem_tuple[0], three_elem_tuple[1], three_elem_tuple[2])#
        #session_email = adsf@arfg.com
        if three_elem_tuple[0] != "session_email" or three_elem_tuple[1] != "=":
            print('Wrong cookie_name or somthing wrong in set cookie proccess')
            return Response({"message": "Wrong cookie_name or somthing wrong in set cookie proccess"})
    except KeyError as e: 
        print(e, 'HTTP_COOKIE doesnt exist')
    
    print('request.META[14:]', request.META['HTTP_COOKIE'][14:])#session_email=adsf@arfg.com
    print('request.POST', request.META['HTTP_COOKIE'])
    
    # result = False
    key_reply='key_reply'
    # cad_num = 'cad_num'
    shirota = 'shirota'
    dolgota = 'dolgota'
    # print('request.META'  , request.META)
    # print("request.META['QUERY_STRING']", request.META['QUERY_STRING']) ## cad_num=23&shirota=23&dolgota=23
    # print('request.__dict__', request.__dict__)
    filter_query = request.META['QUERY_STRING']#filter_query='/?key_reply=444&shirota=53.4343&dolgota=44.4444 HTTP/1.1'
    print('filter_query', filter_query)
    key_reply = values_to_param(filter_query, key_reply)
    # cad_num = values_to_param(filter_query, cad_num)
    shirota = values_to_param(filter_query, shirota)
    dolgota = values_to_param(filter_query, dolgota)
    # filter_query_all = (cad_num[0], shirota[0], dolgota[0])
    filter_query_all = (key_reply[0], shirota[0], dolgota[0])
    print('filter_query_all', filter_query_all)
    

    # print('dolgota______________________________', dolgota)
    # cad_num = re.compile(f"{cad_num}=(\d+)&")
    # cad_num = cad_num.findall(filter_query)
    # print('cad_num______________________________', cad_num[0])
        # clear_query=re.compile("cad_num \(ts\/tv\) =")
        # clear_query = re.compile("cad_num=(.*)&")
    
    # print('filter_query_all', filter_query_all)
    # clear_query = re.compile(f"{cad_num}=(\d+)&")
    # clear_query = clear_query.findall(filter_query)[0]
    # print('print(request.POST.__dict__)', request.POST.__dict__)

    # filter_lst =sorted(list(RusCity.objects.all().values_list('name', 'location')), key=sort_key) # Упорядочили по локации, \
    # если в моделя по локации упорядочено, то наверное лишнее здесь повторять
    filter_qs = RusCity.objects.all()
    location_income=Point(float(shirota[0]), float(dolgota[0]))
    print('location_income', location_income)
    # result = get_closest_to_dt(filter_qs, location_income)
    result = RusCity.objects.filter(location__distance_lte=(location_income, D(km=70)))
    print('result', result)
    # filter_lst_coords=[(i.name, i.location[0], i.location[1]) for i in filter_lst]
    # if location_income in filter_lst:
    #     result = True
    # print("filter_query = request.META['QUERY_STRING']", filter_query)

    print('almost finish ))))))))))))))))))')
    
    url = 'http://127.0.0.1:8000/ad/result/receive'
    # data = {result:result}
    # qs={}
    list_of_data=result.values_list('name', 'location')
    print('list_of_data', list_of_data) 
    # response = requests.post(url, params=data)#, headers={ 'X-CSRFToken': clear_token})
    print("result.values_list('name', 'location')", result.values_list('name', 'location'))
    response = requests.get(url, params=list_of_data)
    # print('response.headers', response_get.headers)
    # print('request.META', request.META['HTTP_COOKIE'])
    # data = json.dumps(result)
    # print('filter_query_all', filter_query_all, 'filter_lst', filter_lst)
    # print('result', result)
    print('response.content', response)
    # if request.method == "POST":

    #   try:
    #         # reobject=RealEstateObject.objects.all().get(cad_num=cad_num, shirota=shirota, dolgota=dolgota)
    #         result=True
    #         context = {
    #             'result':result

    #     }
    #        # time.sleep(7)# Не обязательно все 60 сек ждать, достаточно 7
    #         print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')

    #   except :
    #     print('--------------------------------------------iiii--------------------------------------')
    #     context = [{
    #     'result':result
    #     }]
    #   return HttpResponse(data, content_type='json')
    serialiser = CitySerializer(result, many=True)
    print('serialiser.data', serialiser.data)
    return Response(serialiser.data)


# from django.shortcuts import render

# class CitySerializer(serializers.ModelSerializer):
    
#     class Meta:
#         model = City
#         fields = '__all__'
    
#     def create(self, validated_data):
#         request = self.context.get('request')
#         print('validated_data', validated_data)
#         try: 
#             city_instance = City.objects.get(**validated_data)
#             return Response({"message":"Такой город уже есть"})
#         except City.DoesNotExist:
#             city_instance = City.objects.create(**validated_data)
#         city_instance.save()
#         return city_instance

# def home(request):
#     serializer = 
#     return Response()

# @extend_schema(
#         tags=["Вход/регистрация"],
#         description="Ввод персональных данных пользователя.",
#         summary="Регистрация пользователя",
#         request=SignUpSerializer,
#         responses={
#             status.HTTP_200_OK: OpenApiResponse(
#                 description="Успешный ввод персональных данных",
#                 response=SignUpSerializer,
#             ),
#         }
# )
@extend_schema(
        request=CityCreateSerializer,
        responses={201: CityCreateSerializer},
    )
@api_view(['GET', 'POST'])
# @authentication_classes([TokenAuthentication])
@permission_classes((permissions.AllowAny,))
def home(request):
    """
    List all categories
    """
    if request.method == 'GET':
    
        paginator = PageNumberPagination()
        paginator.page_size = 10
        paginator.last_page_strings = ('last',)
        result_page = paginator.paginate_queryset(RusCity.objects.all(), request)
        serializer = CitySerializer(result_page, many=True)

        return paginator.get_paginated_response(serializer.data)
    
    if request.method == 'POST':
        serializer = CityCreateSerializer(data=request.data, context={'request': request})
        print('does we here?????????????????????')
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# {
#     "data": [
#         {
#             "id": 1,
#             "name": "Zyabrikovo  ",
#             "location": "SRID=4326;POINT (56.84665 34.7048)",
#             "moderarated": false
#         },
