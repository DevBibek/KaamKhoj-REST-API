from .models import Application


class ApplicationRepository:
    def save(self,application):
        print("*************APPLICATIN REPOSITORY *************")
        return Application.objects.create(
            job = application.job,
            cover_latter = application.cover_latter,
            status = application.status,
            created_at = application.created_at,
            updaed_at = application.updated_at            
        )