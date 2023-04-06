from src.domain.base_entity import BaseEntity


class ConfigISmarttEntity(BaseEntity):
    def __init__(self, 
                raiz: str, zonas: str, areas: str, location: str, domain: str, 
                type: str, number: str, nombre: str, technology: str, importance: str, 
                actual_id: str,nombre_actual: str, article: str, final_id: str, nombre_domain: str,
                tasmota_name: str, friendly_name: str, topic_mqtt: str, nombre_imagen_plano: str, path_imagen: str ) -> None:
        super().__init__()
        self.raiz = raiz
        self.zonas = zonas
        self.areas = areas
        self.location = location
        self.domain = domain

        self.type = type
        self.number = number
        self.nombre = nombre
        self.technology = technology
        self.importance = importance

        self.actual_id = actual_id
        self.nombre_actual = nombre_actual
        self.article = article
        self.final_id = final_id
        self.nombre_domain = nombre_domain

        self.tasmota_name = tasmota_name
        self.friendly_name = friendly_name
        self.topic_mqtt = topic_mqtt
        self.nombre_imagen_plano = nombre_imagen_plano
        self.path_imagen = path_imagen