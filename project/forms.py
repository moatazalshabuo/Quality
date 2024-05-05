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
       
        fields = ("Accrediting_Body",
                    "Accreditation_Status",
                    "Accreditation_Start_Date",
                    "Accreditation_End_Date",
                    "Compliance_Level",
                    "Accreditation_Criteria",
                    "Self_Assessment_Reports",
                    "Site_Visit_Reports",
                    "Supporting_Documentation")
    def __init__(self, *args, **kwargs):
        super(CreateAccStatus,self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            
        self.fields['Accreditation_Start_Date'].widget = forms.DateInput(attrs={'type': 'date','class':'form-control'})
        self.fields['Accreditation_End_Date'].widget = forms.DateInput(attrs={'type': 'date','class':'form-control'})