from tokenize import String
import typing
from fastapi import UploadFile
import pandas as pd

from src.application.usecases.interfaces import GenericUseCase
from src.application.utils.error_handling_utils import ErrorHandlingUtils
from src.domain.dog_fact import DogFactEntity


class TransformFileToDataFrameUseCaseTest(unittest.TestCase):
    def __init__(self,fileUpload: UploadFile, sheet_name: str) -> None:
        self.fileUpload = fileUpload
        self.sheet_name = sheet_name

    def execute(self) -> String:
        try:
            df = pd.read_csv(self.fileUpload.file,self.sheet_name.file)

            return "Archivo Creado en la ruta"
        except Exception as exception:
            raise ErrorHandlingUtils.application_error("No se puede obtener el dataframe del archivo excel cargado", exception)
