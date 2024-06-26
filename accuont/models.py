from django.db import models
from django.contrib.auth.models import AbstractUser,UserManager
# Create your models here.

class ManagerUSer(UserManager):
    
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("The Email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        return self.create_user(email, password, **extra_fields)
        

class User(AbstractUser):
    type_enterprise = models.CharField(max_length=50,choices=(('علوم طبية','علوم طبية'),('علوم تطبيقية','علوم تطبيقية'),('علوم انسانية','علوم انسانية')),blank=True, null=True)
    company_name = models.CharField(max_length=50)
    point = models.IntegerField(default=0,null=True,blank=True)
    students = models.IntegerField(default=0)
    staff = models.IntegerField(default=0)
    
    manager = ManagerUSer
    def __str__(self):
        if self.is_superuser:
            return self.username
        return self.company_name    
class Depatment(models.Model):
    name = models.CharField(max_length=50)
    account = models.ForeignKey(User, on_delete=models.CASCADE)
    
