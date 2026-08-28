from app.schemas.auth_schema import UserRegisterRequest

user = UserRegisterRequest(
    company_name="Test Company",
    company_slug="test-company",
    email="john@example.com",
    password="MyPassword123",
    full_name="John Doe",
)

print(user)
print(user.model_dump())
