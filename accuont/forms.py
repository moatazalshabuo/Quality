from django import forms
from .models import *
class CreateAccount(forms.ModelForm):
    class Meta:
        model = User
        fields = ['company_name','email','username','password',]
        
    def __init__(self,*args, **kwargs):
        super(CreateAccount, self).__init__(*args, **kwargs)
        for key ,val in self.fields.items():
            val.widget.attrs['class'] = 'form-control'
        self.fields['password'].widget = forms.PasswordInput(attrs={'class':'form-control'})
        self.fields['password'].label = 'كلمة المرور'
        self.fields['email'].label = 'البريد الالكتروني'
        self.fields['username'].label = 'اسم المستخدم'
        self.fields['company_name'].label = 'اسم المؤسسة'
        
class editAccount(forms.ModelForm):
    class Meta:
        model = User
        fields = ['company_name','email','username',]
        
    def __init__(self,*args, **kwargs):
        super(editAccount, self).__init__(*args, **kwargs)
        for key ,val in self.fields.items():
            val.widget.attrs['class'] = 'form-control'
   
        self.fields['email'].label = 'البريد الالكتروني'
        self.fields['username'].label = 'اسم المستخدم'
        self.fields['company_name'].label = 'اسم المؤسسة'
        
class createDepartments(forms.ModelForm):
    class Meta:
        model = Depatment
        fields = ['name','account']
        
    def __init__(self,*args, **kwargs):
        super(createDepartments, self).__init__(*args, **kwargs)
        for key ,val in self.fields.items():
            val.widget.attrs['class'] = 'form-control'   
    