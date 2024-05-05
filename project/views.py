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
            form.save()
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
    if request.method == "POST":
        if form.is_valid():
            acc_status = form.save(commit=False)
            acc_status.account = User.objects.get(pk=request.POST['account'])
            acc_status.save()
            form= CreateAccStatus()
            messages.success(request,'تم الحفظ بنجاح ')
    return render(request,'views/admin/create_AccStatus.html',{'form':form,'account':account})

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