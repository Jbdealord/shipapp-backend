'''Django Imports'''
from django.conf.urls import url, include

'''View import'''
from .views import DepartmentHandler

urlpattterns = [
    url(r'$' , DepartmentHandler.as_view(), name = 'CBV_for_departments'),
]