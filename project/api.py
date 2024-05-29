from django.http import JsonResponse
from .models import *
from accuont.models import User
from .serializers import AccStatusMainSerializer
import pandas as pd
def getAccreditationData(request):
    id = request.GET['id']
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
        for value in val.col_active.all():
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
    return JsonResponse({'lable':lable,'data1':df.groupby(['year'],as_index=False)['data'].count().to_dict(),'data2':df2.groupby(['year'],as_index=False)['data'].count().to_dict()})


def getAccreditationPie(request):
    val = request.GET['val']
    data = {}
    for i in ['معتمد','غير معتمد','متقدمة للاعتماد','غير متقدمة للاعتماد']:
        data[i] = AccStatusMain.objects.filter(account__type_enterprise=val,Accreditation_Status=i).count()
    return JsonResponse(data)