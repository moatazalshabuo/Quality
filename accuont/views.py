from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import *
from .forms import *
from project.models import *
# Create your views here.
@login_required
def index(request):
    
    return render(request,'home.html',{'depe':Quality_standards.objects.all(),'account':User.objects.filter(is_superuser = False)})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
         
        if user is None:
            # Display an error message if authentication fails (invalid password)
            messages.error(request, "Invalid Password Or PAssword")
           
        else:
            # Log in the user and redirect to the home page upon successful login
            login(request, user)
            return redirect('/')
            
    return render(request,'views/login.html')

def logout_view(request):
    logout(request)
    return redirect('/')

@login_required
def create_account(request):
    form = CreateAccount(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(request.POST['password'])
            user.save()
            form = CreateAccount()
            messages.success(request,'تم الحفظ بنجاح')
    return render(request,'views/create_account.html',{'form':form})

@login_required
def accounts(request):
    users = User.objects.all()
    return render(request,'views/account.html',{'users':users})

@login_required
def edit_account(request,id):
    user = User.objects.get(pk=id)
    form = editAccount(request.POST or None,instance=user)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.success(request,'تم الحفظ بنجاح')
            return redirect('accounts')
    return render(request,'views/edit_account.html',{'form':form})
@login_required
def delete_accont(request):
    User.objects.get(pk=id).delete()
    messages.success(request,'تم الحذف بنجاح')
    return redirect('accounts')
    
@login_required
def department(request,id):
    form = createDepartments(request.POST or None)
    account = User.objects.get(pk=id)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.success(request,'تم الاضافة بنجاح ')
            return redirect(f'department',id=account.id)
    return render(request,'views/department.html',{'form':form,'account':account})

@login_required
def delete_dep(request,id):
    department = Depatment.objects.get(pk=id)
    id_account = department.account.id
    department.delete()
    messages.success(request,'تم الحذف بنجاح')
    return redirect('department',id=id_account)