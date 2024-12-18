from rest_framework import serializers
from rest_framework.response import Response
from russiancities.models import RusCity

class CitySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = RusCity
        fields = '__all__'
    
    
class CityCreateSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = RusCity
        fields = ['name', 'location']
    
    def create(self, validated_data):
        request = self.context.get('request')
        print('request.user', request.user)
        print('validated_data', validated_data)
        try: 
            city_instance = RusCity.objects.get(**validated_data)
            return Response({"message":"Такой город уже есть"})
        except RusCity.DoesNotExist:
            # city_instance=RusCity(name=validated_data['name'], location=validated_data['location'])
            city_instance = RusCity.objects.create(**validated_data)
            city_instance.save()
            return city_instance
    
