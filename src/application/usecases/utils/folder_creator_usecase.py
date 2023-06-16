
import os

from src.application.usecases.interfaces import GenericUseCase

from src.application.utils.error_handling_utils import ErrorHandlingUtils


class FolderCreator(GenericUseCase):
    def __init__() -> None:
        pass
        
    @staticmethod
    def execute(folder_path):
        try:
            isExist = os.path.exists(folder_path)
            if not isExist:
                os.makedirs(folder_path)
        except Exception as exception:
            raise ErrorHandlingUtils.application_error("Error: No se a podido crear la carpeta", exception)
