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
from src.application.usecases.enums.name_entities_ismart_enum import NameEntitiesIsmartEnum

from src.application.usecases.groups_ismart.groups_util_usecase import GroupsUtilUseCase


class CreateGroupsSwitchByZoneAndLightUseCase(GenericUseCase):
    def __init__(self, df: pd.DataFrame, configurar_con_entidades_demos: bool) -> None:
        self.df = df
        self.configurar_con_entidades_demos = configurar_con_entidades_demos
        paths_usecase: PathsIsmartUseCase = PathsIsmartUseCase()
        self.path_ismart_principal = paths_usecase.get_root_path_ismar_home_assintant_principal_grupos()

       

    async def execute(self) -> pd.DataFrame:
        try:

    
            df_groups_switch_by_zone_and_light = GroupsUtilUseCase.build_df_empty_to_build_groups()
                     
            zonas = self.df[ColumnsNameExcelConfigISmart.zonas.value].unique()

            name_group = 'Luces'
            name_file_yaml = 'group_switch_'
            for zona in zonas:
               

                # Filter domain switch by Zonas
                df_switches_by_zone = self.df[(self.df[ColumnsNameExcelConfigISmart.zonas.value] == zona) & (self.df[ColumnsNameExcelConfigISmart.domain.value] == DomainEntitiesIsmartEnum.switch.value)] 
                df_switches_by_zone = df_switches_by_zone[df_switches_by_zone[ColumnsNameExcelConfigISmart.name_entity.value].isin([NameEntitiesIsmartEnum.Luces.value,NameEntitiesIsmartEnum.Luz.value ])]
                name_group_by_zone = name_group +" "+ zona

                unique_id = GroupsUtilUseCase.build_unique_id(name_file_yaml + name_group_by_zone)
                dict_df_switches_by_zone = GroupsUtilUseCase.build_dict_group_switch(df_switches_by_zone, name_group_by_zone, unique_id, self.configurar_con_entidades_demos)

                if dict_df_switches_by_zone:

                    name_file =  name_file_yaml + zona + '.yaml'
                    path_save_yaml = PathsIsmartUseCase.path_join_any_directores([self.path_ismart_principal,'Zonas', zona, 'Integraciones'])
                    FolderCreator.execute(path_save_yaml)
                    YamlUtilUseCase.save_file_yaml(PathsIsmartUseCase.path_join_any_directores([path_save_yaml, name_file]),dict_df_switches_by_zone )

                    new_row = {'title':'Luces de Zona', 'entity':'switch.'+unique_id, 'name':name_group_by_zone, 'icon':'mdi:lightbulb-group', 'tap_action':'none'}
                    df_groups_switch_by_zone_and_light = df_groups_switch_by_zone_and_light.append(new_row, ignore_index=True)

            
            return df_groups_switch_by_zone_and_light
        
        except Exception as exception:
            print(exception)
            raise ErrorHandlingUtils.application_error("Error al crear el archivo group de switches", exception)

    
  
