

from src.application.utils.error_handling_utils import ErrorHandlingUtils


class StringUtilUseCase():
    def __init__(self) -> None:
        pass
        

    @staticmethod
    def convert_string_lower_case(text: str):
        return text.lower()
    
    @staticmethod
    def replace_string(text: str, old_caracter: str, new_caracter: str):
        return text.replace(old_caracter, new_caracter)
    


    

    
    

