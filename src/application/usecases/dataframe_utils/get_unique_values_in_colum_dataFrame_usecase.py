
import pandas as pd
from src.application.usecases.interfaces import GenericUseCase
from src.application.utils.error_handling_utils import ErrorHandlingUtils


class GetUniqueValuesInColunmDataFrameUseCase(GenericUseCase):
    def __init__(self, df: pd.DataFrame, column_to_filter) -> None:
        self.df = df
        self.column_to_filter = column_to_filter

    def execute(self) -> list:
        try:
            return self.df[self.column_to_filter].unique()
            
        except Exception as exception:
            raise ErrorHandlingUtils.application_error("Error al filtrar el DataFrame: ", exception)

