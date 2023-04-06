
import os
from pathlib import Path

from src.application.utils.error_handling_utils import ErrorHandlingUtils
from src.domain.configuration_entity import ConfigurationEntity
from src.infrastructure.config_mapper import ConfigurationMapper

config: ConfigurationEntity = ConfigurationMapper(os.getenv("ENV", "dev")).get_config()

class PathsIsmartUseCase():
    def __init__(self) -> None:
    
        self.path_root = os.path.join(Path(config.root_path), 'ISMART')


    def get_root_path(self):
        try:

            return self.path_root
        except Exception as exception:
            raise ErrorHandlingUtils.application_error("Error: al obtener el root path", exception)


    def get_path_files_yaml_generates(self):
        return os.path.join(self.get_root_path(), "yaml_generados")


    def get_root_path_ismar_home_assintant(self):
        return os.path.join(self.get_path_files_yaml_generates(),'config', 'ismart')


    def get_root_path_ismar_home_assintant_principal(self):
        try:
         return os.path.join(self.get_root_path_ismar_home_assintant(), "principal")
        except Exception as exception:
            raise ErrorHandlingUtils.application_error("Error: al obtener el get_root_path_ismar_home_assintant_principal", exception)


    def path_join_two_directores(dir1,dir2):
        return os.path.join(dir1,dir2)


    def path_join_any_directores(paths):
        return os.path.join(*paths)


    