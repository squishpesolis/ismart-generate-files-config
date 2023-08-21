

from src.application.utils.error_handling_utils import ErrorHandlingUtils
import pyfiglet

class StringUtilUseCase():
    def __init__(self) -> None:
        pass
        

    @staticmethod
    def convert_string_lower_case(text: str):
        return text.lower()
    
    @staticmethod
    def replace_string(text: str, old_caracter: str, new_caracter: str):
        return text.replace(old_caracter, new_caracter)
    
    @staticmethod
    def tranform_string_to_slug(text: str):
        text = text.replace(" ", "_")
        text = text.replace("-", "_")
        return text.lower()
    
    @staticmethod
    def generate_string_pyfiglet(text: str, fuente: str):
        result = pyfiglet.figlet_format(text, font = fuente )
        return result
    
    @staticmethod
    def create_abbreviation(word: str, num_letter: int):
        result = word
        phrases = word.split()
        
        if len(phrases) >= 2:
            result = phrases[0][0:num_letter] + "." + " "+ "".join([str(elem) for elem in phrases[1:]])
            return result
        
        return result


    

    
    

