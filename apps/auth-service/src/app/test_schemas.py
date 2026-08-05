from app.schemas.auth import UserRegisterRequest

user = UserRegisterRequest(
    email="john@example.com",
    password="MyPassword123",
    full_name="John Doe",
)

print(user)
print(user.model_dump())