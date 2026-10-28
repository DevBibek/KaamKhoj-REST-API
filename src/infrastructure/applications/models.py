from django.db import models

from infrastructure.jobs.models import Job
from infrastructure.users.models import JobSeeker


class Application(models.Model):
    class Status(models.TextChoices):
        PENDING = "PENDING","pending"
        REVIEWING = "REVIEWING","reviewing"
        ACCEPTED = "ACCEPTED","accepted"
        REJECTED = "REJECTED","rejected"
        
    jobseeker = models.ForeignKey(JobSeeker,on_delete=models.CASCADE,related_name="application")
    job = models.ForeignKey(Job,on_delete=models.CASCADE,related_name="applications")
    cover_letter = models.TextField(blank=True)
    status = models.CharField(
        max_length=20,
        choices= Status.choices,
        default= Status.PENDING
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.jobseeker} - {self.job}"