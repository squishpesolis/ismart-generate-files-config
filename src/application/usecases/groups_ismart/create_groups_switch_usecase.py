import typing
import pandas as pd
import yaml
from src.application.usecases.interfaces import GenericUseCase
from src.application.utils.error_handling_utils import ErrorHandlingUtils
from src.domain.dog_fact import DogFactEntity


class CreateGroupsSwitchUseCase(GenericUseCase):
    def __init__(self, df: pd.DataFrame) -> None:
        self.df = df

    def execute(self) -> pd.DataFrame:
        try:

            zonas = self.df['zonas'].unique()

            for zona in zonas:
               

                # Filter domain switch by Zonas
                df_switches_by_zone = self.df[(self.df['zonas'] == zona) & (self.df['domain'] == 'switch')] 
                
                self.build_dict_group_switch(df_switches_by_zone)
                    
            # Metodo filtar DF por switch
            # Filtar por Zona GetUniqueValuesInColunmDataFrameUseCase
            # Armar el Yaml por zona
            # Guardar en un temporal los archivos
            # Filtar por Ubicacion GetUniqueValuesInColunmDataFrameUseCase
            # Armar el Yaml por Ubicacion
            # Filtar por Areas GetUniqueValuesInColunmDataFrameUseCase
             # Armar el Yaml por Areas
             
            return "Archivo Creado en la ruta"
        except Exception as exception:
            raise ErrorHandlingUtils.application_error("Cannot get all dog facts", exception)

    
    def build_dict_group_switch(self, df: pd.DataFrame) -> dict:

   
        data = {}

        if df['final_id'].empty:
            return data


        data = {
            'switch': [
                {
                    'platform': 'group',
                    'entities': []
                }
            ]
        }

        for final_id in df['final_id']:
            data['switch'][0]['entities'].append(final_id.replace(" ", ""))


        return data


        #print("The python dictionary is:")
        #print(data)
        #yaml_string=yaml.dump(data,sort_keys=False)
        #print("The YAML string is:")
        #print(yaml_string)