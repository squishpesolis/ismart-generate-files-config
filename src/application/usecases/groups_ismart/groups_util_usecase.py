
import yaml
import os.path

from src.application.utils.error_handling_utils import ErrorHandlingUtils

from src.application.usecases.utils.string_util_usecase import StringUtilUseCase



class GroupsUtilUseCase():
    def __init__(self) -> None:
        pass
        

    @staticmethod
    def build_unique_id(unique:str):
        new_unique_id = StringUtilUseCase.convert_string_lower_case(unique)
        new_unique_id = StringUtilUseCase.replace_string(new_unique_id," ","_")
        return new_unique_id


