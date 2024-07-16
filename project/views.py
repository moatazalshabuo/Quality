from django.shortcuts import render,redirect
from .models import *
from .forms import *
from .serializers import *
from django.contrib import messages
from django.http import JsonResponse
from accuont.models import User
from accuont.serializer import DepartmentSerialzer
import pandas as pd
# Create your views here.

def create_AccStatus(request):
    form = AccStatusForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            # accs = AccStatusMain.objects.create(Accreditation_Status=request.POST['Accreditation_Status'],
            #                                     Accrediting_Body=request.POST['Accrediting_Body'])
            for x,y in zip(request.POST.getlist('quality_standards'),request.POST.getlist('ratio')):
                print(x,y)
            messages.success(request,'تم الحفظ بنجاح ')
    years= range(datetime.datetime.now().year-2,datetime.datetime.now().year)
    return render(request,'views/create_AccStatus.html',{'form':form,'years':years})

def getProgram(request,id):
    institution = Institution.objects.get(pk=id)
    program = institution.program.all()
    return JsonResponse({'data':ProgramSerializer(program,many=True).data})

def index(request):
    accStatus = AccStatus.objects.all()
    
    return render(request,'views/AccStatus.html',{'AccStatus':accStatus})

def create_Acc(request):
    form = CreateAccStatus(request.POST or None,request.FILES or None)
    account = User.objects.filter(is_superuser=0)
    quality_standards = Quality_standards.objects.all()
    if request.method == "POST":
        if form.is_valid():
            # acc_status = form.save(commit=False)
            accou = User.objects.get(pk=request.POST['account'])
            # acc_status.save()
            accs = AccStatusMain.objects.create(account=accou,Accreditation_Status=request.POST['Accreditation_Status'],
                                                Accrediting_Body=request.POST['Accrediting_Body'],year=request.POST['year'])
            
            for x,y in zip(request.POST.getlist('quality_standards[]'),request.POST.getlist('ratio[]')):
                StandardAcc.objects.create(acc_status_main=accs,
                                            quality_standards=Quality_standards.objects.get(pk=x),
                                            ratio=y)
            return redirect('create_college_activities',id=accs.id)
            form= CreateAccStatus()
            messages.success(request,'تم الحفظ بنجاح ')
    years= range(datetime.datetime.now().year-2,datetime.datetime.now().year)
    return render(request,'views/admin/create_AccStatus.html',{'form':form,'account':account,'quality_standards':quality_standards,'years':years})

def edit_Acc(request,id):
    acc = AccStatusMain.objects.get(pk=id)
    form = CreateAccStatus(request.POST or None,request.FILES or None,instance=acc)
    # account = User.objects.filter(is_superuser=0)
    quality_standards = StandardAcc.objects.filter(acc_status_main=acc)
    if request.method == "POST":
        if form.is_valid():
            # # acc_status = form.save(commit=False)
            # accou = User.objects.get(pk=request.POST['account'])
            # # acc_status.save()
            acc.Accreditation_Status = request.POST['Accreditation_Status']
            acc.Accrediting_Body = request.POST['Accrediting_Body']
            acc.year = request.POST['year']
            acc.save()
            for x,y in zip(request.POST.getlist('quality_standards[]'),request.POST.getlist('ratio[]')):
                st = StandardAcc.objects.filter(acc_status_main=acc,
                                            quality_standards=Quality_standards.objects.get(pk=x),
                                            ).first()
                
                st.ratio=y
                st.save()
            form= CreateAccStatus()
            messages.success(request,'تم الحفظ بنجاح ')
            return redirect('acc.index')
    years= range(datetime.datetime.now().year-2,datetime.datetime.now().year)
    return render(request,'views/admin/edit_AccStatus.html',{'form':form,'quality_standards':quality_standards,'years':years})

def delete_acc(request,id):
    acc = AccStatusMain.objects.get(pk=id)
    acc.delete()
    messages.success(request,'تم الحذف بنجاح ')
    return redirect('acc.index')

import datetime
def create_college_activities(request,id):
    years= range(datetime.datetime.now().year-2,datetime.datetime.now().year)
    acc = AccStatusMain.objects.get(pk=id)
    
    if request.method == 'POST':
        College_activities.objects.create(acc_status_main=acc,
                name=request.POST['name'],
                year=request.POST['year'],
                type_activity=request.POST['type'],
                seasson=request.POST['seasson'])
        messages.success(request,'تم الحفظ بنجاح ')
    college_active = College_activities.objects.filter(acc_status_main=acc)
    return render(request,'views/admin/create_collage_active.html',{'years':years,'college_active':college_active,'acc':acc})

def delete_college_active(request,id):
    c = College_activities.objects.get(pk=id)
    id = c.acc_status_main.id
    c.delete()
    messages.success(request,'تم الحذف بنجاح ')
    return redirect('create_college_activities',id=id)

def getDepartment(request,id):
    institution = User.objects.get(pk=id)
    departemnt = institution.depatment_set.all()
    return JsonResponse({'data':DepartmentSerialzer(departemnt,many=True).data})

def Accindex(request):
    if request.user.is_superuser:
        accStatus = AccStatusMain.objects.all()
    else:
        accStatus = AccStatusMain.objects.filter(account=request.user.id)
    return render(request,'views/admin/AccStatus.html',{'AccStatus':accStatus})

def deleteAcc(request,id):
    AccStatusMain.objects.get(pk=id).delete()
    messages.success(request,'تم الحذف بنجاح')
    return redirect('acc.index')

def edit_acc(request,id):
    acc = AccStatusMain.objects.get(pk=id)
    form = CreateAccStatus(request.POST or None,request.FILES or None,instance=acc)
    account = User.objects.filter(is_superuser=0)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.success(request,'تم الحفظ بنجاح ')
            return redirect('acc.index')
    return render(request,'views/admin/edit_acc.html',{'form':form,'account':account,'acc':acc})

def Accreditation(request):
    return render(request,'views/charts/Accreditation.html')

def qualityStandardIndex(request):
    accStatus = Quality_standards.objects.all()
 
    return render(request,'views/admin/quality_standards.html',{'Quality_standards':accStatus})

def quality_standard_create(request):
    form = Quality_standardsForm(request.POST or None,request.FILES or None)

    if request.method == "POST":
        if form.is_valid():
            form.save()
            form= Quality_standardsForm()
            messages.success(request,'تم الحفظ بنجاح ')
    return render(request,'views/admin/quality_standards_create.html',{'form':form})

def quality_standard_delete(request,id):
    Quality_standards.objects.get(pk=id).delete()
    messages.success(request,'تم الحذف بنجاح')
    return redirect('quality_standard.index')

def quality_standard_edit(request,id):
    acc = Quality_standards.objects.get(pk=id)
    form = Quality_standardsForm(request.POST or None,instance=acc)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.success(request,'تم الحفظ بنجاح ')
            return redirect('quality_standard.index')
    return render(request,'views/admin/quality_standards_edit.html',{'form':form,})

def Workshops_lectures(request):
    account = User.objects.filter(is_superuser=False)
    return render(request,'views/charts/Workshops_&_lectures.html',{'account':account})

def accreditation_status(request):
    
    return render(request,'views/charts/Accreditation.html')


def Quality_Standards(request):
    account = User.objects.filter(is_superuser=False)
    # depe = Quality_standards.objects.all()
    if request.user.is_superuser:
        depe = []
        if request.method == 'POST':
            depe = AccStatusMain.objects.filter(account=User.objects.get(pk=request.POST['id'])).last().stan_acc.all()
    else:
        depe = AccStatusMain.objects.filter(account=request.user).last().stan_acc.all()
    return render(request,'views/charts/gusis_chart.html',{'account':account,'depe':depe})

def Acc_pdf(request):
    return render(request,'views/Acc.html')
    
def Evaluation(request):
    df = pd.read_excel('static/data.xlsx')
    def calculate_totals(df):
        totals = {1: [], 2: [], 3: [], 4: [], 5: []}
        for col in df.columns:
            counts = df[col].value_counts().reindex([1, 2, 3, 4, 5], fill_value=0)
            for k, v in counts.items():
                totals[k].append(v)
        return totals
    
    criteria_data = {
        "criteria1": calculate_totals(df.iloc[:, 0:4]),
        "criteria2": calculate_totals(df.iloc[:, 4:8]),
        "criteria3": calculate_totals(df.iloc[:, 8:12]),
    }
    labels = {
        "criteria1": df.columns[0:4].to_list(),
        "criteria2": df.columns[4:8].to_list(),
        "criteria3": df.columns[8:12].to_list(),
    }
    print(criteria_data)
    return render(request,'views/admin/Evaluation.html',{'criteria_data':criteria_data,'labels':labels})