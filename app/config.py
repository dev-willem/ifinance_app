import os
from urllib.parse import quote_plus
from dotenv import load_dotenv

load_dotenv()


def env(key: str, default=None):
    """Helper para acessar variáveis de ambiente."""
    return os.getenv(key, default)


class Config:
    """Configuração base da aplicação."""

    SECRET_KEY: str = env("SECRET_KEY", "dev-secret-key-change-in-production")

    DB_HOST: str = env("DB_HOST", "localhost")
    DB_PORT: str = env("DB_PORT", "3306")
    DB_NAME: str = env("DB_NAME", "finance_db")
    DB_USER: str = env("DB_USER", "root")
    DB_PASSWORD: str = env("DB_PASSWORD", "")

    SQLALCHEMY_TRACK_MODIFICATIONS: bool = False

    DEBUG: bool = env("FLASK_DEBUG", "false").lower() == "true"

    @classmethod
    def build_database_uri(cls) -> str:
        """Constrói a URI de conexão com o banco."""
        user = quote_plus(cls.DB_USER)
        password = quote_plus(cls.DB_PASSWORD)

        return (
            f"mysql+pymysql://{user}:{password}"
            f"@{cls.DB_HOST}:{cls.DB_PORT}/{cls.DB_NAME}"
        )

    SQLALCHEMY_DATABASE_URI: str = env("DATABASE_URL") or build_database_uri()

    @classmethod
    def validate_database_config(cls) -> None:
        """Valida variáveis essenciais de banco."""
        required = ["DB_HOST", "DB_PORT", "DB_NAME", "DB_USER"]

        missing = [var for var in required if not env(var)]

        if missing:
            raise ValueError(
                f"Variáveis obrigatórias ausentes: {', '.join(missing)}"
            )


class DevelopmentConfig(Config):
    """Configuração de desenvolvimento."""

    DEBUG = True


class ProductionConfig(Config):
    """Configuração de produção."""

    DEBUG = False


config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig,
}