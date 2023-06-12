from src.application.usecases.utils.string_util_usecase import StringUtilUseCase

class Utils_Views_Usecase():
    def __init__(self) -> None:
        pass
        
    
    @staticmethod
    def add_card_to_verticaL_stack(verticaL_stack:dict, card: dict):
        if not card:
            return verticaL_stack   
        verticaL_stack['cards'].append(card)
        return verticaL_stack
    
    @staticmethod
    def build_path_view(text:str):
        
        path = StringUtilUseCase.convert_string_lower_case(text)
        path = StringUtilUseCase.replace_string(path, " ", "_")
        return path