from pydantic import Field
from pydantic_settings import BaseSettings
from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import sessionmaker


class Settings(BaseSettings):
    db_host: str = Field("127.0.0.1", env="DB_HOST")
    db_port: int = Field(3306, env="DB_PORT")
    db_user: str = Field("root", env="DB_USER")
    db_password: str = Field("password", env="DB_PASSWORD")
    db_name: str = Field("sigea", env="DB_NAME")
    db_driver: str = Field("pymysql", env="DB_DRIVER")
    db_echo: bool = Field(False, env="DB_ECHO")

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
    }

    @property
    def database_url(self) -> str:
        return URL.create(
            drivername=f"mysql+{self.db_driver}",
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
    future=True,
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
