import traceback
import pandas as pd
from fastapi import APIRouter,File, UploadFile

from src.application.usecases.interfaces import GenericUseCase

from src.application.utils.error_handling_utils import ErrorHandlingUtils


from src.application.usecases.utils.tranform_file_to_get_many_dataframe_usecase import TransformFileToGetManyDataFrameUseCase
from src.application.usecases.views_ismart.create_view_admin_dashboard_usecase import CreateViewAdminDashboardUseCase
from src.application.usecases.groups_ismart.create_groups_switch_by_zone_and_lights_usecase import CreateGroupsSwitchByZoneAndLightUseCase

from src.application.usecases.enums.names_sheet_excel_ismart_configuration_enum import SheetsNameExcelConfigISmart;



class CreateViewMainUseCase(GenericUseCase):
    def __init__(self,file: UploadFile, configurar_con_entidades_demos: bool) -> None:
        self.file = file
        self.configurar_con_entidades_demos = configurar_con_entidades_demos


    async def execute(self):
        try:
            df_views =  pd.DataFrame()
            

            tranform_file_to_dataframe_usecase:TransformFileToGetManyDataFrameUseCase =  TransformFileToGetManyDataFrameUseCase(self.file, [SheetsNameExcelConfigISmart.AreasSK.value, SheetsNameExcelConfigISmart.Entidades.value])
            dataframes = await tranform_file_to_dataframe_usecase.execute()

            groups_by_zones_and_swithes_light: CreateGroupsSwitchByZoneAndLightUseCase = CreateGroupsSwitchByZoneAndLightUseCase(dataframes.get(SheetsNameExcelConfigISmart.Entidades.value),self.configurar_con_entidades_demos)
            df_by_zones_and_swithes_light = await groups_by_zones_and_swithes_light.execute()

            create_view_admin:CreateViewAdminDashboardUseCase = CreateViewAdminDashboardUseCase(dataframes.get(SheetsNameExcelConfigISmart.AreasSK.value),self.configurar_con_entidades_demos,df_by_zones_and_swithes_light) 
            await create_view_admin.execute()
            print("")
        except Exception as exception:
            print(traceback.format_exc())
            raise ErrorHandlingUtils.application_error("Erro al crear las Views, Revisar el excel de configuración: " + SheetsNameExcelConfigISmart.AreasSK.value + " " + str(exception) , exception)
