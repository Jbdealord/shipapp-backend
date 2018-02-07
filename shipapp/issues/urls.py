'''Django Imports'''
from django.conf.urls import url , include

'''View import'''
from .views import IssueHandler, SolutionHandler , SignOff, UploadImages


urlpatterns = [
    url(r'^$' , IssueHandler.as_view() , name = 'CBV_for_issues'),
    url(r'^solutions/$' , SolutionHandler.as_view() , name = 'CBV_for_solutions'),
    url(r'^signoff/$', SignOff , name = 'Issue_signoff'),
    url(r'^images/$', UploadImages , name = 'Image_upload'),
]