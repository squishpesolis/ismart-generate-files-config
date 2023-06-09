from tokenize import String
import typing
from fastapi import UploadFile
import pandas as pd
from io import BytesIO

from src.application.usecases.interfaces import GenericUseCase
from src.application.utils.error_handling_utils import ErrorHandlingUtils
from src.domain.dog_fact import DogFactEntity


class TransformFileToDataFrameUseCase(GenericUseCase):
    def __init__(self,fileUpload: UploadFile, sheet_name: str) -> None:
        self.fileUpload = fileUpload
        self.sheet_name = sheet_name

    async def execute(self) -> pd.DataFrame:
        try:

         
            contents = self.fileUpload.file.read()
            data = BytesIO(contents)
            df = pd.read_excel(data,str(self.sheet_name))
            data.close()
            return df
        except Exception as exception:
            print(exception)
            raise ErrorHandlingUtils.application_error("No se puede obtener el dataframe del archivo excel cargado", exception)
