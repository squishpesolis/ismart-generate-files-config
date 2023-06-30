from enum import Enum

class NamesPositionCardsISmartEnum(Enum):
    left = "LEFT"
    right = "RIGHT"
    center = "CENTER"

    


    def __str__(self):
        return str(self.value)