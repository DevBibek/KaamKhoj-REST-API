from django.contrib import admin

from infrastructure.jobs.models import Job


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = (
        "company",
        "title",
        "description",
        "salary","location",
        "is_active",
        "created_at",
        "updated_at")