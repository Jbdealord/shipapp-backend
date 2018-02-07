'''Django Imports.'''
from django.contrib.auth import authenticate, login


'''RestFramework Imports'''
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny

'''Misc Imports'''
from common import api_response, error_codes


'''Model Imports'''
from .models import User


'''Serializer Imports'''
from .serializers import UserSerializerFields


@api_view(['POST'])
@permission_classes((AllowAny, ))
def Login(request):
    try:
        assert 'username', 'password' in request.data

        u_name = request.data['username']
        p_word = request.data['password']
        user = authenticate(username = u_name, password = p_word)
        if user is not None:
            login(request, user)
            token = Token.objects.get_or_create(user = user)

            if type(token) == type((1,2)):
                token_key = token[0].key
            else:
                token_key = token.key

            serialized_data = UserSerializerFields(
                user
            )
            return api_response(
                success = True,
                status = error_codes._OK,
                data = serialized_data.data
            )
        else:
            return api_response(
                success = False,
                status = error_codes._UNAUTHORISED,
                data = "Login Failed."
            )

    except AssertionError as e:
        return api_response(
            success = False,
            status = error_codes._BAD_PARAM,
            error = error_codes._ASSERTION_ERROR
        )
    except Exception as e:
        return api_response(
            success = False,
            status = error_codes._SERVER_ERROR,
            error = error_codes._EXCEPTION_ERROR
        )