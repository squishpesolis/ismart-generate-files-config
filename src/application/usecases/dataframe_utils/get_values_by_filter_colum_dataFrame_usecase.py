from asyncio.windows_events import NULL
import pandas as pd

from src.application.usecases.enums.operations_dataframe_filter_enum import OperationDataFrameFilter;

from src.application.usecases.interfaces import GenericUseCase
from src.application.utils.error_handling_utils import ErrorHandlingUtils


class GetValuesByFilterColunmDataFramwUseCase(GenericUseCase):
    def __init__(self, df: pd.DataFrame, column_to_filter, value_to_filter, operacion: OperationDataFrameFilter) -> None:
        self.df = df
        self.column_to_filter = column_to_filter
        self.value_to_filter = value_to_filter
        self.operacion = operacion

    def execute(self) -> pd.DataFrame:
        try:

            data_frame_result: any
            if self.validaciones():
                ErrorHandlingUtils.application_error("Error al filtrar el DataFrame", self.validaciones())
            

            if self.operacion == OperationDataFrameFilter.EQUAL:
                data_frame_result =  self.df[self.df[self.column_to_filter] == self.value_to_filter] 

            if self.operacion == OperationDataFrameFilter.GREATER_THAN:
                data_frame_result =  self.df[self.df[self.column_to_filter] > self.value_to_filter]

            return data_frame_result
            
        except Exception as exception:
            raise ErrorHandlingUtils.application_error("Error al filtrar el DataFrame: ", exception)

    def validaciones(self) -> str:
        errores = ""

        if self.df.empty:
                errores = errores + "No se puede filtrar un DataFrame Vacio"
        
        if not self.column_to_filter: 
               errores = errores + "Se debe especificar, una column_to_filtera para filtrar "

        if not self.value_to_filter: 
               errores = errores + "Se debe especificar, un valor para filtar"

        return errores