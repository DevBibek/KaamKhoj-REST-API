from django.contrib import admin

from .models import Application

@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "jobseeker",
        "job",
        "cover_letter",
        "status",
        "created_at",
        "updated_at"
    ]
    


