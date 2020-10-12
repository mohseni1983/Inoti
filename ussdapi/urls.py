from django.urls import path
from . import views
urlpatterns=[
    path('v2/',views.USSDApi,name='ussdapi'),
    path('v1/',views.api,name='api')


]