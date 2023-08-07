import typing
import pandas as pd
import yaml
import numpy as np



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
from src.application.usecases.enums.name_column_df_group import NameColumnDfGroupEnum
from src.application.usecases.enums.name_views_ismart_enum import NameViewsIsmarEnum

from src.domain.api_exception import ApiException



class CreateViewAdminDashboardUseCase(GenericUseCase):
    def __init__(self,
                 dataframe_areas: pd.DataFrame, 
                 configurar_con_entidades_demos: bool,
                 df_switches_by_zone_and_light: pd.DataFrame,
                 df_switches_by_ubication_and_light: pd.DataFrame,
                 df_switches_by_areas_and_light: pd.DataFrame,
                 df_personas: pd.DataFrame,
                 df_scenes: pd.DataFrame,
                df_groups_sensor_temperature_by_zones: pd.DataFrame,
                df_groups_sensor_temp_by_ubi: pd.DataFrame,
                df_groups_sensor_temp_by_area: pd.DataFrame,
                df_groups_sensor_humedad_by_zones: pd.DataFrame,
                df_groups_sensor_humedad_by_ubi: pd.DataFrame,
                df_groups_sensor_humedad_by_area: pd.DataFrame,
                df_groups_covers_by_zones: pd.DataFrame,
                df_groups_covers_by_ubication: pd.DataFrame,
                df_groups_cover_by_area: pd.DataFrame) -> None:
        
        self.dataframe_areas = dataframe_areas
        self.configurar_con_entidades_demos = configurar_con_entidades_demos
        paths_usecase: PathsIsmartUseCase = PathsIsmartUseCase()
        self.path_ismart_views = paths_usecase.get_root_path_ismar_home_assintant_principal_views()
        self.df_switches_by_zone_and_light = df_switches_by_zone_and_light
        self.df_switches_by_ubication_and_light = df_switches_by_ubication_and_light
        self.df_switches_by_areas_and_light = df_switches_by_areas_and_light
        self.df_personas = df_personas
        self.df_scenes = df_scenes

        self.df_groups_sensor_temperature_by_zones = df_groups_sensor_temperature_by_zones
        self.df_groups_sensor_temp_by_ubi = df_groups_sensor_temp_by_ubi
        self.df_groups_sensor_temp_by_area = df_groups_sensor_temp_by_area

        self.df_groups_sensor_humedad_by_zones = df_groups_sensor_humedad_by_zones
        self.df_groups_sensor_humedad_by_ubi = df_groups_sensor_humedad_by_ubi
        self.df_groups_sensor_humedad_by_area = df_groups_sensor_humedad_by_area
        

        self.df_groups_covers_by_zones = df_groups_covers_by_zones
        self.df_groups_covers_by_ubication = df_groups_covers_by_ubication
        self.df_groups_cover_by_area = df_groups_cover_by_area
       

    async def execute(self) -> pd.DataFrame:
        try:

            df_views_areas =  pd.DataFrame()
            dataframe_areas = self.dataframe_areas

       
           
            df_views_areas =dataframe_areas[(dataframe_areas[ColumnsNameExcelConfigISmart.Colocar_Area_en_Dashboard_Views.value] == 'SI')] 
            
            if  df_views_areas.empty:
                raise Exception("Erro al crear la vista Admin, Revisar el excel de configuración: " + SheetsNameExcelConfigISmart.AreasSK.value + " debe haber valores con valor SI en la columna" + ColumnsNameExcelConfigISmart.Colocar_Area_en_Dashboard_Views.value )
                
            df_views_areas = df_views_areas.sort_values(by=[ColumnsNameExcelConfigISmart.Orden_en_DashBoard_Views.value])  
            

            self.build_dashboard_admin("Casa Administrador","mdi:home-account",df_views_areas, 
                                       self.df_switches_by_zone_and_light,
                                       self.df_switches_by_ubication_and_light,
                                       self.df_switches_by_areas_and_light,
                                       self.df_personas,
                                       self.df_scenes,
                                       self.df_groups_sensor_temperature_by_zones,
                                       self.df_groups_sensor_temp_by_ubi,
                                       self.df_groups_sensor_temp_by_area,
                                       self.df_groups_sensor_humedad_by_zones,
                                       self.df_groups_sensor_humedad_by_ubi,
                                       self.df_groups_sensor_humedad_by_area,
                                       self.df_groups_covers_by_zones,
                                       self.df_groups_covers_by_ubication,
                                       self.df_groups_cover_by_area)          
            
            
            #3. Crear el Dashboard admin
            #4. Crear el Dashboar del Plano
            #name_file =  'pruebal.yaml'
            #dict_view_admin = self.build_dict_views(df_views_areas, "title_test", "icon_test")


            #YamlUtilUseCase.save_file_yaml(PathsIsmartUseCase.path_join_any_directores([path_save_yaml, name_file]),dict_view_admin )



            return df_views_areas
        except Exception as exception:

            raise ErrorHandlingUtils.application_error("Erro al crear las Views, Revisar el excel de configuración: " + SheetsNameExcelConfigISmart.AreasSK.value + " " + str(exception) , exception)


    
    def build_dashboard_admin(self,
                              title_dashboard, 
                              icon, 
                              df_areas: pd.DataFrame,
                              df_switches_by_zone_and_light:pd.DataFrame,
                              df_switches_by_ubication_and_light:pd.DataFrame,
                              df_switches_by_areas_and_light:pd.DataFrame,
                              df_personas:pd.DataFrame,
                              df_scenes:pd.DataFrame,
                              df_groups_sensor_temperature_by_zones:pd.DataFrame,
                              df_groups_sensor_temp_by_ubi:pd.DataFrame,
                              df_groups_sensor_temp_by_area:pd.DataFrame,
                              df_groups_sensor_humedad_by_zones:pd.DataFrame,
                              df_groups_sensor_humedad_by_ubi:pd.DataFrame,
                              df_groups_sensor_humedad_by_area:pd.DataFrame,
                              df_groups_covers_by_zones:pd.DataFrame,
                              df_groups_covers_by_ubication:pd.DataFrame,
                              df_groups_cover_by_area:pd.DataFrame
                              ):
        
        view_admin = [
            {
                'title': title_dashboard,
                'path':  Utils_Views_Usecase.build_path_view(title_dashboard),
                'icon': icon,
                'cards': []
            }
        ]



        vertical_stack_left = self.build_vertical_stack_left(df_areas,df_switches_by_zone_and_light,
                                                             df_switches_by_ubication_and_light,
                                                             df_switches_by_areas_and_light)

        vertical_stack_center = self.build_vertical_stack_center(df_personas,df_scenes)
        vertical_stack_right = self.build_vertical_stack_right(df_groups_sensor_temperature_by_zones,
                                                               df_groups_sensor_temp_by_ubi,
                                                               df_groups_sensor_temp_by_area,
                                                               df_groups_sensor_humedad_by_zones,
                                                               df_groups_sensor_humedad_by_ubi,
                                                               df_groups_sensor_humedad_by_area,
                                                               df_groups_covers_by_zones,
                                                               df_groups_covers_by_ubication,
                                                               df_groups_cover_by_area)


        view_admin[0]['cards'].append(vertical_stack_left)
        view_admin[0]['cards'].append(vertical_stack_center)
        view_admin[0]['cards'].append(vertical_stack_right)
        #view_admin[0]['cards'].append(vertical_stack_center)
        path_save_yaml = self.path_ismart_views
        FolderCreator.execute(path_save_yaml)

   

     
        path_save_yaml = self.path_ismart_views
        FolderCreator.execute(path_save_yaml)

        YamlUtilUseCase.save_file_yaml(PathsIsmartUseCase.path_join_any_directores([path_save_yaml, NameViewsIsmarEnum.admin_view.value]),view_admin )

        #path_save_yaml = PathsIsmartUseCase.path_join_any_directores([self.path_ismart_views,'Zonas', zona, 'Integraciones'])

        #YamlUtilUseCase.save_file_yaml(PathsIsmartUseCase.path_join_any_directores([path_save_yaml, name_file]),dict_df_switches_by_zone )


    def build_vertical_stack_left(self, 
                                  df_areas: pd.DataFrame, 
                                  df_switches_by_zone_and_light:pd.DataFrame,
                                  df_switches_by_ubication_and_light:pd.DataFrame,
                                  df_switches_by_areas_and_light:pd.DataFrame) -> dict:
        
        vertical_stack_left_new = {}
        vertical_stack_left_new = CreateCustomComponentsViewsUsecase.create_vertical_stack()
        
       
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

        
        build_card_group_switches_light_by_zone = CreateCustomComponentsViewsUsecase.create_card_entities(
            df_switches_by_zone_and_light[NameColumnDfGroupEnum.title.value].iloc[0],
            False,
            df_switches_by_zone_and_light
        )

        build_card_group_switches_light_by_ubi = CreateCustomComponentsViewsUsecase.create_card_entities(
            df_switches_by_ubication_and_light[NameColumnDfGroupEnum.title.value].iloc[0],
            False,
            df_switches_by_ubication_and_light
        )

        build_card_group_switches_light_by_area = CreateCustomComponentsViewsUsecase.create_card_entities(
            df_switches_by_areas_and_light[NameColumnDfGroupEnum.title.value].iloc[0],
            True,
            df_switches_by_areas_and_light
        )


        vertical_stack_left_new = Utils_Views_Usecase.add_card_to_verticaL_stack(vertical_stack_left_new, build_welcome_card)
        vertical_stack_left_new = Utils_Views_Usecase.add_card_to_verticaL_stack(vertical_stack_left_new, build_card_title)
        vertical_stack_left_new = Utils_Views_Usecase.add_card_to_verticaL_stack(vertical_stack_left_new, build_card_generic_sistema)
        vertical_stack_left_new = Utils_Views_Usecase.add_card_to_verticaL_stack(vertical_stack_left_new, build_card_group_switches_light_by_zone)
        vertical_stack_left_new = Utils_Views_Usecase.add_card_to_verticaL_stack(vertical_stack_left_new, build_card_group_switches_light_by_ubi)
        #vertical_stack_left_new = Utils_Views_Usecase.add_card_to_verticaL_stack(vertical_stack_left_new, build_card_group_switches_light_by_area)
        # Buil group of switchs
        


        return vertical_stack_left_new


    def build_vertical_stack_center(self, df_personas:pd.DataFrame, df_scenes:pd.DataFrame):
        vertical_stack_center_new = {}
        vertical_stack_center_new = CreateCustomComponentsViewsUsecase.create_vertical_stack()

        card_clock = CreateCustomComponentsViewsUsecase.create_card_clock()




        




        card_scenes = CreateCustomComponentsViewsUsecase.create_card_scenes_welcome(df_scenes)


        vertical_stack_center_new = Utils_Views_Usecase.add_card_to_verticaL_stack(vertical_stack_center_new, card_clock)

        df_splits_person = DataFrameUtilUseCase.split_data_frame_by_numbers_rows(df_personas,2)
        
        for df_person in df_splits_person:
            card_horizontal_person = {}
            card_horizontal_person = CreateCustomComponentsViewsUsecase.create_hotizontal_stack_with_list_persons(df_person)
            vertical_stack_center_new = Utils_Views_Usecase.add_card_to_verticaL_stack(vertical_stack_center_new, card_horizontal_person)


        vertical_stack_center_new = Utils_Views_Usecase.add_card_to_verticaL_stack(vertical_stack_center_new, card_scenes)

        return vertical_stack_center_new
       
    
    def build_vertical_stack_right(self, 
                                    df_groups_sensor_temperature_by_zones:pd.DataFrame,
                                    df_groups_sensor_temp_by_ubi:pd.DataFrame,
                                    df_groups_sensor_temp_by_area:pd.DataFrame,
                                    df_groups_sensor_humedad_by_zones:pd.DataFrame,
                                    df_groups_sensor_humedad_by_ubi:pd.DataFrame,
                                    df_groups_sensor_humedad_by_area:pd.DataFrame,
                                    df_groups_covers_by_zones:pd.DataFrame,
                                    df_groups_covers_by_ubication:pd.DataFrame,
                                    df_groups_cover_by_area:pd.DataFrame
                                    ):
        vertical_stack_new = {}
        vertical_stack_new = CreateCustomComponentsViewsUsecase.create_vertical_stack()

        card_weater = CreateCustomComponentsViewsUsecase.create_card_weather_openweathermap()

        card_temperature_humedity_view_zone = CreateCustomComponentsViewsUsecase.create_card_temperature_and_humedity_sensor(df_groups_sensor_temperature_by_zones,df_groups_sensor_humedad_by_zones)
        card_temperature_humedity_view_ubication = CreateCustomComponentsViewsUsecase.create_card_temperature_and_humedity_sensor(df_groups_sensor_temp_by_ubi,df_groups_sensor_humedad_by_ubi)

        


        build_card_group_covers_by_zone = CreateCustomComponentsViewsUsecase.create_card_entities(
            df_groups_covers_by_zones[NameColumnDfGroupEnum.title.value].iloc[0],
            False,
            df_groups_covers_by_zones
        )

        


        vertical_stack_new = Utils_Views_Usecase.add_card_to_verticaL_stack(vertical_stack_new, card_weater)
        vertical_stack_new = Utils_Views_Usecase.add_card_to_verticaL_stack(vertical_stack_new, card_temperature_humedity_view_zone)
        vertical_stack_new = Utils_Views_Usecase.add_card_to_verticaL_stack(vertical_stack_new, card_temperature_humedity_view_ubication)
        vertical_stack_new = Utils_Views_Usecase.add_card_to_verticaL_stack(vertical_stack_new, build_card_group_covers_by_zone)
        return vertical_stack_new


