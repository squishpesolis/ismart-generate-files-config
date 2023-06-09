import typing
import pandas as pd
import yaml
from fastapi import APIRouter,File, UploadFile


from src.application.usecases.interfaces import GenericUseCase
from src.application.usecases.utils.paths_usecase import PathsIsmartUseCase;
from src.application.usecases.utils.yaml_util_usecase import YamlUtilUseCase
from src.application.usecases.utils.string_util_usecase import StringUtilUseCase
from src.application.usecases.utils.tranform_file_to_dataframe_usecase import TransformFileToDataFrameUseCase

from src.application.utils.error_handling_utils import ErrorHandlingUtils

from src.application.usecases.utils.folder_creator_usecase import FolderCreator

from src.application.usecases.enums.names_columns_excel_ismart_configuration_enum import ColumnsNameExcelConfigISmart
from src.application.usecases.enums.names_sheet_excel_ismart_configuration_enum import SheetsNameExcelConfigISmart;

from src.domain.api_exception import ApiException

class CreateViewsDashboardUseCase(GenericUseCase):
    def __init__(self,file: UploadFile) -> None:
        self.file = file
        paths_usecase: PathsIsmartUseCase = PathsIsmartUseCase()
        self.path_ismart_views = paths_usecase.get_root_path_ismar_home_assintant_principal_views()

       

    async def execute(self) -> pd.DataFrame:
        try:

            df_views =  pd.DataFrame()
            tranform_file_to_dataframe_usecase:TransformFileToDataFrameUseCase =  TransformFileToDataFrameUseCase(self.file, SheetsNameExcelConfigISmart.AreasSK.value)
            dataframe_areas = await tranform_file_to_dataframe_usecase.execute()

           
            df_views =dataframe_areas[(dataframe_areas[ColumnsNameExcelConfigISmart.Colocar_Area_en_Dashboard_Views.value] == 'SI')] 
            
            if  df_views.empty:
                raise Exception("Erro al crear las Views, Revisar el excel de configuración: " + SheetsNameExcelConfigISmart.AreasSK.value + " debe haber valores con valor SI en la columna" + ColumnsNameExcelConfigISmart.Colocar_Area_en_Dashboard_Views.value )
                
            df_views = df_views.sort_values(by=[ColumnsNameExcelConfigISmart.Orden_en_DashBoard_Views.value])  
            print(df_views)  
            
            
            #3. Crear el Dashboard admin
            #4. Crear el Dashboar del Plano
            #name_file =  'pruebal.yaml'
            #dict_view_admin = self.build_dict_views(df_views, "title_test", "icon_test")


            #YamlUtilUseCase.save_file_yaml(PathsIsmartUseCase.path_join_any_directores([path_save_yaml, name_file]),dict_view_admin )


            print("------------------2----------------------")
            return df_views
        except Exception as exception:
            print(exception)
            raise ErrorHandlingUtils.application_error("Erro al crear las Views, Revisar el excel de configuración: " + SheetsNameExcelConfigISmart.AreasSK.value + " " + str(exception) , exception)


    def build_dict_views(self, df: pd.DataFrame, title: str, icon: str) -> dict:
        data = {}

        if df.empty:
            return data

        data = {
            'title': title,
            'path': self.build_path_view(title),
            'icon': icon,
            'cards': []
        }

        data_vertical_stack = {
            'type': 'vertical-stack',
            'cards': []
        }

        path_save_yaml = PathsIsmartUseCase.path_join_any_directores([self.path_ismart_views,'Zonas', zona, 'Integraciones'])

        YamlUtilUseCase.save_file_yaml(PathsIsmartUseCase.path_join_any_directores([path_save_yaml, name_file]),dict_df_switches_by_zone )

        
        return data
    

    def build_dict_card_esh_welcome_with_paths():
        data = {}

        return data

    
    def build_dict_group_switch(self, df: pd.DataFrame, name_group: str) -> dict:

   
        data = {}

        if df.empty:
            return data


        data = {
            'switch': [
                {
                    'platform': 'group',
                     'name': name_group,
                    'entities': []
                }
            ]
        }

        for final_id in df['final_id']:
            data['switch'][0]['entities'].append(final_id.replace(" ", ""))


        return data

    def build_path_view(self, text:str):
        
        path = StringUtilUseCase.convert_string_lower_case(text)
        path = StringUtilUseCase.replace_string(path, " ", "_")
        return path