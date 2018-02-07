'''Django Imports'''
from django.conf.urls import url

'''View import'''
from .views import Login


urlpatterns = [
    url(r'^login/$' , Login , name = 'login_call'),
]