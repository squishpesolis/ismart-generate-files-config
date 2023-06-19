import typing
import pandas as pd
import numpy as np
import yaml
from src.application.usecases.interfaces import GenericUseCase
from src.application.utils.error_handling_utils import ErrorHandlingUtils

from src.application.usecases.utils.paths_usecase import PathsIsmartUseCase;
from src.application.usecases.utils.yaml_util_usecase import YamlUtilUseCase
from src.application.usecases.utils.folder_creator_usecase import FolderCreator

from src.application.usecases.enums.names_columns_excel_ismart_configuration_enum import ColumnsNameExcelConfigISmart
from src.application.usecases.enums.domain_entities_ismart_enum import DomainEntitiesIsmartEnum
from src.application.usecases.enums.name_column_df_scene import NameColumnDfSceneEnum
from src.application.usecases.enums.names_files_yamls_enum import NameFilesYamlsEnum

from src.application.usecases.scenes_ismart.scenes_util_usecase import ScenesUtilUseCase


class CreateScenesUseCase(GenericUseCase):
    def __init__(self, 
                 df_scenes_config: pd.DataFrame, 
                 dataframe_areas: pd.DataFrame,
                 dataframe_entites: pd.DataFrame,
                 configurar_con_entidades_demos: bool) -> None:
        
        self.df_scenes_config = df_scenes_config
        self.dataframe_areas = dataframe_areas
        self.dataframe_entites = dataframe_entites
        self.configurar_con_entidades_demos = configurar_con_entidades_demos
        paths_usecase: PathsIsmartUseCase = PathsIsmartUseCase()
        self.path_ismart_scenes = paths_usecase.get_root_path_ismar_home_assintant_principal_scenes()

       

    async def execute(self) -> pd.DataFrame:
        try:

            path_save_yaml = PathsIsmartUseCase.path_join_any_directores([self.path_ismart_scenes])
            FolderCreator.execute(path_save_yaml)

            df_scenes = ScenesUtilUseCase.build_df_empty_to_build_scenes()
            
                     
            scenes_config_unique = self.df_scenes_config


            dataframe_areas = self.dataframe_areas[(self.dataframe_areas[ColumnsNameExcelConfigISmart.Colocar_Area_en_Dashboard_Views.value] == 'SI')] 


            df_entities  = self.dataframe_entites
    


            #name_group = NameOfGroupEnum.lights.value
            name_file_yaml = NameFilesYamlsEnum.scenes.value + "ismart.yaml"
            

            for index, scene_config in scenes_config_unique.iterrows():

            
                icon_scene = scene_config[ColumnsNameExcelConfigISmart.icon_scenes.value]

                for index_aread, area in dataframe_areas.iterrows():
                    
                    
                    area_sub_zona = area[ColumnsNameExcelConfigISmart.Sub_Zona.value]


                    #name_scene_build = "Escena " + scene_config[ColumnsNameExcelConfigISmart.scenes.value] + " " + area_sub_zona
                    name_scene_build = scene_config[ColumnsNameExcelConfigISmart.scenes.value]

                    for domain in DomainEntitiesIsmartEnum:

                        df_entities_by_area_and_domain = pd.DataFrame()

                        df_entities_by_area_and_domain = df_entities[(df_entities[ColumnsNameExcelConfigISmart.areas.value] == area[ColumnsNameExcelConfigISmart.Sub_Zona.value] ) 
                                                                     #& (df_entities[ColumnsNameExcelConfigISmart.domain.value] == domain.value)
                                                                     ] 
                        
                     
                        filtered_values = np.where((df_entities[ColumnsNameExcelConfigISmart.areas.value]==area[ColumnsNameExcelConfigISmart.Sub_Zona.value]) & 
                                                   (df_entities[ColumnsNameExcelConfigISmart.domain.value] == domain.value))

                        df_entities_by_area_and_domain = df_entities.loc[filtered_values]
                        
                        if not df_entities_by_area_and_domain.empty:
                         
                          
                            
                            for index_entity, entity in df_entities_by_area_and_domain.iterrows() :

                                final_id = entity[ColumnsNameExcelConfigISmart.final_id.value]
                                

                                if domain.value in scenes_config_unique.columns:
                                    value_scene = scene_config[domain.value]

                                    row_df_scenes =  {
                                                        NameColumnDfSceneEnum.name_.value: name_scene_build, 
                                                        NameColumnDfSceneEnum.area.value: area_sub_zona, 
                                                        NameColumnDfSceneEnum.icon.value:icon_scene,
                                                        NameColumnDfSceneEnum.domain.value: domain.value, 
                                                        NameColumnDfSceneEnum.entity.value:final_id, 
                                                        NameColumnDfSceneEnum.value_.value:value_scene
                                                    }
                                    
                                    
                                    df_scenes = df_scenes.append(row_df_scenes, ignore_index=True)

            
            df_scenes = df_scenes.sort_values(by=[NameColumnDfSceneEnum.area.value, NameColumnDfSceneEnum.domain.value])
            
            df_groups_by_area = df_scenes.groupby([NameColumnDfSceneEnum.area.value, NameColumnDfSceneEnum.name_.value])
            
            list_scenes = []

            list_scenes_admin = self.build_dict_scenes_admin(df_scenes)

            list_scenes.extend(list_scenes_admin)

            for group_by_area in df_groups_by_area.groups:
                df_scenes_by_group = df_groups_by_area.get_group(group_by_area)

                name_scene = df_scenes_by_group[NameColumnDfSceneEnum.name_.value].iloc[0]
                id_scene = df_scenes_by_group[NameColumnDfSceneEnum.name_.value].iloc[0] + " " + df_scenes_by_group[NameColumnDfSceneEnum.area.value].iloc[0]
                icon = df_scenes_by_group[NameColumnDfSceneEnum.icon.value].iloc[0]


                scene_dict =ScenesUtilUseCase.build_scenes_dict(df_scenes_by_group,name_scene,id_scene,icon)
                list_scenes.append(scene_dict)
                
            YamlUtilUseCase.save_file_yaml(PathsIsmartUseCase.path_join_any_directores([path_save_yaml, name_file_yaml]),list_scenes )

            return df_scenes
        
        except Exception as exception:
            raise ErrorHandlingUtils.application_error("Error al crear el scenes", exception)


    def build_dict_scenes_admin(self, df_scenes: pd.DataFrame):
        list_scenes = []
        df_groups_by_name = df_scenes.groupby(NameColumnDfSceneEnum.name_.value)
        for group_by_name in df_groups_by_name.groups:
            df_scenes_by_name = df_groups_by_name.get_group(group_by_name)
            name_scene = df_scenes_by_name[NameColumnDfSceneEnum.name_.value].iloc[0]
            id_scene = df_scenes_by_name[NameColumnDfSceneEnum.name_.value].iloc[0] + " admin"
            icon = df_scenes_by_name[NameColumnDfSceneEnum.icon.value].iloc[0]
            scene_dict =ScenesUtilUseCase.build_scenes_dict(df_scenes_by_name,name_scene,id_scene,icon)
            list_scenes.append(scene_dict)
        
        return list_scenes
        
  
