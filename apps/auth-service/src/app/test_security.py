from app.core.security import (
    hash_password,
    verify_password,
)

password = "MyPassword123"

hashed = hash_password(password)

print(f"Original : {password}")
print(f"Hash     : {hashed}")

print()

print(
    "Correct Password:",
    verify_password(password, hashed),
)

print(
    "Wrong Password:",
    verify_password("wrong", hashed),
)
