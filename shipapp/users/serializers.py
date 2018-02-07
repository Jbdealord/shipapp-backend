# Author : Debojit Kaushik ( 10th April 2017 )

'''reast Framework Imports'''
from rest_framework import serializers
from rest_framework.authtoken.models import Token

'''Model Imports'''
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        depth = 2

        fields = '__all__'


class TokenSerializer(serializers.ModelSerializer):

    class Meta:
        model = Token
        exclude = (
            'user',
            'created'
        )

class UserSerializerFields(serializers.ModelSerializer):
    auth_token = TokenSerializer(read_only = True)
    class Meta:
        model = User

        exclude = (
            'password',
            'is_superuser',
            'is_staff',
            'is_active',
            'groups',
            'user_permissions'
        )