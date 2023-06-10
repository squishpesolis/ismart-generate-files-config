class Utils_Views_Usecase():
    def __init__(self) -> None:
        pass
        

    @staticmethod
    def create_vertical_stack():
        verticaL_stack = {
                        'type': 'vertical-stack',
                        'cards': []
                        }
        return verticaL_stack
    
    @staticmethod
    def add_card_to_verticaL_stack(verticaL_stack:dict, card: dict):
        verticaL_stack['cards'].append(card)
        return verticaL_stack