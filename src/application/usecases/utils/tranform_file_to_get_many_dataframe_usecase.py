from tokenize import String
import typing
from fastapi import UploadFile
import pandas as pd
from io import BytesIO

from src.application.usecases.interfaces import GenericUseCase
from src.application.utils.error_handling_utils import ErrorHandlingUtils
from src.domain.dog_fact import DogFactEntity


class TransformFileToGetManyDataFrameUseCase(GenericUseCase):
    def __init__(self,fileUpload: UploadFile, sheets_name) -> None:
        self.fileUpload = fileUpload
        self.sheets_name = sheets_name

    async def execute(self) -> pd.DataFrame:
        try:

         
            contents = self.fileUpload.file.read()
            data = BytesIO(contents)
            df = pd.read_excel(data,sheet_name=self.sheets_name)
            data.close()
            return df
        except Exception as exception:
            raise ErrorHandlingUtils.application_error("No se puede obtener el dataframe del archivo excel cargado", exception)
