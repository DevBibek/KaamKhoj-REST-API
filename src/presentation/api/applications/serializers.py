from rest_framework import serializers

from infrastructure.applications.models import Application

# from infrastructure.users.models import JobSeeker


class ApplicationSerializer(serializers.ModelSerializer):
    jobseeker = serializers.CharField(
        read_only = True,
        source = "jobseeker.full_name"
    )
    cover_letter = serializers.CharField(required = True,error_messages = {
        "required":"Cover letter is required"
    })
    
    class Meta:
        model = Application
        fields = (
            'id',
            "jobseeker",
            "job",
            "cover_letter" ,
            "status",
            "created_at",
            "updated_at",
        )
        read_only_fields = (
            "jobseeker",
            "status",
            "created_at",
            "updated_at"
        )
        
class ApplicationListSerializer(serializers.ModelSerializer):
    job_title = serializers.ReadOnlyField(source = "job.title")
    class Meta:
        model = Application
        fields = (
            "id",
            "job",
            "job_title",
            "status"
        )
        

class UpdateApplicationStatusSerializers(serializers.ModelSerializer):
    status = serializers.ChoiceField(
        choices=[
            "PENDING",
            "REVIEWING",
            "ACCEPTED",
            "REJECTED",
        ]
    )
    class Meta:
        model = Application
        fields = ["status"]