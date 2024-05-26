from django.shortcuts import render,redirect
from .models import *
from .forms import *
from .serializers import *
from django.contrib import messages
from django.http import JsonResponse
from accuont.models import User
from accuont.serializer import DepartmentSerialzer
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
    return render(request,'views/create_AccStatus.html',{'form':form})

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
                                                Accrediting_Body=request.POST['Accrediting_Body'])
            
            for x,y in zip(request.POST.getlist('quality_standards[]'),request.POST.getlist('ratio[]')):
                StandardAcc.objects.create(acc_status_main=accs,
                                            quality_standards=Quality_standards.objects.get(pk=x),
                                            ratio=y)
            return redirect('create_college_activities',id=accs.id)
            form= CreateAccStatus()
            messages.success(request,'تم الحفظ بنجاح ')
    return render(request,'views/admin/create_AccStatus.html',{'form':form,'account':account,'quality_standards':quality_standards})
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
