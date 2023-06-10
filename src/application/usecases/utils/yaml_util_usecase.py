
import yaml
import os.path

from src.application.utils.error_handling_utils import ErrorHandlingUtils


class YamlUtilUseCase():
    def __init__(self) -> None:
        pass
        

    @staticmethod
    def save_file_yaml(path, datos: dict):
        try:
            #FolderCreator.execute(path)
            file=open(path,"w")
            yaml.dump(datos,file,sort_keys=False)
            file.close()
        except Exception as exception:
            print(exception)
            raise ErrorHandlingUtils.application_error("Error: no se pudo crear el archivo yaml", exception)

    def check_exist_file(path):
        os.path.isfile(path)
