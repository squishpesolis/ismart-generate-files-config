
import yaml
import os.path
import pandas as pd

from src.application.utils.error_handling_utils import ErrorHandlingUtils

from src.application.usecases.utils.string_util_usecase import StringUtilUseCase
from src.application.usecases.enums.names_columns_excel_ismart_configuration_enum import ColumnsNameExcelConfigISmart
from src.application.usecases.enums.name_column_df_group import NameColumnDfGroupEnum
from src.application.usecases.enums.name_column_df_group_path_files_yaml import NameColumnDfGroupPathFulesEnum
from src.application.usecases.enums.entities_ismart_demos_enum import EntitiesIsmartDemosEnum

class GroupsUtilUseCase():
    def __init__(self) -> None:
        pass
        

    @staticmethod
    def build_unique_id(unique:str):
        new_unique_id = StringUtilUseCase.convert_string_lower_case(unique)
        new_unique_id = StringUtilUseCase.replace_string(new_unique_id," ","_")
        return new_unique_id
    
    @staticmethod
    def build_dict_group_switch(df: pd.DataFrame, name_group: str, unique_id:str) -> dict:

        data = {}

        if df.empty:
            return data


        data = {
            'switch': [
                {
                    'platform': 'group',
                    'name': name_group,
                    #'unique_id': unique_id,
                    'entities': []
                }
            ]
        }

        for final_id in df[ColumnsNameExcelConfigISmart.final_id.value]:

            data['switch'][0]['entities'].append(final_id.replace(" ", ""))


        return data

    @staticmethod
    def build_dict_group_sensor(df: pd.DataFrame, name_group: str, unique_id:str, type: str) -> dict:

        #data = {}
        data = []

        if df.empty:
            return data


        data = [
                {
                    'platform': 'group',
                    'type': type,
                    'name': name_group,
                    'unique_id': unique_id,
                    'entities': []
                }
        ]
        



        for final_id in df[ColumnsNameExcelConfigISmart.final_id.value]:

            #data['sensor'][0]['entities'].append(final_id.replace(" ", ""))
            data[0]['entities'].append(final_id.replace(" ", ""))

        return data
    

    @staticmethod
    def build_dict_group_cover(df: pd.DataFrame, name_group: str, unique_id:str) -> dict:

        #data = {}
        data = []
        if df.empty:
            return data


        """ data = {
            'cover': [
                {
                    'platform': 'group',
                    'name': name_group,
                    'unique_id': unique_id,
                    'entities': []
                }
            ]
        } """

        data = [
            {
                'platform': 'group',
                'name': name_group,
                'unique_id': unique_id,
                'entities': []
            }
        ]

        for final_id in df[ColumnsNameExcelConfigISmart.final_id.value]:

            #data['cover'][0]['entities'].append(final_id.replace(" ", ""))
            data[0]['entities'].append(final_id.replace(" ", ""))


        return data
    
    @staticmethod
    def build_df_empty_to_build_groups():

        columnsName = [NameColumnDfGroupEnum.title.value,
                       NameColumnDfGroupEnum.entity.value,
                       NameColumnDfGroupEnum.name_.value,
                       NameColumnDfGroupEnum.icon.value,
                       NameColumnDfGroupEnum.tap_action.value]
         
        return pd.DataFrame(columns=columnsName)
    
    @staticmethod
    def build_df_empty_to_build_paths_files_yaml_groups() -> pd.DataFrame:

        columnsName = [NameColumnDfGroupPathFulesEnum.name_.value,NameColumnDfGroupPathFulesEnum.path_.value,NameColumnDfGroupPathFulesEnum.domain_.value]
         
        return pd.DataFrame(columns=columnsName)
