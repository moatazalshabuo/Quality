from django import forms
from .models import *

class AccStatusForm(forms.ModelForm):
    class Meta:
        model = AccStatus
        fields = '__all__'
      
    def __init__(self, *args, **kwargs):
        super(AccStatusForm,self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            
        self.fields['Accreditation_Start_Date'].widget = forms.DateInput(attrs={'type': 'date','class':'form-control'})
        self.fields['Accreditation_End_Date'].widget = forms.DateInput(attrs={'type': 'date','class':'form-control'})
        
class CreateAccStatus(forms.ModelForm):
    class Meta:
        model = AccStatusMain
       
        fields = ("Accreditation_Status",
                  "Accrediting_Body",  
                    )
        widgets = {
            'Accrediting_Body' : forms.RadioSelect(),
            'Accreditation_Status' : forms.RadioSelect()
            }
    
class Quality_standardsForm(forms.ModelForm):
    class Meta:
        model = Quality_standards
       
        fields = '__all__'
    def __init__(self, *args, **kwargs):
        super(Quality_standardsForm,self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'