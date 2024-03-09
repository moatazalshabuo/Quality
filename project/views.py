from django.shortcuts import render
from .models import *
from .forms import *
from .serializers import *
from django.contrib import messages
from django.http import JsonResponse
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