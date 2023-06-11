from tokenize import String
import typing
import pandas as pd



from src.application.utils.error_handling_utils import ErrorHandlingUtils

from src.application.usecases.enums.names_columns_excel_ismart_configuration_enum import ColumnsNameExcelConfigISmart

class DataFrameUtilUseCase():
    def __init__(self) -> None:
        pass
        

    @staticmethod
    def get_value_dataframe_from_position_row_and_name_colum(position: int, colum_name: ColumnsNameExcelConfigISmart,df: pd.DataFrame, name_data_frame: str):
      
        if not colum_name.value in df.columns:
            raise Exception("Error: no existe Columna: " +colum_name.value + " en el Sheet : " + name_data_frame) 

        if position > df.shape[0]:
           raise Exception("Error: No existe una fila : " + str(position) + " en el Sheet : " + name_data_frame) 
        
        return df[colum_name.value].iloc[position]
 
