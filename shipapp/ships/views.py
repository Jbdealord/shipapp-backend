#Author: Debojit Kaushik ( 11th April 2017 )

'''Django Imports'''

'''Rest Framework Imports'''
from rest_framework.views import APIView
from rest_framework.decorators import authentication_classes
from rest_framework.authentication import TokenAuthentication

'''Misc Imports'''
from common import api_response, error_codes

'''Model Imports'''
from .models import Ship

'''Serializer Imports'''
from .serializers import ShipSerializer


class ShipHandler(APIView):
    '''
        Resource endpoint (Class Based View) for CRUD requests related to Ships.
        Methods: 
            GET
    '''
    serializer_class = ShipSerializer
    
    @authentication_classes((TokenAuthentication))
    def get(self,request):
        try:
            data_set = Ship.objects.all()
            if data_set.exists():
                serialized_data_set = ShipSerializer(
                    data_set,
                    many = True
                )
                return api_response(
                    success = True,
                    status = error_codes._OK,
                    data = serialized_data_set.data
                )
            else:
                return api_response(
                    success = False,
                    status = error_codes._NOT_FOUND,
                    data = "Ships not found."
                )
        except Exception as e:
            print(e)
            return api_response(
                success = False,
                status = error_codes._SERVER_ERROR,
                error = error_codes._EXCEPTION_ERROR
            )