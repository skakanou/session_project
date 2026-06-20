import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "default_secret_key")

    SQLALCHEMY_DATABASE_URI ="mysql+pymysql://root:%40dmin@127.0.0.1:3306/session_project"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "dev_jwt_secret_key")
    JWT_ALGORITHM = "HS256"