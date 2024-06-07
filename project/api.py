from django.http import JsonResponse
from .models import *
from accuont.models import User
from .serializers import AccStatusMainSerializer
import pandas as pd
from .serializers import *
def getAccreditationData(request):
    id = request.GET['id']
    if id == 'all':
        account = AccStatusMain.objects.filter()  
    else:      
        account = AccStatusMain.objects.filter(account=User.objects.get(pk=id))
    data1 = {
        'year':[],
        'session':[],
        'data':[]
    }
    data2 = {
        'year':[],
        'session':[],
        'data':[]
    }
    for val in account:
        for value in val.col_active.order_by('year').all():
            if value.type_activity == 'محاضرة':
                data1['year'].append(f'{value.year} - {value.seasson}')
                # data1['session'].append(value.seasson)
                data1['data'].append(value.type_activity)
            else:
                data2['year'].append(f'{value.year} - {value.seasson}')
                # data2['session'].append(value.seasson)
                data2['data'].append(value.type_activity)
    df = pd.DataFrame(data1,columns=['year','data'])
    df2 = pd.DataFrame(data2,columns=['year','data'])
    # print(df)
    # print(df.groupby(['year','session'], as_index=False)['data'].count())
    lable = data1['year'] + data2['year']
    lable = list(set(lable))
 
    return JsonResponse({'id':id,'lable':lable,'data1':df.groupby(['year'],as_index=False)['data'].count().to_dict(),'data2':df2.groupby(['year'],as_index=False)['data'].count().to_dict()})


def getAccreditationPie(request):
    val = request.GET['val']
    data = {}
    if val == 'all':
         for i in ['معتمد','غير معتمد','متقدمة للاعتماد','غير متقدمة للاعتماد']:
            data[i] = AccStatusMain.objects.filter(Accreditation_Status=i).count()
    else: 
        for i in ['معتمد','غير معتمد','متقدمة للاعتماد','غير متقدمة للاعتماد']:
            data[i] = AccStatusMain.objects.filter(account__type_enterprise=val,Accreditation_Status=i).count()
    return JsonResponse(data)

def getAccreditationPieMain(request):
    val = request.GET['val']
    data = {}
    if val == 'all':
         for i in ['معتمد','غير معتمد','متقدمة للاعتماد','غير متقدمة للاعتماد']:
            data[i] = AccStatusMain.objects.filter(Accreditation_Status=i).count()
    else: 
        for i in ['معتمد','غير معتمد','متقدمة للاعتماد','غير متقدمة للاعتماد']:
            data[i] = AccStatusMain.objects.filter(account_id=val,Accreditation_Status=i).count()
    return JsonResponse(data)

def quality_standard_api(request):
    val = request.GET['val']
    depe = AccStatusMain.objects.filter(account=User.objects.get(pk=val)).last().stan_acc.all()
    return JsonResponse({'data':StandardAccSerializer(depe,many=True).data})

def get_students_staff(request):
    val = request.GET['val']
    students = 0
    staff = 0
    if val == 'all':
        for val in User.objects.all():
            students += val.students
            staff += val.staff
    else:
        account = User.objects.get(pk=val)
        staff = account.staff
        students = account.students
    return JsonResponse({'students':students,'staff':staff})