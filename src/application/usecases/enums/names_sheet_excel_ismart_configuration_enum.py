from enum import Enum
class SheetsNameExcelConfigISmart(Enum):
    AreasSK = "AreasSK"
    Entidades = "Entidades"
    Ubicacion = "Ubicacion"
    Personas = "Personas"
    Zona = "AreasSK"
    Domain = "Domain"
    Type = "Type"    

    def __str__(self):
        return str(self.value)