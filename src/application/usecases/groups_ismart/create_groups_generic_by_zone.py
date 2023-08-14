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
from src.application.usecases.enums.name_column_df_group import NameColumnDfGroupEnum
from src.application.usecases.enums.name_column_df_group_path_files_yaml import NameColumnDfGroupPathFulesEnum
from src.application.usecases.enums.names_of_groups_enum import NameOfGroupEnum
from src.application.usecases.enums.names_files_yamls_enum import NameFilesYamlsEnum
from src.application.usecases.enums.name_titles_ismart_enum import NameTitlesIsmartEnum


from src.application.usecases.groups_ismart.groups_util_usecase import GroupsUtilUseCase
from src.application.usecases.utils.string_util_usecase import StringUtilUseCase


class CreateGroupsGenericByZone(GenericUseCase):
    def __init__(self, 
                 df: pd.DataFrame, 
                 domain: DomainEntitiesIsmartEnum,
                 icon_domain: str, 
                 name_of_group: NameOfGroupEnum, 
                 name_entity_ismart:NameEntitiesIsmartEnum,
                 name_title_ismart: NameTitlesIsmartEnum) -> None:
        self.df = df
        paths_usecase: PathsIsmartUseCase = PathsIsmartUseCase()
        self.path_ismart_principal = paths_usecase.get_root_path_ismar_home_assintant_principal_grupos()
        self.path_ismar_home_assintant_config = paths_usecase.get_root_path_ismar_home_assintant_config()
        self.name_group = domain.value
        self.domain = domain
        self.name_of_group = name_of_group
        self.name_entity_ismart = name_entity_ismart
        self.icon_domain = icon_domain
        self.name_title_ismart = name_title_ismart

       

    async def execute(self) -> pd.DataFrame:
        try:

            name_domain = self.domain.value
            name_entity_ismart = self.name_entity_ismart.value
            icon_domain = self.icon_domain
            name_title_ismart = self.name_title_ismart

            df_groups_generic_by_zone = GroupsUtilUseCase.build_df_empty_to_build_groups()
            df_yamls_paths_created_groups_generic_by_zone = GroupsUtilUseCase.build_df_empty_to_build_paths_files_yaml_groups()
                     
            zonas = self.df[ColumnsNameExcelConfigISmart.zonas.value].unique()

            
            name_file_yaml = NameFilesYamlsEnum.group_generic_.value + self.name_group
            for zona in zonas:
               

                # Filter domain switch by Zonas
                df_generic_by_zone = self.df[(self.df[ColumnsNameExcelConfigISmart.zonas.value] == zona) & (self.df[ColumnsNameExcelConfigISmart.domain.value] == name_domain)] 
                
                name_group_generic_by_zone = self.name_of_group.value +" "+ zona
                unique_id_generic = GroupsUtilUseCase.build_unique_id(name_file_yaml + "_"+name_group_generic_by_zone)
                
                df_generic_group_by_zone =  df_generic_by_zone[df_generic_by_zone[ColumnsNameExcelConfigISmart.name_entity.value].isin([name_entity_ismart])]

                dict_df_generic_by_zone = {}

                if name_domain == DomainEntitiesIsmartEnum.sensor.value:

                    dict_df_generic_by_zone = GroupsUtilUseCase.build_dict_group_sensor(df_generic_group_by_zone, name_group_generic_by_zone, unique_id_generic,"mean")

                if name_domain == DomainEntitiesIsmartEnum.cover.value:

                    dict_df_generic_by_zone = GroupsUtilUseCase.build_dict_group_cover(df_generic_group_by_zone, name_group_generic_by_zone, unique_id_generic)

                if dict_df_generic_by_zone:

                    name_file =  name_file_yaml +"_" + StringUtilUseCase.convert_string_lower_case(name_entity_ismart)+"_" + StringUtilUseCase.convert_string_lower_case(zona) + '.yaml'

                    
                    path_save_yaml = PathsIsmartUseCase.path_join_any_directores([self.path_ismart_principal,'Zonas', zona, 'Integraciones','grupos',self.name_of_group.value])
                    FolderCreator.execute(path_save_yaml)
                    YamlUtilUseCase.save_file_yaml(PathsIsmartUseCase.path_join_any_directores([path_save_yaml, name_file]),dict_df_generic_by_zone )

                    row_df_generic_group_by_zone = {
                                                            NameColumnDfGroupEnum.title.value:name_title_ismart.value, 
                                                            #NameColumnDfGroupEnum.entity.value: name_domain +'.'+unique_id_generic,
                                                            NameColumnDfGroupEnum.entity.value: name_domain +'.'+StringUtilUseCase.tranform_string_to_slug(name_group_generic_by_zone),
                                                            NameColumnDfGroupEnum.name_.value:name_group_generic_by_zone, 
                                                            NameColumnDfGroupEnum.icon.value: icon_domain, 
                                                            NameColumnDfGroupEnum.tap_action.value:'none'
                                                        }
                    

                    """ row_df_path_yamls= {
                                                            NameColumnDfGroupPathFulesEnum.name_.value:StringUtilUseCase.tranform_string_to_slug("gr "+name_group_generic_by_zone), 
                                                            NameColumnDfGroupPathFulesEnum.path_.value:path_save_yaml.replace(self.path_ismar_home_assintant_config+"\\", '')
                                                        } """
                    

                    
                    df_groups_generic_by_zone = df_groups_generic_by_zone.append(row_df_generic_group_by_zone, ignore_index=True)
                    
                    row_df_path_yamls= {
                                                            NameColumnDfGroupPathFulesEnum.name_.value:name_group_generic_by_zone, 
                                                            NameColumnDfGroupPathFulesEnum.path_.value:path_save_yaml
                                        }
                    df_yamls_paths_created_groups_generic_by_zone = df_yamls_paths_created_groups_generic_by_zone.append(row_df_path_yamls, ignore_index=True)
            
            return df_groups_generic_by_zone, df_yamls_paths_created_groups_generic_by_zone
        
        except Exception as exception:
            raise ErrorHandlingUtils.application_error("Error al crear el archivo group " +  name_domain + "Por zona", exception)

    
  
