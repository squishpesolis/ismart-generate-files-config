from enum import Enum
# Nombre de los metodos de cards en CreateCustomComponentsViewsUsecase
class NamesCardsISmartEnum(Enum):
    create_card_clock = "create_card_clock"
    create_card_scenes_welcome = "create_card_scenes_welcome"
    card_group_switch_entities = "card_group_switch_entities"
    create_card_title_welcome_smart = "create_card_title_welcome_smart"
    create_card_list_of_notes = "create_card_list_of_notes"
    create_card_temperature_and_humedity_sensor = "create_card_temperature_and_humedity_sensor"
    create_card_cover = "create_card_cover"

    


    def __str__(self):
        return str(self.value)