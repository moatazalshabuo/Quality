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
    path('api/Accreditation',getAccreditationData),
    path('api/AccreditationPie',getAccreditationPie),
    path('api/AccreditationPieMain',getAccreditationPieMain),
    path('api/quality_standard_api',quality_standard_api),
    path('api/get_students_staff',get_students_staff),
    path('quality_standard/index',qualityStandardIndex,name='quality_standard.index'),
    path('quality_standard/create',quality_standard_create,name="quality_standard.create"),
    path('quality_standard/<int:id>',quality_standard_delete,name='quality_standard.delete'),
    path('quality_standard/<int:id>/edit',quality_standard_edit,name='quality_standard.edit'),
    path('create_college_activities/<int:id>',create_college_activities,name='create_college_activities'),
    path('delete_college_activities/<int:id>',delete_college_active,name='delete_college_activities'),
    path('Workshops-lectures',Workshops_lectures,name='Workshops.lectures'),
    path('accreditation-status',accreditation_status,name='accreditation.status'),
    path('quality-standards',Quality_Standards,name='quality.standards'),
    path('University_education/',Acc_pdf,name='Acc_pdf'),
    path('Evaluation',Evaluation,name='Evaluation'),
    path('edit_Acc/<int:id>',edit_Acc,name='edit_Acc'),
    path('delete_acc/<int:id>',delete_acc,name='delete_acc')
]
