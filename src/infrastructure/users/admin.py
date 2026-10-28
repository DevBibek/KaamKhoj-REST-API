from django.contrib import admin

from .models import Company, JobSeeker, User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display =(
            "email",
            "role"
    )

@admin.register(JobSeeker)
class JobSeekerAdmin(admin.ModelAdmin):
    list_display = (
            "id",
            "full_name",
            "phone_number",
            "address",
            "skills",
            "education",
            "experience",
            "resume",
            "created_at",
            "updated_at"
        )
    
    
@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display=(
            "id",
            "company_name",
            "description",
            "location",
            "website",
            "phone",
            "verification_status",
            "created_at",
            "updated_at"
        )
    