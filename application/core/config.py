from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int
    database_url: str


class Config:
    env_file = ".env"


settings = Settings(secret_key='791376c27ad90e5594339a004d26ef259e8faaba', algorithm='HS256', access_token_expire_minutes=120, database_url="postgresql://superuserp:jkl555@localhost/quickborrows")
