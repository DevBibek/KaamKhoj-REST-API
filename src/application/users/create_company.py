from domain.users.company import Company


class CreateCompany:
    def __init__(self, repository):
        self.repository = repository

    def execute(self, data, user):

        if user.role != user.Role.COMPANY:
            raise ValueError(
            "Only company role user can create company profile."
            )
            
        if self.repository.exists_by_user(user):
            raise ValueError("You allreday have a company profile.")
        company = Company(
            user=user,
            company_name=data["company_name"],
            description=data["description"],
            location=data["location"],
            phone=data["phone"],
            website=data.get("website"),
        )

        return self.repository.save(company)