import traceback
import pandas as pd
import numpy as np
from fastapi import APIRouter,File, UploadFile

from src.application.usecases.interfaces import GenericUseCase

from src.application.utils.error_handling_utils import ErrorHandlingUtils
from src.application.usecases.utils.string_util_usecase import StringUtilUseCase


from src.application.usecases.utils.tranform_file_to_get_many_dataframe_usecase import TransformFileToGetManyDataFrameUseCase
from src.application.usecases.views_ismart.create_view_admin_dashboard_usecase import CreateViewAdminDashboardUseCase
from src.application.usecases.views_ismart.create_view_by_areas_dashboard_usecase import CreateViewByAreasDashboardUseCase



from src.application.usecases.groups_ismart.create_groups_switch_by_zone_and_lights_usecase import CreateGroupsSwitchByZoneAndLightUseCase
from src.application.usecases.groups_ismart.create_groups_switch_by_ubication_and_lights_usecase import CreateGroupsSwitchByUbicationAndLightUseCase
from src.application.usecases.groups_ismart.create_groups_switch_by_areas_and_lights_usecase import CreateGroupsSwitchByAreasAndLightUseCase


from src.application.usecases.groups_ismart.create_groups_generic_by_zone import CreateGroupsGenericByZone
from src.application.usecases.groups_ismart.create_groups_generic_by_ubication import CreateGroupsGenericByUbication
from src.application.usecases.groups_ismart.create_groups_generic_by_area import CreateGroupsGenericByArea

from src.application.usecases.scenes_ismart.create_scenes_usecase import CreateScenesUseCase
from src.application.usecases.config_ismart.create_config_file_usecase import  CreateConfigFileUseCase

from src.application.usecases.enums.names_sheet_excel_ismart_configuration_enum import SheetsNameExcelConfigISmart;
from src.application.usecases.enums.names_columns_excel_ismart_configuration_enum import ColumnsNameExcelConfigISmart
from src.application.usecases.enums.entities_ismart_demos_enum import EntitiesIsmartDemosEnum
from src.application.usecases.enums.domain_entities_ismart_enum import DomainEntitiesIsmartEnum
from src.application.usecases.enums.entities_ismart_demos_enum import EntitiesIsmartDemosEnum
from src.application.usecases.enums.name_entities_ismart_enum import NameEntitiesIsmartEnum
from src.application.usecases.enums.names_of_groups_enum import NameOfGroupEnum
from src.application.usecases.enums.name_titles_ismart_enum import NameTitlesIsmartEnum
from src.application.usecases.enums.name_column_df_group_path_files_yaml import NameColumnDfGroupPathFulesEnum
from src.application.usecases.groups_ismart.groups_util_usecase import GroupsUtilUseCase
from src.application.usecases.utils.paths_usecase import PathsIsmartUseCase;


class CreateViewMainUseCase(GenericUseCase):
    def __init__(self,file: UploadFile, configurar_con_entidades_demos: bool) -> None:
        self.file = file
        self.configurar_con_entidades_demos = configurar_con_entidades_demos
        paths_usecase: PathsIsmartUseCase = PathsIsmartUseCase()
        self.path_ismar_home_assintant_config = paths_usecase.get_root_path_ismar_home_assintant_config()


    async def execute(self):
        try:
            df_views =  pd.DataFrame()
            path_ismar_home_assintant_config = self.path_ismar_home_assintant_config
            

            df_excel:TransformFileToGetManyDataFrameUseCase =  TransformFileToGetManyDataFrameUseCase(self.file,
                                                                                                    [SheetsNameExcelConfigISmart.AreasSK.value, 
                                                                                                    SheetsNameExcelConfigISmart.Entidades.value,
                                                                                                    SheetsNameExcelConfigISmart.Personas.value,
                                                                                                    SheetsNameExcelConfigISmart.Scenes_config.value,
                                                                                                    SheetsNameExcelConfigISmart.Cards_order_in_view.value,
                                                                                                    SheetsNameExcelConfigISmart.Configuracion.value])
            dataframes = await df_excel.execute()

            df_entidades = dataframes.get(SheetsNameExcelConfigISmart.Entidades.value)

            df_areas = dataframes.get(SheetsNameExcelConfigISmart.AreasSK.value)

            df_personas = dataframes.get(SheetsNameExcelConfigISmart.Personas.value)

            df_scenes_config = dataframes.get(SheetsNameExcelConfigISmart.Scenes_config.value)

            df_config_file = dataframes.get(SheetsNameExcelConfigISmart.Configuracion.value)

            df_cards_orden_in_view = dataframes.get(SheetsNameExcelConfigISmart.Cards_order_in_view.value)

            if self.configurar_con_entidades_demos:

                df_entidades = self.change_values_of_entities_by_domain_demo_default(df_entidades)
                df_personas = self.change_values_entities_demo(df_personas,ColumnsNameExcelConfigISmart.persona.value, EntitiesIsmartDemosEnum.person.value )
                

            df_yamls_paths_created_groups = GroupsUtilUseCase.build_df_empty_to_build_paths_files_yaml_groups()



             ######  ##      ## #### ########  ######  ##     ## ########  ######  
            ##    ## ##  ##  ##  ##     ##    ##    ## ##     ## ##       ##    ## 
            ##       ##  ##  ##  ##     ##    ##       ##     ## ##       ##       
             ######  ##  ##  ##  ##     ##    ##       ######### ######    ######  
                  ## ##  ##  ##  ##     ##    ##       ##     ## ##             ## 
            ##    ## ##  ##  ##  ##     ##    ##    ## ##     ## ##       ##    ## 
             ######   ###  ###  ####    ##     ######  ##     ## ########  ######  


            groups_by_zones_and_swithes_light: CreateGroupsSwitchByZoneAndLightUseCase = CreateGroupsSwitchByZoneAndLightUseCase(df_entidades,self.configurar_con_entidades_demos,DomainEntitiesIsmartEnum.switch)
            df_by_zones_and_swithes_light, df_paths_yamls_by_zones_and_swithes_light = await groups_by_zones_and_swithes_light.execute()

            df_yamls_paths_created_groups = df_yamls_paths_created_groups.append(df_paths_yamls_by_zones_and_swithes_light)

            groups_by_ubi_and_swithes_light: CreateGroupsSwitchByUbicationAndLightUseCase = CreateGroupsSwitchByUbicationAndLightUseCase(df_entidades,self.configurar_con_entidades_demos,DomainEntitiesIsmartEnum.switch)
            df_by_ubi_and_swithes_light, df_path_yaml_by_ubi_and_swithes_light = await groups_by_ubi_and_swithes_light.execute()

            df_yamls_paths_created_groups = df_yamls_paths_created_groups.append(df_path_yaml_by_ubi_and_swithes_light)

            groups_by_area_and_swithes_light: CreateGroupsSwitchByAreasAndLightUseCase = CreateGroupsSwitchByAreasAndLightUseCase(df_entidades,self.configurar_con_entidades_demos,DomainEntitiesIsmartEnum.switch)
            df_by_areas_and_swithes_light,df_paths_yaml_by_areas_and_swithes_light = await groups_by_area_and_swithes_light.execute()

            df_yamls_paths_created_groups = df_yamls_paths_created_groups.append(df_paths_yaml_by_areas_and_swithes_light)

             ######   ######  ######## ##    ## ########  ######  
            ##    ## ##    ## ##       ###   ## ##       ##    ## 
            ##       ##       ##       ####  ## ##       ##       
             ######  ##       ######   ## ## ## ######    ######  
                  ## ##       ##       ##  #### ##             ## 
            ##    ## ##    ## ##       ##   ### ##       ##    ## 
             ######   ######  ######## ##    ## ########  ######  

            create_scenes_useCase: CreateScenesUseCase = CreateScenesUseCase(df_scenes_config,
                                                                             df_areas,
                                                                             df_entidades,
                                                                             self.configurar_con_entidades_demos)
            
            df_create_scenes_admin,df_create_scenes  = await create_scenes_useCase.execute()



            
             ######## ######## ##     ## ########  ######## ########     ###    ######## ##     ## ########     ###    
                ##    ##       ###   ### ##     ## ##       ##     ##   ## ##      ##    ##     ## ##     ##   ## ##   
                ##    ##       #### #### ##     ## ##       ##     ##  ##   ##     ##    ##     ## ##     ##  ##   ##  
                ##    ######   ## ### ## ########  ######   ########  ##     ##    ##    ##     ## ########  ##     ## 
                ##    ##       ##     ## ##        ##       ##   ##   #########    ##    ##     ## ##   ##   ######### 
                ##    ##       ##     ## ##        ##       ##    ##  ##     ##    ##    ##     ## ##    ##  ##     ## 
                ##    ######## ##     ## ##        ######## ##     ## ##     ##    ##     #######  ##     ## ##     ## 

 


            groups_sensor_temperature_by_zones: CreateGroupsGenericByZone = CreateGroupsGenericByZone(df_entidades,
                                                                                          DomainEntitiesIsmartEnum.sensor,
                                                                                          "mdi:home-thermometer",
                                                                                          NameOfGroupEnum.sensor_temperatura,
                                                                                          NameEntitiesIsmartEnum.Temperatura,
                                                                                          NameTitlesIsmartEnum.temperatura_por_zona)
            
            df_groups_sensor_temperature_by_zones,df_paths_yamls_groups_sensor_temperature_by_zones  = await groups_sensor_temperature_by_zones.execute()

            df_yamls_paths_created_groups = df_yamls_paths_created_groups.append(df_paths_yamls_groups_sensor_temperature_by_zones)

            
            groups_sensor_temp_by_ubi: CreateGroupsGenericByUbication = CreateGroupsGenericByUbication(df_entidades,
                                                                                          DomainEntitiesIsmartEnum.sensor,
                                                                                          "mdi:home-thermometer",
                                                                                          NameOfGroupEnum.sensor_temperatura,
                                                                                          NameEntitiesIsmartEnum.Temperatura,
                                                                                          NameTitlesIsmartEnum.temperatura_por_ubicacion)
            df_groups_sensor_temp_by_ubi,df_paths_yamls_groups_sensor_temp_by_ubi = await groups_sensor_temp_by_ubi.execute()

            df_yamls_paths_created_groups = df_yamls_paths_created_groups.append(df_paths_yamls_groups_sensor_temp_by_ubi)


            
            groups_sensor_temp_by_area: CreateGroupsGenericByArea = CreateGroupsGenericByArea(df_entidades,
                                                                                          DomainEntitiesIsmartEnum.sensor,
                                                                                          "mdi:home-thermometer",
                                                                                          NameOfGroupEnum.sensor_temperatura,
                                                                                          NameEntitiesIsmartEnum.Temperatura,
                                                                                          NameTitlesIsmartEnum.temperatura_por_area)
            df_groups_sensor_temp_by_area, df_paths_yamls_groups_sensor_temp_by_area = await groups_sensor_temp_by_area.execute()
            
            df_yamls_paths_created_groups = df_yamls_paths_created_groups.append(df_paths_yamls_groups_sensor_temp_by_area)
            ##     ## ##     ## ##     ## ######## ########     ###    ########  
            ##     ## ##     ## ###   ### ##       ##     ##   ## ##   ##     ## 
            ##     ## ##     ## #### #### ##       ##     ##  ##   ##  ##     ## 
            ######### ##     ## ## ### ## ######   ##     ## ##     ## ##     ## 
            ##     ## ##     ## ##     ## ##       ##     ## ######### ##     ## 
            ##     ## ##     ## ##     ## ##       ##     ## ##     ## ##     ## 
            ##     ##  #######  ##     ## ######## ########  ##     ## ########  

            
            groups_sensor_humedad_by_zones: CreateGroupsGenericByZone = CreateGroupsGenericByZone(df_entidades,
                                                                                          DomainEntitiesIsmartEnum.sensor,
                                                                                          "mdi:home-thermometer",
                                                                                          NameOfGroupEnum.sensor_humedad,
                                                                                          NameEntitiesIsmartEnum.Humedad,
                                                                                          NameTitlesIsmartEnum.humedad_por_zona)
            df_groups_sensor_humedad_by_zones,df_paths_yamls_groups_sensor_humedad_by_zones  = await groups_sensor_humedad_by_zones.execute()

            df_yamls_paths_created_groups = df_yamls_paths_created_groups.append(df_paths_yamls_groups_sensor_humedad_by_zones)
            

            groups_sensor_humedad_by_ubi: CreateGroupsGenericByUbication = CreateGroupsGenericByUbication(df_entidades,
                                                                                          DomainEntitiesIsmartEnum.sensor,
                                                                                          "mdi:home-thermometer",
                                                                                          NameOfGroupEnum.sensor_humedad,
                                                                                          NameEntitiesIsmartEnum.Humedad,
                                                                                          NameTitlesIsmartEnum.humedad_por_ubicacion)
            df_groups_sensor_humedad_by_ubi, df_paths_yamls_groups_sensor_humedad_by_ubi = await groups_sensor_humedad_by_ubi.execute()

            df_yamls_paths_created_groups = df_yamls_paths_created_groups.append(df_paths_yamls_groups_sensor_humedad_by_ubi)

            groups_sensor_humedad_by_area: CreateGroupsGenericByArea = CreateGroupsGenericByArea(df_entidades,
                                                                                          DomainEntitiesIsmartEnum.sensor,
                                                                                          "mdi:home-thermometer",
                                                                                          NameOfGroupEnum.sensor_humedad,
                                                                                          NameEntitiesIsmartEnum.Humedad,
                                                                                          NameTitlesIsmartEnum.humedad_por_area)
            df_groups_sensor_humedad_by_area,df_paths_yamls_groups_sensor_humedad_by_area  = await groups_sensor_humedad_by_area.execute()

            df_yamls_paths_created_groups = df_yamls_paths_created_groups.append(df_paths_yamls_groups_sensor_humedad_by_area)

            ######   #######  ##     ## ######## ########  
            ##    ## ##     ## ##     ## ##       ##     ## 
            ##       ##     ## ##     ## ##       ##     ## 
            ##       ##     ## ##     ## ######   ########  
            ##       ##     ##  ##   ##  ##       ##   ##   
            ##    ## ##     ##   ## ##   ##       ##    ##  
            ######   #######     ###    ######## ##     ## 

            groups_cover_by_zones: CreateGroupsGenericByZone = CreateGroupsGenericByZone(df_entidades,
                                                                                          DomainEntitiesIsmartEnum.cover,
                                                                                          "mdi:curtains-closed",
                                                                                          NameOfGroupEnum.cover,
                                                                                          NameEntitiesIsmartEnum.M_Cortina,
                                                                                          NameTitlesIsmartEnum.cortinas_por_zona)
            
            
            
            df_groups_covers_by_zones,df_paths_yamls_groups_covers_by_zones  = await groups_cover_by_zones.execute()

            df_yamls_paths_created_groups = df_yamls_paths_created_groups.append(df_paths_yamls_groups_covers_by_zones)

            
            groups_cover_by_ubication: CreateGroupsGenericByUbication = CreateGroupsGenericByUbication(df_entidades,
                                                                                          DomainEntitiesIsmartEnum.cover,
                                                                                          "mdi:curtains-closed",
                                                                                          NameOfGroupEnum.cover,
                                                                                          NameEntitiesIsmartEnum.M_Cortina,
                                                                                          NameTitlesIsmartEnum.cortinas_por_ubicacion)
            


            df_groups_covers_by_ubication,df_paths_yamls_groups_covers_by_ubication = await groups_cover_by_ubication.execute()
            
            df_yamls_paths_created_groups = df_yamls_paths_created_groups.append(df_paths_yamls_groups_covers_by_ubication)

            groups_cover_by_area: CreateGroupsGenericByArea = CreateGroupsGenericByArea(df_entidades,
                                                                                          DomainEntitiesIsmartEnum.cover,
                                                                                          "mdi:curtains-closed",
                                                                                          NameOfGroupEnum.cover,
                                                                                          NameEntitiesIsmartEnum.M_Cortina,
                                                                                          NameTitlesIsmartEnum.cortinas_por_area)
            
            
            df_groups_cover_by_area,df_paths_groups_cover_by_area = await groups_cover_by_area.execute()

            df_yamls_paths_created_groups = df_yamls_paths_created_groups.append(df_paths_groups_cover_by_area)





             ######   #######  ##    ## ######## ####  ######   ##     ## ########     ###    ######## ####  #######  ##    ## 
            ##    ## ##     ## ###   ## ##        ##  ##    ##  ##     ## ##     ##   ## ##      ##     ##  ##     ## ###   ## 
            ##       ##     ## ####  ## ##        ##  ##        ##     ## ##     ##  ##   ##     ##     ##  ##     ## ####  ## 
            ##       ##     ## ## ## ## ######    ##  ##   #### ##     ## ########  ##     ##    ##     ##  ##     ## ## ## ## 
            ##       ##     ## ##  #### ##        ##  ##    ##  ##     ## ##   ##   #########    ##     ##  ##     ## ##  #### 
            ##    ## ##     ## ##   ### ##        ##  ##    ##  ##     ## ##    ##  ##     ##    ##     ##  ##     ## ##   ### 
             ######   #######  ##    ## ##       ####  ######    #######  ##     ## ##     ##    ##    ####  #######  ##    ## 

            
            
            for index, row in df_yamls_paths_created_groups.iterrows():
 
                row[NameColumnDfGroupPathFulesEnum.path_.value]= row[NameColumnDfGroupPathFulesEnum.path_.value].replace(path_ismar_home_assintant_config+'\\', '')
                row[NameColumnDfGroupPathFulesEnum.name_.value] = StringUtilUseCase.tranform_string_to_slug(row[NameColumnDfGroupPathFulesEnum.name_.value])


            create_config_file_use_case: CreateConfigFileUseCase = CreateConfigFileUseCase(
                                                                             df_config_file,
                                                                             df_yamls_paths_created_groups,
                                                                             self.configurar_con_entidades_demos)
            
            await create_config_file_use_case.execute()

            print("1-------------")
            print(df_by_zones_and_swithes_light)

            create_view_admin:CreateViewAdminDashboardUseCase = CreateViewAdminDashboardUseCase(df_areas,
                                                                                                self.configurar_con_entidades_demos,
                                                                                                df_by_zones_and_swithes_light,
                                                                                                df_by_ubi_and_swithes_light,
                                                                                                df_by_areas_and_swithes_light,
                                                                                                df_personas,
                                                                                                df_create_scenes_admin,
                                                                                                df_groups_sensor_temperature_by_zones,
                                                                                                df_groups_sensor_temp_by_ubi,
                                                                                                df_groups_sensor_temp_by_area,
                                                                                                df_groups_sensor_humedad_by_zones,
                                                                                                df_groups_sensor_humedad_by_ubi,
                                                                                                df_groups_sensor_humedad_by_area,
                                                                                                df_groups_covers_by_zones,
                                                                                                df_groups_covers_by_ubication,
                                                                                                df_groups_cover_by_area
                                                                                                ) 
            await create_view_admin.execute()



            create_view_by_areas: CreateViewByAreasDashboardUseCase = CreateViewByAreasDashboardUseCase(df_areas,
                                                                                                self.configurar_con_entidades_demos,
                                                                                                df_by_areas_and_swithes_light,
                                                                                                df_personas,
                                                                                                df_create_scenes,
                                                                                                df_entidades,
                                                                                                df_cards_orden_in_view,
                                                                                                df_groups_sensor_temp_by_area,
                                                                                                df_groups_sensor_humedad_by_area)
            
            await create_view_by_areas.execute()

        except Exception as exception:
            print(traceback.format_exc())
            raise ErrorHandlingUtils.application_error("Erro al crear las Views, Revisar el excel de configuración: " + SheetsNameExcelConfigISmart.AreasSK.value + " " + str(exception) , exception)


    def change_values_entities_demo(self, df: pd.DataFrame, colunm:str, new_vale:str):
        df.loc[:, [colunm]] = new_vale
        return df
    
    def change_values_of_entities_by_domain_demo_default(self, df: pd.DataFrame):
    
        df.loc[df[ColumnsNameExcelConfigISmart.domain.value] == DomainEntitiesIsmartEnum.switch.value, ColumnsNameExcelConfigISmart.final_id.value] = EntitiesIsmartDemosEnum.switch_ac.value
        df.loc[df[ColumnsNameExcelConfigISmart.domain.value] == DomainEntitiesIsmartEnum.sensor.value, ColumnsNameExcelConfigISmart.final_id.value] = EntitiesIsmartDemosEnum.sensor.value
        
        df[ColumnsNameExcelConfigISmart.final_id.value] = np.where((df[ColumnsNameExcelConfigISmart.domain.value] == DomainEntitiesIsmartEnum.sensor.value) & (df[ColumnsNameExcelConfigISmart.name_entity.value] == NameEntitiesIsmartEnum.Temperatura.value), EntitiesIsmartDemosEnum.sensor_temperature.value, df[ ColumnsNameExcelConfigISmart.final_id.value])
        df[ColumnsNameExcelConfigISmart.final_id.value] = np.where((df[ColumnsNameExcelConfigISmart.domain.value] == DomainEntitiesIsmartEnum.sensor.value) & (df[ColumnsNameExcelConfigISmart.name_entity.value] == NameEntitiesIsmartEnum.Humedad.value), EntitiesIsmartDemosEnum.sensor_humedad.value, df[ ColumnsNameExcelConfigISmart.final_id.value])
        df[ColumnsNameExcelConfigISmart.final_id.value] = np.where((df[ColumnsNameExcelConfigISmart.domain.value] == DomainEntitiesIsmartEnum.sensor.value) & (df[ColumnsNameExcelConfigISmart.name_entity.value] == NameEntitiesIsmartEnum.Bateria_Sensor_TH.value), EntitiesIsmartDemosEnum.sensor_humedad.value, df[ ColumnsNameExcelConfigISmart.final_id.value])
       
        df[ColumnsNameExcelConfigISmart.final_id.value] = np.where((df[ColumnsNameExcelConfigISmart.domain.value] == DomainEntitiesIsmartEnum.cover.value) & (df[ColumnsNameExcelConfigISmart.name_entity.value] == NameEntitiesIsmartEnum.M_Cortina.value), EntitiesIsmartDemosEnum.cover.value, df[ ColumnsNameExcelConfigISmart.final_id.value])
        return df
