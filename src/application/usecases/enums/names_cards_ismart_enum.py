from enum import Enum
# Nombre de los metodos de cards en CreateCustomComponentsViewsUsecase
class NamesCardsISmartEnum(Enum):
    create_card_clock = "create_card_clock"
    create_card_scenes_welcome = "create_card_scenes_welcome"
    card_group_switch_entities = "card_group_switch_entities"


    def __str__(self):
        return str(self.value)