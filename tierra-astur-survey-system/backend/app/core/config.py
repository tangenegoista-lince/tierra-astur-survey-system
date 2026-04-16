from pydantic import BaseSettings, Field

class Settings(BaseSettings):
    # API
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Tierra Astur Survey Card Data Extraction System"

    # Database
    POSTGRES_SERVER: str = Field(default="localhost")
    POSTGRES_USER: str = Field(default="postgres")
    POSTGRES_PASSWORD: str = Field(default="postgres")
    POSTGRES_DB: str = Field(default="tierra_astur_surveys")
    POSTGRES_PORT: str = Field(default="5432")

    @property
    def SQLALCHEMY_DATABASE_URI(self) -> str:
        return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

    # OCR/OMR
    TESSERACT_CMD: str = Field(default="/usr/bin/tesseract")
    OCR_TIMEOUT: int = Field(default=30)  # seconds

    # File upload
    UPLOAD_DIR: str = Field(default="./uploads")
    MAX_UPLOAD_SIZE: int = Field(default=10 * 1024 * 1024)  # 10 MB

    # Security
    SECRET_KEY: str = Field(default="CHANGE_THIS_IN_PRODUCTION")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=60 * 24 * 8)  # 8 days

    class Config:
        case_sensitive = True
        env_file = ".env"

settings = Settings()
