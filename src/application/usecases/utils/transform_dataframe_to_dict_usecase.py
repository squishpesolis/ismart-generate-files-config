import pandas as pd
from src.application.utils.error_handling_utils import ErrorHandlingUtils


from src.application.usecases.interfaces import GenericUseCase
from src.domain.dog_fact import DogFactEntity


class TransformDataFrameToDictUseCase(GenericUseCase):
    def __init__(self,df: pd.DataFrame) -> None:
        self.df = df

    def execute(self) -> pd.DataFrame:
        try:

            if self.df.empty:
                raise ErrorHandlingUtils.application_error("El dataframe no contiene datos")
    
            return self.df.to_dict('records')
        except Exception as exception:
            raise ErrorHandlingUtils.application_error("Un erro ocurrio a convertir el Datafram en Dict", exception)
