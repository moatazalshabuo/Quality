from django.urls import path
from .views import *
urlpatterns = [
    path('create-accstatus',create_AccStatus,name="Accstaus.create"),
    path('get-program/<int:id>',getProgram,name='get.program'),
    path('accStatus',index,name='index.accStatus')
]
