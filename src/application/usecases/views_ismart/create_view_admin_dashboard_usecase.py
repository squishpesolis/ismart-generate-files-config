import typing
import pandas as pd
import yaml



from src.application.usecases.interfaces import GenericUseCase
from src.application.utils.error_handling_utils import ErrorHandlingUtils

from src.application.usecases.utils.paths_usecase import PathsIsmartUseCase
from src.application.usecases.utils.yaml_util_usecase import YamlUtilUseCase
from src.application.usecases.utils.dataframe_util_usecase import DataFrameUtilUseCase

from src.application.usecases.views_ismart.utils_views_usecase import Utils_Views_Usecase
from src.application.usecases.views_ismart.create_custom_components_views_usecase import CreateCustomComponentsViewsUsecase



from src.application.usecases.utils.folder_creator_usecase import FolderCreator

from src.application.usecases.enums.names_columns_excel_ismart_configuration_enum import ColumnsNameExcelConfigISmart
from src.application.usecases.enums.names_sheet_excel_ismart_configuration_enum import SheetsNameExcelConfigISmart;

from src.domain.api_exception import ApiException



class CreateViewAdminDashboardUseCase(GenericUseCase):
    def __init__(self,dataframe_areas: pd.DataFrame, configurar_con_entidades_demos: bool) -> None:
        self.dataframe_areas = dataframe_areas
        self.configurar_con_entidades_demos = configurar_con_entidades_demos
        paths_usecase: PathsIsmartUseCase = PathsIsmartUseCase()
        self.path_ismart_views = paths_usecase.get_root_path_ismar_home_assintant_principal_views()

       

    async def execute(self) -> pd.DataFrame:
        try:

            df_views_areas =  pd.DataFrame()
            dataframe_areas = self.dataframe_areas

       
           
            df_views_areas =dataframe_areas[(dataframe_areas[ColumnsNameExcelConfigISmart.Colocar_Area_en_Dashboard_Views.value] == 'SI')] 
            
            if  df_views_areas.empty:
                raise Exception("Erro al crear la vista Admin, Revisar el excel de configuración: " + SheetsNameExcelConfigISmart.AreasSK.value + " debe haber valores con valor SI en la columna" + ColumnsNameExcelConfigISmart.Colocar_Area_en_Dashboard_Views.value )
                
            df_views_areas = df_views_areas.sort_values(by=[ColumnsNameExcelConfigISmart.Orden_en_DashBoard_Views.value])  
            

            self.build_dashboard_admin("Casa Administrador","mdi:home-account",df_views_areas )          
            
            
            #3. Crear el Dashboard admin
            #4. Crear el Dashboar del Plano
            #name_file =  'pruebal.yaml'
            #dict_view_admin = self.build_dict_views(df_views_areas, "title_test", "icon_test")


            #YamlUtilUseCase.save_file_yaml(PathsIsmartUseCase.path_join_any_directores([path_save_yaml, name_file]),dict_view_admin )


            print("------------------2----------------------")
            return df_views_areas
        except Exception as exception:
            print(exception)
            raise ErrorHandlingUtils.application_error("Erro al crear las Views, Revisar el excel de configuración: " + SheetsNameExcelConfigISmart.AreasSK.value + " " + str(exception) , exception)


    
    def build_dashboard_admin(self,title_dashboard, icon, df_areas: pd.DataFrame):
        
        view_admin = [
            {
                'title': title_dashboard,
                'path':  Utils_Views_Usecase.build_path_view(title_dashboard),
                'icon': icon,
                'cards': []
            }
        ]



        vertical_stack_left = self.build_vertical_stack_left(df_areas)

        #vertical_stack_center = Utils_Views_Usecase.create_vertical_stack()
        #vertical_stack_right = Utils_Views_Usecase.create_vertical_stack()


        view_admin[0]['cards'].append(vertical_stack_left)
        #view_admin['cards'].append(vertical_stack_center)
        #view_admin['cards'].append(vertical_stack_right)

   

     
        path_save_yaml = self.path_ismart_views
        FolderCreator.execute(path_save_yaml)

        YamlUtilUseCase.save_file_yaml(PathsIsmartUseCase.path_join_any_directores([path_save_yaml, 'prueba.yaml']),view_admin )

        #path_save_yaml = PathsIsmartUseCase.path_join_any_directores([self.path_ismart_views,'Zonas', zona, 'Integraciones'])

        #YamlUtilUseCase.save_file_yaml(PathsIsmartUseCase.path_join_any_directores([path_save_yaml, name_file]),dict_df_switches_by_zone )


    def build_vertical_stack_left(self, df_areas: pd.date_range) -> dict:
        vertical_stack_left_new = {}
        vertical_stack_left_new = Utils_Views_Usecase.create_vertical_stack()
        
       
        entity_2_name = DataFrameUtilUseCase.get_value_dataframe_from_position_row_and_name_colum(0, ColumnsNameExcelConfigISmart.Sub_Zona, df_areas, 'Areas')
        entity_3_name = DataFrameUtilUseCase.get_value_dataframe_from_position_row_and_name_colum(1, ColumnsNameExcelConfigISmart.Sub_Zona, df_areas, 'Areas')
        entity_4_name = DataFrameUtilUseCase.get_value_dataframe_from_position_row_and_name_colum(2, ColumnsNameExcelConfigISmart.Sub_Zona, df_areas, 'Areas')
        entity_5_name = DataFrameUtilUseCase.get_value_dataframe_from_position_row_and_name_colum(3, ColumnsNameExcelConfigISmart.Sub_Zona, df_areas, 'Areas')

        entity_2_icon = DataFrameUtilUseCase.get_value_dataframe_from_position_row_and_name_colum(0, ColumnsNameExcelConfigISmart.Icono_en_el_Dashboard_Views, df_areas, 'Areas')
        entity_3_icon = DataFrameUtilUseCase.get_value_dataframe_from_position_row_and_name_colum(1, ColumnsNameExcelConfigISmart.Icono_en_el_Dashboard_Views, df_areas, 'Areas')
        entity_4_icon = DataFrameUtilUseCase.get_value_dataframe_from_position_row_and_name_colum(2, ColumnsNameExcelConfigISmart.Icono_en_el_Dashboard_Views, df_areas, 'Areas')
        entity_5_icon = DataFrameUtilUseCase.get_value_dataframe_from_position_row_and_name_colum(3, ColumnsNameExcelConfigISmart.Icono_en_el_Dashboard_Views, df_areas, 'Areas')

        
        entity_2_nav = Utils_Views_Usecase.build_path_view(entity_2_name)
        entity_3_nav = Utils_Views_Usecase.build_path_view(entity_3_name)
        entity_4_nav = Utils_Views_Usecase.build_path_view(entity_4_name)
        entity_5_nav = Utils_Views_Usecase.build_path_view(entity_5_name)

        build_welcome_card = CreateCustomComponentsViewsUsecase.create_card_esh_welcome(
                                'minimalist_dropdown', 'openweathermap',
                                'plano-tercera-planta', 'mdi:home','Plano',
                                entity_2_nav, entity_2_icon,entity_2_name,
                                entity_3_nav, entity_3_icon,entity_3_name,
                                entity_4_nav, entity_4_icon,entity_4_name,
                                entity_5_nav, entity_5_icon,entity_5_name
        )

        build_card_title = CreateCustomComponentsViewsUsecase.create_card_title('Sistema')
        build_card_generic_sistema = CreateCustomComponentsViewsUsecase.create_card_generic('sensor.uptime', 'I-SMART UP', 'mdi:home-assistant')


        vertical_stack_left_new = Utils_Views_Usecase.add_card_to_verticaL_stack(vertical_stack_left_new, build_welcome_card)
        vertical_stack_left_new = Utils_Views_Usecase.add_card_to_verticaL_stack(vertical_stack_left_new, build_card_title)
        vertical_stack_left_new = Utils_Views_Usecase.add_card_to_verticaL_stack(vertical_stack_left_new, build_card_generic_sistema)

        # Buil group of switchs


        return vertical_stack_left_new

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

