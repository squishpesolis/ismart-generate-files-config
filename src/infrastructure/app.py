
import os
from fastapi import FastAPI
from injector import Injector, SingletonScope
from fastapi_injector import attach_injector

from src.adapter.api.cat_facts import cat_facts_controllers as cat_facts_controller
from src.adapter.api.dog_facts import dog_facts_controllers as dog_facts_controller
from src.adapter.api.config_file_facts import grupos_config_file_facts_controllers as grupos_config_file_facts_controllers
from src.adapter.api.config_file_facts import generate_config_files_facts_controllers as generate_config_files_facts_controllers
from src.adapter.spi.db.db_connection import DbConnection
from src.adapter.spi.http.http_connection import HttpConnection
from src.adapter.spi.repositories_factory import RepositoriesFactory
from src.domain.configuration_entity import ConfigurationEntity
from src.infrastructure.config_mapper import ConfigurationMapper

config: ConfigurationEntity = ConfigurationMapper(os.getenv("ENV", "dev")).get_config()
db_connection: DbConnection = DbConnection(config)
http_connection: HttpConnection = HttpConnection()
repositories_factory = RepositoriesFactory(config, db_connection, http_connection)


def create_app(injector: Injector) -> FastAPI:
    app: FastAPI = FastAPI()

    app.include_router(dog_facts_controller.router, prefix="/api/v1/dogs", tags=["dogs"])
    app.include_router(cat_facts_controller.router, prefix="/api/v1/cats", tags=["cats"])
    app.include_router(grupos_config_file_facts_controllers.router, prefix="/api/v1/grupos", tags=["grupos"])
    app.include_router(generate_config_files_facts_controllers.router, prefix="/api/v1/configuraciones", tags=["configuraciones"])

    injector.binder.bind(RepositoriesFactory, to=repositories_factory, scope=SingletonScope)

    attach_injector(app, injector)
    return app
