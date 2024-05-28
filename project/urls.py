from django.urls import path
from .views import *
from .api import *
urlpatterns = [
    path('create-accstatus',create_AccStatus,name="Accstaus.create"),
    path('get-program/<int:id>',getProgram,name='get.program'),
    path('accStatus',index,name='index.accStatus'),
    path('acc/index',Accindex,name='acc.index'),
    path('create-accs',create_Acc,name="Acc.create"),
    path('get-department/<int:id>',getDepartment,name='get.departemnt'),
    path('acc-edit/<int:id>',edit_acc,name='edit.acc'),
    path('Accreditation',Accreditation,name='Accreditation.chart'),
    path('api/Accreditation',getAccreditationData)
    ,path('quality_standard/index',qualityStandardIndex,name='quality_standard.index'),
    path('quality_standard/create',quality_standard_create,name="quality_standard.create"),
    path('quality_standard/<int:id>',quality_standard_delete,name='quality_standard.delete'),
    path('quality_standard/<int:id>/edit',quality_standard_edit,name='quality_standard.edit'),
    path('create_college_activities/<int:id>',create_college_activities,name='create_college_activities'),
    path('delete_college_activities/<int:id>',delete_college_active,name='delete_college_activities'),
    path('Workshops-lectures',Workshops_lectures,name='Workshops.lectures')
]
