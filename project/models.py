from django.db import models
from accuont.models import Depatment,User
# Create your models here.
class Institution(models.Model):
    name = models.CharField('Name Institution', max_length=50)
    #created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    def __str__(self):
        return self.name
class Program(models.Model):
    name = models.CharField('Name Program', max_length=50)
    institution = models.ForeignKey(Institution,related_name='program', on_delete=models.CASCADE)
    def __str__(self):
        return self.name

class Quality_standards(models.Model):
    name = models.CharField('اسم المعيار', max_length=50)
    descripe = models.CharField('وصف المعيار',max_length=250,null=True,blank=True)
    
class AccStatus(models.Model):
    institution = models.ForeignKey(Institution,verbose_name='اسم المؤسسة',blank=True, null=True,on_delete=models.CASCADE)
    program = models.ForeignKey(Program,verbose_name='اسم القسم', on_delete=models.CASCADE)
    Accrediting_Body = models.CharField(verbose_name='نوع التقديم',max_length=50,choices=(('محلي','محلي'),('دولي','دولي')),blank=True, null=True)
    Accreditation_Status = models.CharField(verbose_name='حالة الاعتماد',max_length=50,choices=(('معتمد','معتمد'),('غير معتمد','غير معتمد'),('متقدمة للاعتماد','متقدمة للاعتماد'),('غير متقدمة للاعتماد','غير متقدمة للاعتماد')),blank=True, null=True)
    Accreditation_Start_Date = models.DateField(verbose_name='تاريخ بداية الاعتماد',auto_now=False, auto_now_add=False,blank=True, null=True)
    Accreditation_End_Date = models.DateField(verbose_name='تاريخ نهاية الاعتماد',auto_now=False, auto_now_add=False,blank=True, null=True)
    Compliance_Level = models.CharField(verbose_name='مستوى الامتثال',choices=(('High','High'),('Medium','Medium'),('Low','Low')),max_length=50,blank=True, null=True)
    Accreditation_Criteria = models.CharField(verbose_name='معايير الاعتماد',choices=(('A','A'),('B','B'),('C','C')),max_length=50,blank=True, null=True)
    # Progress_Towards_Accreditation = models.FileField(upload_to='Progress/Towards/Accreditation', max_length=100,blank=True, null=True)
    Self_Assessment_Reports = models.FileField(verbose_name='تقرير التقييم الذاتي',upload_to='Self-Assessment/Reports', max_length=100,blank=True, null=True)
    Site_Visit_Reports = models.FileField(verbose_name='تقرير زيادة الموقع',upload_to='Site/Visit/Reports', max_length=100,blank=True, null=True)
    Supporting_Documentation = models.FileField(verbose_name='التوثيق الداعم',upload_to='Supporting/Documentation', max_length=100,blank=True, null=True)
    
    

class AccStatusMain(models.Model):
    account = models.ForeignKey(User,verbose_name='اسم القسم',related_name='acc_main', on_delete=models.CASCADE)
    Accrediting_Body = models.CharField(verbose_name='نوع التقديم',max_length=50,choices=(('محلي','محلي'),('دولي','دولي')),blank=True, null=True)
    Accreditation_Status = models.CharField(verbose_name='حالة الاعتماد',max_length=50,choices=(('معتمد','معتمد'),('غير معتمد','غير معتمد'),('متقدمة للاعتماد','متقدمة للاعتماد'),('غير متقدمة للاعتماد','غير متقدمة للاعتماد')),blank=True, null=True)
    # Accreditation_Start_Date = models.DateField(verbose_name='تاريخ بداية الاعتماد',auto_now=False, auto_now_add=False,blank=True, null=True)
    # Accreditation_End_Date = models.DateField(verbose_name='تاريخ نهاية الاعتماد',auto_now=False, auto_now_add=False,blank=True, null=True)
    # Compliance_Level = models.CharField(verbose_name='مستوى الامتثال',choices=(('High','High'),('Medium','Medium'),('Low','Low')),max_length=50,blank=True, null=True)
    # Accreditation_Criteria = models.CharField(verbose_name='معايير الاعتماد',choices=(('A','A'),('B','B'),('C','C')),max_length=50,blank=True, null=True)
    # Progress_Towards_Accreditation = models.FileField(upload_to='Progress/Towards/Accreditation', max_length=100,blank=True, null=True)
    # Self_Assessment_Reports = models.FileField(verbose_name='تقرير التقييم الذاتي',upload_to='Self-Assessment/Reports', max_length=100,blank=True, null=True)
    # Site_Visit_Reports = models.FileField(verbose_name='تقرير زيادة الموقع',upload_to='Site/Visit/Reports', max_length=100,blank=True, null=True)
    # Supporting_Documentation = models.FileField(verbose_name='التوثيق الداعم',upload_to='Supporting/Documentation', max_length=100,blank=True, null=True)
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True,blank=True, null=True)
    
class StandardAcc(models.Model):
    acc_status_main = models.ForeignKey(AccStatusMain,related_name='stan_acc', on_delete=models.CASCADE)
    quality_standards = models.ForeignKey(Quality_standards,on_delete=models.CASCADE)
    ratio = models.IntegerField(default=0)
    
class College_activities(models.Model):
    acc_status_main = models.ForeignKey(AccStatusMain,related_name='col_active', on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    year = models.IntegerField()
    type_activity = models.CharField(max_length=45,blank=True, null=True) 
    seasson = models.CharField(max_length=15)