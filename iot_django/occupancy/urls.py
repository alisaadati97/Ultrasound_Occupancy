
from django.urls import path 
from .views import * 

urlpatterns = [
    path('', index) ,
    path('getdata', getdata) ,
    path('senddata', senddata) ,
]
