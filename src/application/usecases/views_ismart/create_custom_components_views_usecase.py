import pandas as pd

from src.application.usecases.enums.name_column_df_group import NameColumnDfGroupEnum
from src.application.usecases.enums.name_column_df_person import NameColumnDfPersonEnum
from src.application.usecases.enums.name_column_df_scene import NameColumnDfSceneEnum

from src.application.usecases.utils.string_util_usecase import StringUtilUseCase
class CreateCustomComponentsViewsUsecase():
    def __init__(self) -> None:
        pass
        

    @staticmethod
    def create_card_esh_welcome(input_boolean_triggers_update: str, weather:str,
                                entity_1_nav:str, entity_1_icon:str,entity_1_name:str,
                                entity_2_nav:str, entity_2_icon:str,entity_2_name:str,
                                entity_3_nav:str, entity_3_icon:str,entity_3_name:str,
                                entity_4_nav:str, entity_4_icon:str,entity_4_name:str,
                                entity_5_nav:str, entity_5_icon:str,entity_5_name:str):
        card_esh_welcome = {
                                'type': 'custom:button-card',
                                'template': 'card_esh_welcome',
                                'triggers_update': 'input_boolean.'+input_boolean_triggers_update,
                                'variables': {
                                    'ulm_card_esh_welcome_collapse': 'input_boolean.'+input_boolean_triggers_update,
                                    'ulm_weather': 'weather.' + weather,
                                    'ulm_language': 'es',
                                    'entity_1': {
                                        'nav': entity_1_nav,
                                        'icon': entity_1_icon,
                                        'name': entity_1_name,
                                        'color': 'blue'
                                    },
                                    'entity_2': {
                                        'nav': entity_2_nav,
                                        'icon': entity_2_icon,
                                        'name': entity_2_name,
                                        'color': 'green'
                                    },
                                    'entity_3': {
                                        'nav': entity_3_nav,
                                        'icon': entity_3_icon,
                                        'name': entity_3_name,
                                        'color': 'purple'
                                    },
                                    'entity_4': {
                                        'nav': entity_4_nav,
                                        'icon': entity_4_icon,
                                        'name': entity_4_name,
                                        'color': 'yellow'
                                    },
                                    'entity_5': {
                                        'nav': entity_5_nav,
                                        'icon': entity_5_icon,
                                        'name': entity_5_name,
                                        'color': 'red'
                                    }
                                }
                            }
        return card_esh_welcome

    @staticmethod
    def create_card_title(card_title_name: str, subtitle:str =""):
        card_title = {
                        'type': 'custom:button-card',
                        'template': 'card_title',
                        'name': card_title_name  
                    }
        if not subtitle == "":
            card_title['label'] = subtitle
        return card_title
    
    @staticmethod
    def create_card_title_welcome_smart():
        return CreateCustomComponentsViewsUsecase.create_card_title("Bienvenido a","ISMART")

    @staticmethod
    def create_card_list_of_notes(card_title_name: str = "Lista"):
        card_title = {
                        'type': 'shopping-list',
                        'title': card_title_name  
                    }
        return card_title
    
    @staticmethod
    def create_card_generic( entity: str, card_generic_name: str, card_generic_icon: str):
        card_generic = {
                        'type': 'custom:button-card',
                        'template': 'card_generic',
                        'entity': entity,
                        'variables': {
                            'ulm_card_generic_name': card_generic_name,
                            'ulm_card_generic_icon': card_generic_icon
                        }
                    }
        
        return card_generic

    @staticmethod
    def create_card_entities( title: str, show_header_toggle: bool, df: pd.DataFrame):
        
        if df.empty:
            return {}
        
        card_entities = {
                        'type': 'entities',
                        'title': title,
                        'show_header_toggle': show_header_toggle,
                        'entities': []
                    }
        
        
        for index, row in df.iterrows():
            

            new_entity ={
                        'entity': row[NameColumnDfGroupEnum.entity.value],
                        'name': row[NameColumnDfGroupEnum.name_.value],
                        'icon': row[NameColumnDfGroupEnum.icon.value],
                            'tap_action': {
                                'action': row[NameColumnDfGroupEnum.tap_action.value]
                            }
                        }
            card_entities['entities'].append(new_entity)

        return card_entities
    

    @staticmethod
    def create_vertical_stack():
        verticaL_stack = {
                        'type': 'vertical-stack',
                        'cards': []
                        }
        return verticaL_stack
    
    @staticmethod
    def create_hotizontal_stack_with_list_persons(df:pd.DataFrame):
        if df.empty:
            return {}
        
        cards = CreateCustomComponentsViewsUsecase.create_horizontal_stack()

        cards_persons = []

        for index, row in df.iterrows():
            
            cards_person = CreateCustomComponentsViewsUsecase.create_card_person(
                row[NameColumnDfPersonEnum.Persona.value],
                row[NameColumnDfPersonEnum.MostrarImagen.value],
                row[NameColumnDfPersonEnum.Icon.value],
                False)
            cards_persons.append(cards_person)

        cards['cards']  = cards_persons

        return cards

    @staticmethod
    def create_card_person(entity: str, ulm_card_person_use_entity_picture: bool,
                           ulm_card_person_icon: str, tap_action: bool):
        
        aux_entity = StringUtilUseCase.replace_string(entity," ","_")
        aux_entity = StringUtilUseCase.convert_string_lower_case(entity)
               
        person_entity = 'person.'+aux_entity

        card_entities = {
                        'type': 'custom:button-card',
                        'template': 'card_person',
                        'entity': person_entity,
                        'variables': {
                            'ulm_card_person_entity': person_entity,
                            'ulm_card_person_use_entity_picture': ulm_card_person_use_entity_picture,
                            'ulm_card_person_icon': ulm_card_person_icon
                        },
                        'tap_action': {
                            'action': tap_action
                        }
                    }
        
      
        return card_entities
    
    @staticmethod
    def create_horizontal_stack():
        stack = {
                        'type': 'horizontal-stack',
                        'cards': []
                        }
        return stack
    
    @staticmethod
    def create_card_clock():
        card = {
                    'type': 'custom:button-card',
                    'template': 'custom_card_nik_clock',
                    'variables': {
                        'ulm_custom_card_nik_clock_switch': 'input_boolean.menu_tablet',
                        'ulm_custom_card_nik_clock_switch_enable': 'false',
                    }
                }
        return card

    @staticmethod
    def create_card_scenes_welcome(df:pd.DataFrame):

        colors = ['yellow','purple','blue','red','pink']

        card = {
                    'type': 'custom:button-card',
                    'template': 'card_scenes_welcome',
                    'variables': {}
                }

        counter = 1
        for index, scene in df.iterrows():

            #   counter > 5 ya que estas son las scenas por defecto  
            if counter > 5 :
                break

            entity_id = 'scene.' + scene[NameColumnDfSceneEnum.id.value]
            icon = scene[NameColumnDfSceneEnum.icon.value]
            name = scene[NameColumnDfSceneEnum.name_.value]
            color = colors[counter - 1]
            build_entitiy = {"entity_"+str(counter): {
                                'entity_id': entity_id,
                                'icon': icon,
                                'name': name,
                                'color': color
                            }}
            
            card['variables'].update(build_entitiy)
            counter = counter + 1
        

        return card
    
    @staticmethod
    def create_card_weather_openweathermap():
        card = {
                    'type': 'custom:button-card',
                    'template': 'card_weather',
                    'entity': 'weather.openweathermap',
                    'tap_action': {
                        'action': 'none'
                    },
                    'variables': {
                        'ulm_card_weather_name': '',
                        'ulm_card_weather_primary_info': ['wind_speed','precipitation_probability'],
                        'ulm_card_weather_backdrop': {
                            'fade': True
                        },
                    }
                }
        return card

    @staticmethod
    def create_card_temperature_and_humedity_sensor(df_temp:pd.DataFrame, df_hum:pd.DataFrame):
        if df_temp.empty & df_hum.empty:
            return {}
        
        data ={
            'type': 'horizontal-stack',
            'cards': []
        }

        list_vertical_stack = []

        vertical_stack_temp = CreateCustomComponentsViewsUsecase.create_vertical_stack()
        vertical_stack_humed = CreateCustomComponentsViewsUsecase.create_vertical_stack()

        if not df_temp.empty:
                        
            list_cards_temp = []

            for index, temp in df_temp.iterrows():

                cards_temp = CreateCustomComponentsViewsUsecase.create_card_generic(
                temp[NameColumnDfGroupEnum.entity.value],
                temp[NameColumnDfGroupEnum.name_.value],
                temp[NameColumnDfGroupEnum.icon.value])

                list_cards_temp.append(cards_temp)
            
            vertical_stack_temp['cards']  = list_cards_temp
            
            list_vertical_stack.append(vertical_stack_temp)

        if not df_hum.empty:
 
            list_cards_humed = []

            for index2, humed in df_hum.iterrows():

                cards_humed = CreateCustomComponentsViewsUsecase.create_card_generic(
                humed[NameColumnDfGroupEnum.entity.value],
                humed[NameColumnDfGroupEnum.name_.value],
                humed[NameColumnDfGroupEnum.icon.value])

                list_cards_humed.append(cards_humed)
            
            vertical_stack_humed['cards']  = list_cards_humed
            list_vertical_stack.append(vertical_stack_humed)

        data['cards'] = list_vertical_stack


        return data
    

    @staticmethod
    def create_cards_cover(df_covers: pd.DataFrame):
        
        if df_covers.empty:
            return {}
        
        card_cover = {
                        'type': 'custom:button-card',
                        'template': 'card_cover',
                        'entity': 'cover.'+'example',
                        'variables': {
                            'ulm_card_cover_enable_controls': 'true',
                            'ulm_card_cover_enable_slider': 'true',
                            'ulm_card_cver_favorite_percentage': '45',
                            'ulm_card_cover_color': 'green'
                        }
                    }
        return card_cover