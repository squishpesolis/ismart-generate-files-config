import typing
import pandas as pd
import yaml
from src.application.usecases.interfaces import GenericUseCase
from src.application.utils.error_handling_utils import ErrorHandlingUtils

from src.application.usecases.utils.paths_usecase import PathsIsmartUseCase;
from src.application.usecases.utils.yaml_util_usecase import YamlUtilUseCase
from src.application.usecases.utils.folder_creator_usecase import FolderCreator

from src.application.usecases.enums.names_columns_excel_ismart_configuration_enum import ColumnsNameExcelConfigISmart
from src.application.usecases.enums.domain_entities_ismart_enum import DomainEntitiesIsmartEnum

from src.application.usecases.groups_ismart.groups_util_usecase import GroupsUtilUseCase

class CreateGroupsSwitchByLightUseCase(GenericUseCase):
    def __init__(self, df: pd.DataFrame) -> None:
        self.df = df
        paths_usecase: PathsIsmartUseCase = PathsIsmartUseCase()
        self.path_ismart_principal = paths_usecase.get_root_path_ismar_home_assintant_principal_grupos()

       

    def execute(self) -> pd.DataFrame:
        try:

            zonas = self.df[ColumnsNameExcelConfigISmart.zonas.value].unique()

            name_group = 'Grupo Switch '
            name_file_yaml = 'group_switch_'
            for zona in zonas:
               
                datos_demo = False

                # Filter domain switch by Zonas
                df_switches_by_zone = self.df[(self.df[ColumnsNameExcelConfigISmart.zonas.value] == zona) & (self.df[ColumnsNameExcelConfigISmart.domain.value] == 'switch')] 
                unique_id_switches_by_zone = GroupsUtilUseCase.build_unique_id(name_file_yaml + name_group +  zona)

                dict_df_switches_by_zone = GroupsUtilUseCase.build_dict_group_switch(df_switches_by_zone, name_group +  zona, unique_id_switches_by_zone, datos_demo)
               
                if dict_df_switches_by_zone:
  
                    name_file =  name_file_yaml + zona + '.yaml'
                    path_save_yaml = PathsIsmartUseCase.path_join_any_directores([self.path_ismart_principal,'Zonas', zona, 'Integraciones','grupos'])
                    
                    FolderCreator.execute(path_save_yaml)
                    
                    YamlUtilUseCase.save_file_yaml(PathsIsmartUseCase.path_join_any_directores([path_save_yaml, name_file]),dict_df_switches_by_zone )


                    ubicaciones = self.df[ColumnsNameExcelConfigISmart.ubicacion.value].unique()
       
                    for ubicacion in ubicaciones:

                        df_switches_by_ubicacion_and_zone = self.df[(self.df[ColumnsNameExcelConfigISmart.ubicacion.value] == ubicacion) & (self.df[ColumnsNameExcelConfigISmart.zonas.value] == zona) & (self.df[ColumnsNameExcelConfigISmart.domain.value] == DomainEntitiesIsmartEnum.switch.value) ] 
                        
                        unique_id_switches_ubicacion_and_zone = GroupsUtilUseCase.build_unique_id(name_file_yaml + name_group +  ubicacion)
                        dict_df_switches_ubicacion_and_zone = GroupsUtilUseCase.build_dict_group_switch(df_switches_by_ubicacion_and_zone,  name_group +  ubicacion, unique_id_switches_ubicacion_and_zone, datos_demo)
                       
                        if dict_df_switches_ubicacion_and_zone:
                            name_file_ubicacion =  name_file_yaml + ubicacion + '.yaml'
    
                            path_save_yaml_ubicacion = PathsIsmartUseCase.path_join_any_directores([self.path_ismart_principal,'Zonas', zona,'Ubicacion', ubicacion, 'Integraciones'])
                            FolderCreator.execute(path_save_yaml_ubicacion)
                            YamlUtilUseCase.save_file_yaml(PathsIsmartUseCase.path_join_any_directores([path_save_yaml_ubicacion, name_file_ubicacion]),dict_df_switches_ubicacion_and_zone )

                            areas = self.df[ColumnsNameExcelConfigISmart.areas.value].unique()

                            for area in areas:

                                df_switches_by_ubicacion_and_zone_and_area = self.df[(self.df[ColumnsNameExcelConfigISmart.ubicacion.value] == ubicacion) & (self.df[ColumnsNameExcelConfigISmart.zonas.value] == zona)  & (self.df[ColumnsNameExcelConfigISmart.areas.value] == area) & (self.df[ColumnsNameExcelConfigISmart.domain.value] == DomainEntitiesIsmartEnum.switch.value) ] 
                                unique_id_switches_ubicacion_and_zone_and_area = GroupsUtilUseCase.build_unique_id(name_file_yaml + name_group +  area)
                                dict_df_switches_ubicacion_and_zone_and_area = GroupsUtilUseCase.build_dict_group_switch(df_switches_by_ubicacion_and_zone_and_area,  name_group +  area, unique_id_switches_ubicacion_and_zone_and_area, datos_demo)
                                if dict_df_switches_ubicacion_and_zone_and_area:
                                    name_file_area = name_file_yaml+ area + '.yaml'
                                    list_path = [self.path_ismart_principal,'Zonas', zona,'Ubicacion', ubicacion, 'Areas',area,'Integraciones' ]
                                    path_save_yaml_area = PathsIsmartUseCase.path_join_any_directores(list_path)
                                    FolderCreator.execute(path_save_yaml_area)
                                    YamlUtilUseCase.save_file_yaml(PathsIsmartUseCase.path_join_any_directores([path_save_yaml_area, name_file_area]),dict_df_switches_ubicacion_and_zone_and_area )


            return "Archivo Creado en la ruta"
        except Exception as exception:
            raise ErrorHandlingUtils.application_error("Error al crear el archivo group de switches ", exception)

    

