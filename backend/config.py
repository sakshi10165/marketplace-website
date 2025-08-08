from pydantic_settings import BaseSettings
from typing import List
import os
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    # Database
    database_url: str = os.getenv("DATABASE_URL", "postgresql://neondb_owner:npg_N4c2zJbKeXOo@ep-old-frog-a12uhaff-pooler.ap-southeast-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require")
    # JWT
    secret_key: str = os.getenv("SECRET_KEY", "your-secret-key-here")
    algorithm: str = os.getenv("ALGORITHM", "HS256")
    access_token_expire_minutes: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
    
    # Application
    debug: bool = os.getenv("DEBUG", "True").lower() == "true"
    allowed_hosts: List[str] = ["https://marketplace-website-paav.onrender.com"]
    
    class Config:
        env_file = ".env"

settings = Settings() 