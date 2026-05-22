from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import sessionmaker
from models import Base


class Settings(BaseSettings):
    db_host: str = Field("localhost", env="DB_HOST")
    db_port: int = Field(3306, env="DB_PORT")
    db_user: str = Field("root", env="DB_USER")
    db_password: str = Field("password", env="DB_PASSWORD")
    db_name: str = Field("sigea", env="DB_NAME")
    db_driver: str = Field("pymysql", env="DB_DRIVER")
    db_echo: bool = Field(False, env="DB_ECHO")
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )

    secret_key: str = Field("ChaveJwt", env="SECRET_KEY")
    jwt_algorithm: str = Field("decoderAlg", env="JWT_ALGORITHM")
    access_token_expire_minutes: int = Field(60, env="ACCESS_TOKEN_EXPIRE_MINUTES")

    @property
    def database_url(self) -> str:
        return URL.create(
            drivername=f"mysql+pymysql",
            username=self.db_user,
            password=self.db_password,
            host=self.db_host,
            port=self.db_port,
            database=self.db_name,
            query={"charset": "utf8mb4"}
        )


settings = Settings()

engine = create_engine(
    settings.database_url,
    echo=settings.db_echo,
    future=True,
    pool_pre_ping=True,
)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False,
)


def get_db():
    """Dependency para injetar sessão do banco nas rotas"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    Base.metadata.create_all(bind=engine)