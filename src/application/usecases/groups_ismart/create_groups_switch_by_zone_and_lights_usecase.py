import typing
import pandas as pd
import yaml
from src.application.usecases.interfaces import GenericUseCase
from src.application.utils.error_handling_utils import ErrorHandlingUtils

from src.application.usecases.utils.paths_usecase import PathsIsmartUseCase;
from src.application.usecases.utils.yaml_util_usecase import YamlUtilUseCase
from src.application.usecases.utils.string_util_usecase import StringUtilUseCase
from src.application.usecases.utils.folder_creator_usecase import FolderCreator

from src.application.usecases.enums.names_columns_excel_ismart_configuration_enum import ColumnsNameExcelConfigISmart
from src.application.usecases.enums.domain_entities_ismart_enum import DomainEntitiesIsmartEnum
from src.application.usecases.enums.name_entities_ismart_enum import NameEntitiesIsmartEnum
from src.application.usecases.enums.entities_ismart_demos_enum import EntitiesIsmartDemosEnum
from src.application.usecases.enums.name_column_df_group import NameColumnDfGroupEnum
from src.application.usecases.enums.names_of_groups_enum import NameOfGroupEnum
from src.application.usecases.enums.names_files_yamls_enum import NameFilesYamlsEnum

from src.application.usecases.groups_ismart.groups_util_usecase import GroupsUtilUseCase

from src.application.usecases.enums.name_column_df_group_path_files_yaml import NameColumnDfGroupPathFulesEnum

from src.application.usecases.enums.domain_entities_ismart_enum import DomainEntitiesIsmartEnum


class CreateGroupsSwitchByZoneAndLightUseCase(GenericUseCase):
    def __init__(self, df: pd.DataFrame, configurar_con_entidades_demos: bool,domain: DomainEntitiesIsmartEnum) -> None:
        self.df = df
        self.configurar_con_entidades_demos = configurar_con_entidades_demos
        paths_usecase: PathsIsmartUseCase = PathsIsmartUseCase()
        self.path_ismart_principal = paths_usecase.get_root_path_ismar_home_assintant_principal_grupos()
        self.domain = domain

       

    async def execute(self) -> pd.DataFrame:
        try:

    
            df_groups_switch_by_zone_and_light = GroupsUtilUseCase.build_df_empty_to_build_groups()
            df_yamls_paths = GroupsUtilUseCase.build_df_empty_to_build_paths_files_yaml_groups()                     

            zonas = self.df[ColumnsNameExcelConfigISmart.zonas.value].unique()

            name_group = NameOfGroupEnum.lights.value
            name_file_yaml = NameFilesYamlsEnum.group_switch_.value
            for zona in zonas:
               

                # Filter domain switch by Zonas
                df_switches_by_zone = self.df[(self.df[ColumnsNameExcelConfigISmart.zonas.value] == zona) & (self.df[ColumnsNameExcelConfigISmart.domain.value] == DomainEntitiesIsmartEnum.switch.value)] 
                df_switches_by_zone = df_switches_by_zone[df_switches_by_zone[ColumnsNameExcelConfigISmart.name_entity.value].isin([NameEntitiesIsmartEnum.Luces.value,NameEntitiesIsmartEnum.Luz.value ])]
                name_group_by_zone = name_group +" "+ zona

                unique_id = GroupsUtilUseCase.build_unique_id(name_file_yaml + name_group_by_zone)
                dict_df_switches_by_zone = GroupsUtilUseCase.build_dict_group_switch(df_switches_by_zone, name_group_by_zone, unique_id)

                if dict_df_switches_by_zone:

                    name_file =  name_file_yaml + zona + '.yaml'
                    path_save_yaml = PathsIsmartUseCase.path_join_any_directores([self.path_ismart_principal,'Zonas', zona, 'Integraciones','grupos','switch'])
                    FolderCreator.execute(path_save_yaml)
                    YamlUtilUseCase.save_file_yaml(PathsIsmartUseCase.path_join_any_directores([path_save_yaml, name_file]),dict_df_switches_by_zone )

                    row_df_switches_by_zone_and_light = {
                                                            NameColumnDfGroupEnum.title.value:'Luces de Zona', 
                                                            #NameColumnDfGroupEnum.entity.value:'switch.'+unique_id,
                                                            NameColumnDfGroupEnum.entity.value:'switch.'+StringUtilUseCase.tranform_string_to_slug(name_group_by_zone),
                                                            
                                                            NameColumnDfGroupEnum.name_.value:name_group_by_zone, 
                                                            NameColumnDfGroupEnum.icon.value:'mdi:lightbulb-group', 
                                                            NameColumnDfGroupEnum.tap_action.value:'none'
                                                        }
                    
                    if self.configurar_con_entidades_demos:
                        row_df_switches_by_zone_and_light[NameColumnDfGroupEnum.entity.value] = EntitiesIsmartDemosEnum.switch_group.value

                    df_groups_switch_by_zone_and_light = df_groups_switch_by_zone_and_light.append(row_df_switches_by_zone_and_light, ignore_index=True)

                    row_df_path_yamls= {
                                            NameColumnDfGroupPathFulesEnum.name_.value:name_group_by_zone, 
                                            NameColumnDfGroupPathFulesEnum.path_.value:path_save_yaml,
                                            NameColumnDfGroupPathFulesEnum.domain_.value: self.domain.value
                                        }
                            
                    df_yamls_paths = df_yamls_paths.append(row_df_path_yamls, ignore_index=True)
            
            return df_groups_switch_by_zone_and_light, df_yamls_paths
        
        except Exception as exception:
            raise ErrorHandlingUtils.application_error("Error al crear el archivo group de switches", exception)

    
  
