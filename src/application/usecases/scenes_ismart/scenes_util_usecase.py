
import yaml
import os.path
import pandas as pd

from src.application.usecases.utils.string_util_usecase import StringUtilUseCase

from src.application.usecases.enums.names_columns_excel_ismart_configuration_enum import ColumnsNameExcelConfigISmart
from src.application.usecases.enums.name_column_df_scenes import NameColumnDfSceneEnum
from src.application.usecases.enums.entities_ismart_demos_enum import EntitiesIsmartDemosEnum
from src.application.usecases.enums.domain_entities_ismart_enum import DomainEntitiesIsmartEnum


class ScenesUtilUseCase():
    def __init__(self) -> None:
        pass
        

    @staticmethod
    def build_dict_group_switch(df_entites: pd.DataFrame, name_scene: str,icon:str) -> dict:

        scene_object = {}

        if df_entites.empty:
            return scene_object
        
        scene_object = {
                'name': name_scene,
                'id': ScenesUtilUseCase.build_unique_id(name_scene),
                'icon': icon,
                'entities': {}
        }

        entities = {}
        for entity in df_entites:

            new_entity = {entity[NameColumnDfSceneEnum.entity.value]:entity[NameColumnDfSceneEnum.value_.value]}
            if entity[NameColumnDfSceneEnum.domain.value] == DomainEntitiesIsmartEnum.switch.value:
                print("Hacer algo para el sith")

            entities.update(new_entity)
     
        scene_object['entities'] = entities


        return scene_object
    
    @staticmethod
    def build_unique_id(unique:str):
        new_unique_id = StringUtilUseCase.convert_string_lower_case(unique)
        new_unique_id = StringUtilUseCase.replace_string(new_unique_id," ","_")
        return new_unique_id
    
    @staticmethod
    def build_df_empty_to_build_scenes():

        columnsName = [NameColumnDfSceneEnum.name_.value,
                       NameColumnDfSceneEnum.icon.value,
                       NameColumnDfSceneEnum.domain.value,
                       NameColumnDfSceneEnum.entity.value,
                       NameColumnDfSceneEnum.value_.value]
         
        return pd.DataFrame(columns=columnsName)