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
from src.application.usecases.enums.names_of_groups_enum import NameOfGroupEnum
from src.application.usecases.enums.names_files_yamls_enum import NameFilesYamlsEnum
from src.application.usecases.enums.name_titles_ismart_enum import NameTitlesIsmartEnum

from src.application.usecases.groups_ismart.groups_util_usecase import GroupsUtilUseCase
from src.application.usecases.utils.string_util_usecase import StringUtilUseCase


class CreateGroupsSensorHumedityByArea(GenericUseCase):
    def __init__(self, df: pd.DataFrame) -> None:
        self.df = df
        paths_usecase: PathsIsmartUseCase = PathsIsmartUseCase()
        self.path_ismart_principal = paths_usecase.get_root_path_ismar_home_assintant_principal_grupos()

       

    async def execute(self) -> pd.DataFrame:
        try:

    
            df_groups_sensor_humedity_by_area = GroupsUtilUseCase.build_df_empty_to_build_groups()
                     
            zonas = self.df[ColumnsNameExcelConfigISmart.zonas.value].unique()

            
            name_file_yaml = NameFilesYamlsEnum.group_sensor_.value
            for zona in zonas:
               
                ubication = self.df[ColumnsNameExcelConfigISmart.ubicacion.value].unique()
                
                for ubi in ubication:

                    areas = self.df[ColumnsNameExcelConfigISmart.areas.value].unique()

                    for area in areas:

                        df_sensor_by_area = self.df[(self.df[ColumnsNameExcelConfigISmart.ubicacion.value] == ubi) &
                                                    (self.df[ColumnsNameExcelConfigISmart.zonas.value] == zona) & 
                                                    (self.df[ColumnsNameExcelConfigISmart.areas.value] == area) & 
                                                    (self.df[ColumnsNameExcelConfigISmart.domain.value] == DomainEntitiesIsmartEnum.sensor.value)] 
                        
                        name_group_humedity_by_area = NameOfGroupEnum.sensor_humedad.value +" "+ area
                        unique_id_humedity = GroupsUtilUseCase.build_unique_id(name_file_yaml + name_group_humedity_by_area)
                        
                        df_sensor_humedity_by_area =  df_sensor_by_area[df_sensor_by_area[ColumnsNameExcelConfigISmart.name_entity.value].isin([NameEntitiesIsmartEnum.Humedad.value])]
                        dict_df_sensor_humedity_by_area = GroupsUtilUseCase.build_dict_group_sensor(df_sensor_humedity_by_area, name_group_humedity_by_area, unique_id_humedity,"mean")


                        if dict_df_sensor_humedity_by_area:

                            name_file =  name_file_yaml + StringUtilUseCase.convert_string_lower_case(NameEntitiesIsmartEnum.Humedad.value)+"_" + StringUtilUseCase.convert_string_lower_case(area) + '.yaml'
                            path_save_yaml = PathsIsmartUseCase.path_join_any_directores([self.path_ismart_principal,'Zonas', zona,'Ubicacion', ubi,'Areas',area, 'Integraciones'])
                            FolderCreator.execute(path_save_yaml)
                            YamlUtilUseCase.save_file_yaml(PathsIsmartUseCase.path_join_any_directores([path_save_yaml, name_file]),dict_df_sensor_humedity_by_area )

                            row_df_sensor_humedity_by_zone = {
                                                                    NameColumnDfGroupEnum.title.value:NameTitlesIsmartEnum.humedad_por_area.value, 
                                                                    NameColumnDfGroupEnum.entity.value:'sensor.'+unique_id_humedity,
                                                                    NameColumnDfGroupEnum.name_.value:name_group_humedity_by_area, 
                                                                    NameColumnDfGroupEnum.icon.value:'mdi:home-thermometer', 
                                                                    NameColumnDfGroupEnum.tap_action.value:'none'
                                                                }
                            
                            
                            df_groups_sensor_humedity_by_area = df_groups_sensor_humedity_by_area.append(row_df_sensor_humedity_by_zone, ignore_index=True)

            
            return df_groups_sensor_humedity_by_area
        
        except Exception as exception:
            raise ErrorHandlingUtils.application_error("Error al crear el archivo group de sensores Humedad por area", exception)

    
  
