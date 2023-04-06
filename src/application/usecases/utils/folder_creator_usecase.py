
import os

from src.application.usecases.interfaces import GenericUseCase

from src.application.utils.error_handling_utils import ErrorHandlingUtils


class FolderCreator(GenericUseCase):
    def __init__(self,folder_path: str) -> None:
        self.folder_path = folder_path
        

    def execute(self):
        try:
            os.makedirs(self.folder_path, exist_ok=True)
        except Exception as exception:
            raise ErrorHandlingUtils.application_error("Error: No se a podido crear la carpeta", exception)
