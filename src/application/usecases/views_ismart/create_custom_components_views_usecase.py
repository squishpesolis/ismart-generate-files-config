import pandas as pd

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
    def create_card_title(card_title_name: str):
        card_title = {
                        'type': 'custom:button-card',
                        'template': 'card_title',
                        'name': card_title_name  
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
        
        card_entities = {
                        'type': 'custom:button-card',
                        'title': title,
                        'show_header_toggle': show_header_toggle,
                        'entities': []
                    }
        
        for index, row in df.iterrows():
            

            new_entity ={
                        'entity': row['entity'],
                        'name': row['name'],
                        'icon': row['icon'],
                            'tap_action': {
                                'action': row['tap_action']
                            }
                        }
            card_entities['entities'].append(new_entity)


        return card_entities