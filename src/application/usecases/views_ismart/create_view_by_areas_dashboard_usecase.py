import typing
import pandas as pd
import yaml



from src.application.usecases.interfaces import GenericUseCase
from src.application.utils.error_handling_utils import ErrorHandlingUtils

from src.application.usecases.utils.paths_usecase import PathsIsmartUseCase
from src.application.usecases.utils.yaml_util_usecase import YamlUtilUseCase
from src.application.usecases.utils.dataframe_util_usecase import DataFrameUtilUseCase
from src.application.usecases.utils.string_util_usecase import StringUtilUseCase
from src.application.usecases.groups_ismart.groups_util_usecase import GroupsUtilUseCase

from src.application.usecases.views_ismart.utils_views_usecase import Utils_Views_Usecase
from src.application.usecases.views_ismart.create_custom_components_views_usecase import CreateCustomComponentsViewsUsecase



from src.application.usecases.utils.folder_creator_usecase import FolderCreator

from src.application.usecases.enums.names_columns_excel_ismart_configuration_enum import ColumnsNameExcelConfigISmart
from src.application.usecases.enums.names_sheet_excel_ismart_configuration_enum import SheetsNameExcelConfigISmart;
from src.application.usecases.enums.name_column_df_group import NameColumnDfGroupEnum
from src.application.usecases.enums.name_views_ismart_enum import NameViewsIsmarEnum
from src.application.usecases.enums.name_column_df_scene import NameColumnDfSceneEnum
from src.application.usecases.enums.domain_entities_ismart_enum import DomainEntitiesIsmartEnum
from src.application.usecases.enums.name_titles_ismart_enum import NameTitlesIsmartEnum
from src.application.usecases.enums.name_column_df_list_cards import NameColumnDfListCardsInView
from src.application.usecases.enums.name_column_df_cards_orden_in_view import NameColumnDfCardsOrderInView
from src.application.usecases.enums.names_cards_ismart_enum import NamesCardsISmartEnum
from src.application.usecases.enums.names_position_cards_ismart_enum import NamesPositionCardsISmartEnum

from src.domain.api_exception import ApiException



class CreateViewByAreasDashboardUseCase(GenericUseCase):
    def __init__(self,
                 dataframe_areas: pd.DataFrame, 
                 configurar_con_entidades_demos: bool,
                 df_switches_gropus_by_areas_and_light: pd.DataFrame,
                 df_personas: pd.DataFrame,
                 df_scenes: pd.DataFrame,
                 df_entidades: pd.DataFrame,
                 df_cards_orden_in_view: pd.DataFrame,
                 df_groups_sensor_temp_by_area: pd.DataFrame,
                 df_groups_sensor_humedad_by_area: pd.DataFrame) -> None:
        
        self.dataframe_areas = dataframe_areas
        self.configurar_con_entidades_demos = configurar_con_entidades_demos
        paths_usecase: PathsIsmartUseCase = PathsIsmartUseCase()
        self.path_ismart_views = paths_usecase.get_root_path_ismar_home_assintant_principal_views()
        self.df_switches_gropus_by_areas_and_light = df_switches_gropus_by_areas_and_light
        self.df_personas = df_personas
        self.df_scenes = df_scenes
        self.df_entidades = df_entidades
        self.df_cards_orden_in_view = df_cards_orden_in_view
        self.df_groups_sensor_temp_by_area = df_groups_sensor_temp_by_area
        self.df_groups_sensor_humedad_by_area = df_groups_sensor_humedad_by_area
        

       

    async def execute(self) -> pd.DataFrame:
        try:

            df_views_areas =  pd.DataFrame()
            dataframe_areas = self.dataframe_areas

       
           
            df_views_areas =dataframe_areas[(dataframe_areas[ColumnsNameExcelConfigISmart.Colocar_Area_en_Dashboard_Views.value] == 'SI')] 
            
            if  df_views_areas.empty:
                raise Exception("Erro al crear la vista Admin, Revisar el excel de configuración: " + SheetsNameExcelConfigISmart.AreasSK.value + " debe haber valores con valor SI en la columna" + ColumnsNameExcelConfigISmart.Colocar_Area_en_Dashboard_Views.value )
                
            df_views_areas = df_views_areas.sort_values(by=[ColumnsNameExcelConfigISmart.Orden_en_DashBoard_Views.value])  
            

            count: int = 3
            for index, area_row in df_views_areas.iterrows():

                title_dashboard = area_row[ColumnsNameExcelConfigISmart.Sub_Zona.value]
                name_view = self.buil_name_view(count,title_dashboard)
                icon_view = area_row[ColumnsNameExcelConfigISmart.Icono_en_el_Dashboard_Views.value]

                self.build_dashboard_by_view(title_dashboard,
                                             icon_view,
                                             name_view,
                                             area_row,
                                             self.df_switches_gropus_by_areas_and_light,
                                             self.df_personas,
                                             self.df_scenes,
                                             self.df_entidades,
                                             self.df_cards_orden_in_view,
                                             self.df_groups_sensor_temp_by_area,
                                             self.df_groups_sensor_humedad_by_area)   


                count = count +1 

            return df_views_areas
        except Exception as exception:

            raise ErrorHandlingUtils.application_error("Erro al crear las Views By Areas, Revisar el excel de configuración: " + SheetsNameExcelConfigISmart.AreasSK.value + " " + str(exception) , exception)


    
    def build_dashboard_by_view(self,
                              title_dashboard, 
                              icon, 
                              name_view,
                              area_row,
                              df_switches_gropus_by_areas_and_light:pd.DataFrame,
                              df_personas:pd.DataFrame,
                              df_scenes:pd.DataFrame,
                              df_entities:pd.DataFrame,
                              df_cards_orden_in_view:pd.DataFrame,
                              df_groups_sensor_temp_by_area:pd.DataFrame,
                              df_groups_sensor_humedad_by_area:pd.DataFrame):
        

        




        name_area = area_row[ColumnsNameExcelConfigISmart.Sub_Zona.value]

        df_scenes_by_area = self.df_scenes[(self.df_scenes[NameColumnDfSceneEnum.area.value] == name_area)] 
        #df_scenes_by_area.loc[df_scenes_by_area[NameColumnDfSceneEnum.] > 1990, 'First Season'] = 1


        df_switch_group_by_area = self.df_switches_gropus_by_areas_and_light[(self.df_switches_gropus_by_areas_and_light[NameColumnDfSceneEnum.name_.value] == name_area)] 
        #df_switch_group_by_area.loc[df_switch_group_by_area[NameColumnDfSceneEnum.] > 1990, 'First Season'] = 1
        

        df_switches_by_area = self.get_entities_by_area_and_domain(df_entities, name_area, DomainEntitiesIsmartEnum.switch.value)

  

        df_switch_formater_by_build_card = self.create_switches_entites(df_switches_by_area, name_area)

 
        df_switch_group_by_area.loc[df_switch_group_by_area[NameColumnDfGroupEnum.title.value] == NameTitlesIsmartEnum.luces_por_area.value , NameColumnDfGroupEnum.title.value] = NameTitlesIsmartEnum.luces.value + " " + name_area


        df_cards_orden_in_view_by_area =  df_cards_orden_in_view.loc[(df_cards_orden_in_view[NameColumnDfCardsOrderInView.area_sk.value] == name_area)]


        
        df_group_sensor_temp_by_area = df_groups_sensor_temp_by_area[(df_groups_sensor_temp_by_area[NameColumnDfSceneEnum.name_.value] == name_area)] 
        df_group_sensor_humedad_by_area = df_groups_sensor_humedad_by_area[(df_groups_sensor_humedad_by_area[NameColumnDfSceneEnum.name_.value] == name_area)] 
        
        df_group_sensor_temp_by_area.loc[df_group_sensor_temp_by_area[NameColumnDfGroupEnum.title.value] == NameTitlesIsmartEnum.temperatura_por_area.value , NameColumnDfGroupEnum.name_.value] = NameTitlesIsmartEnum.temperatura.value + " " + name_area
        df_group_sensor_humedad_by_area.loc[df_group_sensor_humedad_by_area[NameColumnDfGroupEnum.title.value] == NameTitlesIsmartEnum.humedad_por_area.value , NameColumnDfGroupEnum.name_.value] = NameTitlesIsmartEnum.humedad.value + " " + name_area

    

        vertical_stack_center,vertical_stack_left, vertical_stack_rigth = self.build_element_for_views(df_personas,
                                                             df_scenes_by_area,
                                                             df_switch_group_by_area,
                                                             df_switch_formater_by_build_card,
                                                             df_cards_orden_in_view_by_area,
                                                             df_group_sensor_temp_by_area,
                                                             df_group_sensor_humedad_by_area
                                                             )
        
        
        view_by_name = [
            {
                'title': title_dashboard,
                'path':  Utils_Views_Usecase.build_path_view(title_dashboard),
                'icon': icon,
                'cards': []
            }
        ]

        if self.check_if_vertical_stack_has_cards(vertical_stack_left):
            view_by_name[0]['cards'].append(vertical_stack_left)

        if self.check_if_vertical_stack_has_cards(vertical_stack_center):
            view_by_name[0]['cards'].append(vertical_stack_center)
        
        if self.check_if_vertical_stack_has_cards(vertical_stack_rigth):
            view_by_name[0]['cards'].append(vertical_stack_rigth)
        
        path_save_yaml = self.path_ismart_views
        FolderCreator.execute(path_save_yaml)
        YamlUtilUseCase.save_file_yaml(PathsIsmartUseCase.path_join_any_directores([path_save_yaml, name_view + ".yaml"]),view_by_name )


    def check_if_vertical_stack_has_cards(self, vertical_stack:dict):
        has_data = False
        if len(vertical_stack['cards']) > 0 :
            has_data = True
        return has_data


    def build_element_for_views(self, 
                                    df_personas:pd.DataFrame, 
                                    df_scenes:pd.DataFrame,
                                    df_scenes_by_area:pd.DataFrame,
                                    df_switch_formater_by_build_card:pd.DataFrame,
                                    df_cards_orden_in_view:pd.DataFrame,
                                    df_group_sensor_temp_by_area:pd.DataFrame,
                                    df_group_sensor_humedad_by_area:pd.DataFrame):
        
        vertical_stack_center_new = {}
        vertical_stack_center_new = CreateCustomComponentsViewsUsecase.create_vertical_stack()

        columnsName = [NameColumnDfListCardsInView.dict_cards.value,
                       NameColumnDfListCardsInView.order.value,
                       NameColumnDfListCardsInView.position.value,
                       NameColumnDfListCardsInView.area.value]
         
            
        df_list_cards = pd.DataFrame(columns=columnsName)

        df_cards_orden_in_view = df_cards_orden_in_view.drop_duplicates()

        #############################create_card_clock#########################################

        df_select_config_card_create_card_clock = self.get_config_cards_by_name_card_i_smart(df_cards_orden_in_view,NamesCardsISmartEnum.create_card_clock)
        
        card_clock = CreateCustomComponentsViewsUsecase.create_card_clock()

        list_card_clock = self.build_list_of_cards(df_select_config_card_create_card_clock,card_clock)
        if list_card_clock:
            df_list_cards =df_list_cards.append(list_card_clock, ignore_index=True)

        

        ###########################create_card_scenes_welcome###########################################
      
        df_select_config_card_scenes = self.get_config_cards_by_name_card_i_smart(df_cards_orden_in_view,NamesCardsISmartEnum.create_card_scenes_welcome)
        
        card_scenes = CreateCustomComponentsViewsUsecase.create_card_scenes_welcome(df_scenes)

        list_card_scenes = self.build_list_of_cards(df_select_config_card_scenes,card_scenes)
        if list_card_scenes:
            df_list_cards =df_list_cards.append(list_card_scenes, ignore_index=True)

                

        ############################card_group_switch_entities##########################################
        
        df_select_config_card_group_switch_entities = self.get_config_cards_by_name_card_i_smart(df_cards_orden_in_view,NamesCardsISmartEnum.card_group_switch_entities)
        

        card_group_switch_entities = CreateCustomComponentsViewsUsecase.create_card_entities(
            df_scenes_by_area[NameColumnDfGroupEnum.title.value].iloc[0],
            True,
            df_switch_formater_by_build_card
        )

        list_card_card_group_switch_entities = self.build_list_of_cards(df_select_config_card_group_switch_entities,card_group_switch_entities)
        if list_card_card_group_switch_entities:
            df_list_cards =df_list_cards.append(list_card_card_group_switch_entities, ignore_index=True)


        ##########################create_card_title_welcome_smart############################################
        
        df_select_config_card_title_welcome_smart = self.get_config_cards_by_name_card_i_smart(df_cards_orden_in_view,NamesCardsISmartEnum.create_card_title_welcome_smart)
        
        
        card_title_welcome_smart = CreateCustomComponentsViewsUsecase.create_card_title_welcome_smart()

        list_card_card_title_welcome_smart = self.build_list_of_cards(df_select_config_card_title_welcome_smart,card_title_welcome_smart)
        if list_card_card_title_welcome_smart:
            df_list_cards =df_list_cards.append(list_card_card_title_welcome_smart, ignore_index=True)


        #################################create_card_list_of_notes###################################       

       
        df_select_config_card_list_of_notes = self.get_config_cards_by_name_card_i_smart(df_cards_orden_in_view,NamesCardsISmartEnum.create_card_list_of_notes)
        
        card_list_of_notes = CreateCustomComponentsViewsUsecase.create_card_list_of_notes()

        list_card_list_of_notes = self.build_list_of_cards(df_select_config_card_list_of_notes,card_list_of_notes)
        if list_card_list_of_notes:
            df_list_cards =df_list_cards.append(list_card_list_of_notes, ignore_index=True)

        #################################create_card_temperature_and_humedity_sensor###################################      

        df_select_config_card_temperature_and_humedity_sensor = self.get_config_cards_by_name_card_i_smart(df_cards_orden_in_view,NamesCardsISmartEnum.create_card_temperature_and_humedity_sensor)
        
        card_temperature_and_humedity_sensor = CreateCustomComponentsViewsUsecase.create_card_temperature_and_humedity_sensor(df_group_sensor_temp_by_area,df_group_sensor_humedad_by_area)

        list_card_temperature_and_humedity_sensor = self.build_list_of_cards(df_select_config_card_temperature_and_humedity_sensor,card_temperature_and_humedity_sensor)
        if list_card_temperature_and_humedity_sensor:
            df_list_cards =df_list_cards.append(list_card_temperature_and_humedity_sensor, ignore_index=True)

        ##############################################################################################################      

        vertical_stack_center_new,vertical_stack_left_new, vertical_stack_right_new = self.add_cards_in_position(df_list_cards)

        return vertical_stack_center_new,vertical_stack_left_new, vertical_stack_right_new
    

    def get_config_cards_by_name_card_i_smart(self, df_cards_orden_in_view:pd.DataFrame, name_cards_i_smart:NamesCardsISmartEnum):

        return df_cards_orden_in_view.loc[
            (df_cards_orden_in_view[NameColumnDfCardsOrderInView.name_cards_i_smart.value] == name_cards_i_smart.value)]
        

    def add_cards_in_position(self, df_list_cards: pd.DataFrame ):
        vertical_stack_center_new = CreateCustomComponentsViewsUsecase.create_vertical_stack()
        vertical_stack_left_new  = CreateCustomComponentsViewsUsecase.create_vertical_stack()
        vertical_stack_right_new  = CreateCustomComponentsViewsUsecase.create_vertical_stack()
        df_list_cards = df_list_cards.sort_values(by=[NameColumnDfListCardsInView.order.value, NameColumnDfListCardsInView.area.value])

        for index, card_loop in df_list_cards.iterrows():

            position = card_loop[NameColumnDfListCardsInView.position.value]
            card = card_loop[NameColumnDfListCardsInView.dict_cards.value]
            hidden = card_loop[NameColumnDfListCardsInView.hidden.value]
            
            if hidden:
                continue
            

            if position == NamesPositionCardsISmartEnum.center.value:
                vertical_stack_center_new = Utils_Views_Usecase.add_card_to_verticaL_stack(vertical_stack_center_new, card)
            if position == NamesPositionCardsISmartEnum.left.value:
                vertical_stack_left_new = Utils_Views_Usecase.add_card_to_verticaL_stack(vertical_stack_left_new, card)
            if position == NamesPositionCardsISmartEnum.right.value:
                vertical_stack_right_new = Utils_Views_Usecase.add_card_to_verticaL_stack(vertical_stack_right_new, card)

        return vertical_stack_center_new,vertical_stack_left_new, vertical_stack_right_new
    

    def build_list_elements_view_by_area(self, 
                                    df_personas:pd.DataFrame, 
                                    df_scenes:pd.DataFrame,
                                    df_scenes_by_area:pd.DataFrame,
                                    df_switch_formater_by_build_card:pd.DataFrame,
                                    df_cards_orden_in_view:pd.DataFrame):

        columnsName = [NameColumnDfListCardsInView.dict_cards.value,
                       NameColumnDfListCardsInView.order.value,
                       NameColumnDfListCardsInView.position.value,
                       NameColumnDfListCardsInView.area.value]
         
            
        df_list_cards = pd.DataFrame(columns=columnsName)

        df_cards_orden_in_view = df_cards_orden_in_view.drop_duplicates()


        df_select_config_card_create_card_clock = df_cards_orden_in_view.loc[
            (df_cards_orden_in_view[NameColumnDfCardsOrderInView.name_cards_i_smart.value] == NamesCardsISmartEnum.create_card_clock.value)]
        

        
        card_clock = CreateCustomComponentsViewsUsecase.create_card_clock()

        list_card_clock = self.build_list_of_cards(df_select_config_card_create_card_clock,card_clock)
        if list_card_clock:
            df_list_cards =df_list_cards.append(list_card_clock, ignore_index=True)

        


        df_select_config_card_scenes = df_cards_orden_in_view.loc[
            (df_cards_orden_in_view[NameColumnDfCardsOrderInView.name_cards_i_smart.value] == NamesCardsISmartEnum.create_card_scenes_welcome.value)]
        
        card_scenes = CreateCustomComponentsViewsUsecase.create_card_scenes_welcome(df_scenes)

        list_card_scenes = self.build_list_of_cards(df_select_config_card_scenes,card_scenes)
        if list_card_scenes:
            df_list_cards =df_list_cards.append(list_card_scenes, ignore_index=True)

                

        #
        df_select_config_card_group_switch_entities = df_cards_orden_in_view.loc[
            (df_cards_orden_in_view[NameColumnDfCardsOrderInView.name_cards_i_smart.value] == NamesCardsISmartEnum.card_group_switch_entities.value)]
        
        
        card_group_switch_entities = CreateCustomComponentsViewsUsecase.create_card_entities(
            df_scenes_by_area[NameColumnDfGroupEnum.title.value].iloc[0],
            True,
            df_switch_formater_by_build_card
        )

        list_card_card_group_switch_entities = self.build_list_of_cards(df_select_config_card_group_switch_entities,card_group_switch_entities)
        if list_card_card_group_switch_entities:
            df_list_cards =df_list_cards.append(list_card_card_group_switch_entities, ignore_index=True)

    

        return df_list_cards
    
    def build_vertical_stack_right(self, ):
        vertical_stack_new = {}
        vertical_stack_new = CreateCustomComponentsViewsUsecase.create_vertical_stack()

        card_weater = CreateCustomComponentsViewsUsecase.create_card_weather_openweathermap()

        vertical_stack_new = Utils_Views_Usecase.add_card_to_verticaL_stack(vertical_stack_new, card_weater)

        return vertical_stack_new


    def buil_name_view(self,secuntial: int, name: str) -> str:
        num_secuntial  = str(secuntial).zfill(4)
        name_lower_case = StringUtilUseCase.convert_string_lower_case(name)
        final_name = num_secuntial + "_" + StringUtilUseCase.replace_string(name_lower_case," ","")
        return final_name
    
    def get_entities_by_area_and_domain(self, df_entities: pd.DataFrame, area:str,domain:str)-> pd.DataFrame:
        df_entities_result = df_entities[(df_entities[ColumnsNameExcelConfigISmart.areas.value] == area) & (df_entities[ColumnsNameExcelConfigISmart.domain.value] == domain)] 
        return df_entities_result 
    
    def create_switches_entites(self, df_entities:pd.DataFrame, name_area: str):

        
        df_switches_by_area_and_light = GroupsUtilUseCase.build_df_empty_to_build_groups()

        part_of_dataframe = df_entities[[ColumnsNameExcelConfigISmart.final_id.value, ColumnsNameExcelConfigISmart.friendly_name.value]].copy()
        
        for index, switch in part_of_dataframe.iterrows():
            name = switch[ColumnsNameExcelConfigISmart.friendly_name.value]
            final_id = switch[ColumnsNameExcelConfigISmart.final_id.value]
            row_df_switches = {
                                        NameColumnDfGroupEnum.title.value: name_area, 
                                        NameColumnDfGroupEnum.entity.value:final_id,
                                        NameColumnDfGroupEnum.name_.value:name, 
                                        NameColumnDfGroupEnum.icon.value:'mdi:lightbulb-group', 
                                        NameColumnDfGroupEnum.tap_action.value:'none'
                                                                }
        
            df_switches_by_area_and_light = df_switches_by_area_and_light.append(row_df_switches, ignore_index=True)

        return df_switches_by_area_and_light
    

    def build_list_of_cards(self, df:pd.DataFrame, dict_card: dict):
        list_cards = []
        for index, config_card_scenes in df.iterrows():
            row_df_list_cards = {}

            row_df_list_cards = {
                NameColumnDfListCardsInView.dict_cards.value: dict_card,
                NameColumnDfListCardsInView.order.value: config_card_scenes[NameColumnDfCardsOrderInView.order.value],
                NameColumnDfListCardsInView.position.value:config_card_scenes[NameColumnDfCardsOrderInView.position.value],
                NameColumnDfListCardsInView.area.value:config_card_scenes[NameColumnDfCardsOrderInView.area_sk.value],
                NameColumnDfListCardsInView.hidden.value:config_card_scenes[NameColumnDfCardsOrderInView.hidden.value]
            }
            list_cards.append(pd.Series(row_df_list_cards))
            
        return  list_cards