from django.urls import path
from .views import *
urlpatterns = [
    path('create-accstatus',create_AccStatus,name="Accstaus.create"),
    path('get-program/<int:id>',getProgram,name='get.program'),
    path('accStatus',index,name='index.accStatus'),
    path('acc/index',Accindex,name='acc.index'),
    path('create-accs',create_Acc,name="Acc.create"),
    path('get-department/<int:id>',getDepartment,name='get.departemnt'),
    path('acc-edit/<int:id>',edit_acc,name='edit.acc')
]
