import os

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "supersecret")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "jwtsecret")
    MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/vaccination_portal")
    JWT_ACCESS_TOKEN_EXPIRES = 3600  # 1 hour
    