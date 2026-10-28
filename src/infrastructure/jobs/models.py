from django.db import models

from infrastructure.users.models import Company


class Job(models.Model):
    
    company = models.ForeignKey(Company,on_delete=models.CASCADE,related_name="job")
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=200)
    salary = models.DecimalField(max_digits=10,decimal_places=2)
    location = models.CharField(max_length=100)
    is_active = models.BooleanField(default= True)
    created_at = models.DateTimeField(auto_now_add= True)
    updated_at = models.DateTimeField(auto_now=True)
    
    
    def __str__(self):
        return self.title
    
    
