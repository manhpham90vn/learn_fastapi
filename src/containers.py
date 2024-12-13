import os

from dependency_injector import containers, providers
from dotenv import load_dotenv
from sqlalchemy.ext.declarative import declarative_base

load_dotenv()


class Container(containers.DeclarativeContainer):
    config = providers.Configuration()

    # env
    data_base_url = providers.Singleton(lambda: os.getenv("SQLALCHEMY_DATABASE_URI"))
    secret_key = providers.Singleton(lambda: os.getenv("SECRET_KEY"))
    algorithm = providers.Singleton(lambda: os.getenv("ALGORITHM"))
    access_token_expire_minutes = providers.Singleton(
        lambda: int(os.getenv("ACCESS_TOKEN_EXPIRE", 30))
    )

    # base
    get_base = providers.Singleton(lambda: declarative_base())


container = Container()
