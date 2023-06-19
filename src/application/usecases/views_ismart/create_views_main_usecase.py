import traceback
import pandas as pd
from fastapi import APIRouter,File, UploadFile

from src.application.usecases.interfaces import GenericUseCase

from src.application.utils.error_handling_utils import ErrorHandlingUtils


from src.application.usecases.utils.tranform_file_to_get_many_dataframe_usecase import TransformFileToGetManyDataFrameUseCase
from src.application.usecases.views_ismart.create_view_admin_dashboard_usecase import CreateViewAdminDashboardUseCase

from src.application.usecases.groups_ismart.create_groups_switch_by_zone_and_lights_usecase import CreateGroupsSwitchByZoneAndLightUseCase
from src.application.usecases.groups_ismart.create_groups_switch_by_ubication_and_lights_usecase import CreateGroupsSwitchByUbicationAndLightUseCase
from src.application.usecases.groups_ismart.create_groups_switch_by_areas_and_lights_usecase import CreateGroupsSwitchByAreasAndLightUseCase

from src.application.usecases.scenes_ismart.create_scenes_usecase import CreateScenesUseCase

from src.application.usecases.enums.names_sheet_excel_ismart_configuration_enum import SheetsNameExcelConfigISmart;
from src.application.usecases.enums.names_columns_excel_ismart_configuration_enum import ColumnsNameExcelConfigISmart
from src.application.usecases.enums.entities_ismart_demos_enum import EntitiesIsmartDemosEnum
from src.application.usecases.enums.domain_entities_ismart_enum import DomainEntitiesIsmartEnum
from src.application.usecases.enums.entities_ismart_demos_enum import EntitiesIsmartDemosEnum


class CreateViewMainUseCase(GenericUseCase):
    def __init__(self,file: UploadFile, configurar_con_entidades_demos: bool) -> None:
        self.file = file
        self.configurar_con_entidades_demos = configurar_con_entidades_demos


    async def execute(self):
        try:
            df_views =  pd.DataFrame()
            

            df_excel:TransformFileToGetManyDataFrameUseCase =  TransformFileToGetManyDataFrameUseCase(self.file,
                                                                                                    [SheetsNameExcelConfigISmart.AreasSK.value, 
                                                                                                    SheetsNameExcelConfigISmart.Entidades.value,
                                                                                                    SheetsNameExcelConfigISmart.Personas.value,
                                                                                                    SheetsNameExcelConfigISmart.Scenes_config.value])
            dataframes = await df_excel.execute()

            df_entidades = dataframes.get(SheetsNameExcelConfigISmart.Entidades.value)

            df_areas = dataframes.get(SheetsNameExcelConfigISmart.AreasSK.value)

            df_personas = dataframes.get(SheetsNameExcelConfigISmart.Personas.value)

            df_scenes_config = dataframes.get(SheetsNameExcelConfigISmart.Scenes_config.value)

            
            if self.configurar_con_entidades_demos:

                df_entidades = self.change_values_of_entities_by_domain_demo_default(df_entidades)
                df_personas = self.change_values_entities_demo(df_personas,ColumnsNameExcelConfigISmart.persona.value, EntitiesIsmartDemosEnum.person.value )
                


            groups_by_zones_and_swithes_light: CreateGroupsSwitchByZoneAndLightUseCase = CreateGroupsSwitchByZoneAndLightUseCase(df_entidades,self.configurar_con_entidades_demos)
            df_by_zones_and_swithes_light = await groups_by_zones_and_swithes_light.execute()

            groups_by_ubi_and_swithes_light: CreateGroupsSwitchByUbicationAndLightUseCase = CreateGroupsSwitchByUbicationAndLightUseCase(df_entidades,self.configurar_con_entidades_demos)
            df_by_ubi_and_swithes_light = await groups_by_ubi_and_swithes_light.execute()


            groups_by_area_and_swithes_light: CreateGroupsSwitchByAreasAndLightUseCase = CreateGroupsSwitchByAreasAndLightUseCase(df_entidades,self.configurar_con_entidades_demos)
            df_by_areas_and_swithes_light = await groups_by_area_and_swithes_light.execute()

            create_scenes_useCase: CreateScenesUseCase = CreateScenesUseCase(df_scenes_config,
                                                                             df_areas,
                                                                             df_entidades,
                                                                             self.configurar_con_entidades_demos)
            
            df_create_scenes_admin,df_create_scenes  = await create_scenes_useCase.execute()


            create_view_admin:CreateViewAdminDashboardUseCase = CreateViewAdminDashboardUseCase(df_areas,
                                                                                                self.configurar_con_entidades_demos,
                                                                                                df_by_zones_and_swithes_light,
                                                                                                df_by_ubi_and_swithes_light,
                                                                                                df_by_areas_and_swithes_light,
                                                                                                df_personas,
                                                                                                df_create_scenes_admin) 
            await create_view_admin.execute()

        except Exception as exception:
            print(traceback.format_exc())
            raise ErrorHandlingUtils.application_error("Erro al crear las Views, Revisar el excel de configuración: " + SheetsNameExcelConfigISmart.AreasSK.value + " " + str(exception) , exception)


    def change_values_entities_demo(self, df: pd.DataFrame, colunm:str, new_vale:str):
        df.loc[:, [colunm]] = new_vale
        return df
    
    def change_values_of_entities_by_domain_demo_default(self, df: pd.DataFrame):
    
        df.loc[df[ColumnsNameExcelConfigISmart.domain.value] == DomainEntitiesIsmartEnum.switch.value, ColumnsNameExcelConfigISmart.final_id.value] = EntitiesIsmartDemosEnum.switch_ac.value
        df.loc[df[ColumnsNameExcelConfigISmart.domain.value] == DomainEntitiesIsmartEnum.sensor.value, ColumnsNameExcelConfigISmart.final_id.value] = EntitiesIsmartDemosEnum.sensor.value
        return df
