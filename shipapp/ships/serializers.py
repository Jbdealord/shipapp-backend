# Author : Debojit Kaushik ( 10th April 2017 )

'''Rest Framework imports'''
from rest_framework import serializers

'''Model Imports'''
from .models import Ship


'''Serializer Imports'''
from users.serializers import UserSerializerFields

class ShipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ship
        exclude = (
            'owner',
            'departments'
        )
