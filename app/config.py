from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    aws_s3_bucket_name: str = "demo-bucket"
    openai_api_key: str

    class Config:
        env_file = ".env"  # Optional if you're using a .env file

settings = Settings()
