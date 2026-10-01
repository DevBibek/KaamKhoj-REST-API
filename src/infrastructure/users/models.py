from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class Role(models.TextChoices):
        JOB_SEEKER ="JOB_SEEKER","Job Seeker"
        COMPANY = "COMPANY","Company"
    email = models.EmailField(unique= True)
    role = models.CharField(max_length=20,choices= Role.choices)
    USERNAME_FIELD = ("email")
    REQUIRED_FIELDS = ("username",)



from django.core.validators import RegexValidator


class JobSeeker(models.Model):
    user = models.OneToOneField(User,on_delete= models.CASCADE,related_name="jobseeker")
    full_name = models.CharField(max_length=100)
    phone_number = models.CharField(
        max_length=14,
        unique= True,
        validators = [RegexValidator(
            regex=r"^(?:\+977)?(?:96|97|98)\d{8}$",
            message= "Enter a valid nepali number"
        )])
    address= models.CharField(max_length=100)
    skills = models.TextField(max_length=100)
    education = models.CharField(max_length =100)
    experience = models.PositiveIntegerField(default=0)
    resume = models.FileField(
        upload_to= "resumes/",
        blank=True,
        null= True)
    created_at = models.DateTimeField(auto_now_add= True)
    updated_at = models.DateTimeField(auto_now= True)
    
    def __str__(self):
        return self.user.username
    
    
    

class Company(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name="company")
    company_name = models.CharField(max_length=100)
    description = models.TextField(blank= True)
    location = models.CharField(default="nepal")
    website = models.URLField(null= True ,blank=True)
    phone = models.CharField(
        max_length=14,
        validators =[
            RegexValidator(
                regex=r"^(?:\+977)?(?:96|97|98)\d{8}$",
            message= "Enter a valid nepali number"
        )])
    created_at = models.DateTimeField(auto_now_add= True)
    updated_at = models.DateTimeField(auto_now=True)
    
    
    def __str__(self):
        return self.company_name