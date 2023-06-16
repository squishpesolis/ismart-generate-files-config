import pandas as pd
import json 
from src.application.utils.error_handling_utils import ErrorHandlingUtils
from src.application.usecases.interfaces import GenericUseCase



class TransformDictToJsonUseCase(GenericUseCase):
    def __init__(self,datos) -> None:
        self.datos = datos

    def execute(self) -> str:
        try:
            return json.dumps(self.datos) 
        except Exception as exception:
            raise ErrorHandlingUtils.application_error("Un erro ocurrio a convertir el Dict en JSON", exception)
