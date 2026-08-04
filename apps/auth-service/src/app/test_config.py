from app.core.config import settings

print("Application")
print(settings.app.name)
print(settings.app.env)
print(settings.app.version)

print()

print("Database")
print(settings.database.host)
print(settings.database.port)
print(settings.database.db)

print()

print("Redis")
print(settings.redis.host)

print()

print("JWT")
print(settings.jwt.algorithm)