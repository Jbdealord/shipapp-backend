"""shipapp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""

'''Django Imports'''
from django.conf.urls import url , include
from django.contrib import admin

'''Rest Framework Imports'''


'''Url imports from respective apps'''
# from departments.urls import *
from issues import urls as issue_urls
from users import urls as user_urls
from departments.views import DepartmentHandler
from ships.views import ShipHandler

urlpatterns = [
    url(r'^departments/$', DepartmentHandler.as_view()),
    url(r'^ships/$', ShipHandler.as_view(), name = 'Crud_for_ships'),
    url(r'^admin/', admin.site.urls),
    url(r'^users/', include(user_urls, namespace = 'User_urls')),
    url(r'^issues/' , include(issue_urls, namespace = 'Issues_urls')),
    url(r'^docs/', include('rest_framework_docs.urls')),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
