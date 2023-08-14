import typing
import pandas as pd
import numpy as np
import yaml
from src.application.usecases.interfaces import GenericUseCase
from src.application.utils.error_handling_utils import ErrorHandlingUtils

from src.application.usecases.utils.paths_usecase import PathsIsmartUseCase;
from src.application.usecases.utils.yaml_util_usecase import YamlUtilUseCase
from src.application.usecases.utils.folder_creator_usecase import FolderCreator


from src.application.usecases.enums.domain_entities_ismart_enum import DomainEntitiesIsmartEnum
from src.application.usecases.enums.name_column_df_scene import NameColumnDfSceneEnum
from src.application.usecases.enums.entities_ismart_demos_enum import EntitiesIsmartDemosEnum
from src.application.usecases.enums.name_column_df_configuration_file import NameColumnDfConfigurationFileEnum


from src.application.usecases.config_ismart.config_file_util_usecase import ConfigFileUtilUseCase


class CreateConfigFileUseCase(GenericUseCase):
    def __init__(self, 
                 dataframe_config_file: pd.DataFrame,
                 dataframe_yamls_paths_created_groups: pd.DataFrame,
                 configurar_con_entidades_demos: bool) -> None:
        
        self.dataframe_config_file = dataframe_config_file
        self.dataframe_yamls_paths_created_groups = dataframe_yamls_paths_created_groups
        self.configurar_con_entidades_demos = configurar_con_entidades_demos
        paths_usecase: PathsIsmartUseCase = PathsIsmartUseCase()
        self.path_config_file = paths_usecase.get_root_path_ismar_home_assintant_config()

       

    async def execute(self):
        try:

            dataframe_yamls_paths_created_groups = self.dataframe_yamls_paths_created_groups
            path_save_yaml = PathsIsmartUseCase.path_join_any_directores([self.path_config_file])
            FolderCreator.execute(path_save_yaml)

          
            config_df = self.dataframe_config_file

            name_house_filter = np.where((config_df[NameColumnDfConfigurationFileEnum.configuration_.value]==NameColumnDfConfigurationFileEnum.nombre_casa.value))
            name_house = config_df.loc[name_house_filter] 

            latitud_filter = np.where((config_df[NameColumnDfConfigurationFileEnum.configuration_.value]==NameColumnDfConfigurationFileEnum.latitud.value))
            latitud = config_df.loc[latitud_filter] 

            longitud_filter = np.where((config_df[NameColumnDfConfigurationFileEnum.configuration_.value]== NameColumnDfConfigurationFileEnum.longitud.value))
            longitud = config_df.loc[longitud_filter]

            server_port_filter = np.where((config_df[NameColumnDfConfigurationFileEnum.configuration_.value]== NameColumnDfConfigurationFileEnum.serverPort.value))
            server_port = config_df.loc[server_port_filter] 

            time_zone_filter = np.where((config_df[NameColumnDfConfigurationFileEnum.configuration_.value]== NameColumnDfConfigurationFileEnum.timeZone.value))
            time_zone = config_df.loc[time_zone_filter] 

            dns_filter = np.where((config_df[NameColumnDfConfigurationFileEnum.configuration_.value]== NameColumnDfConfigurationFileEnum.dns.value))
            dns = config_df.loc[dns_filter] 


            msg_error = ""

            if name_house.empty:
                msg_error = msg_error + "En el excel, sección Configuracion, No existe la propiedad " + NameColumnDfConfigurationFileEnum.nombre_casa.value

            if latitud.empty:
                msg_error = msg_error + "En el excel, sección Configuracion, No existe la propiedad " + NameColumnDfConfigurationFileEnum.latitud.value

            if longitud.empty:
                msg_error = msg_error + "En el excel, sección Configuracion, No existe la propiedad " + NameColumnDfConfigurationFileEnum.longitud.value 


            if server_port.empty:
                msg_error = msg_error + "En el excel, sección Configuracion, No existe la propiedad " + NameColumnDfConfigurationFileEnum.serverPort.value 

            if time_zone.empty:
                msg_error = msg_error + "En el excel, sección Configuracion, No existe la propiedad " + NameColumnDfConfigurationFileEnum.timeZone.value 


            if dns.empty:
                msg_error = msg_error + "En el excel, sección Configuracion, No existe la propiedad " + NameColumnDfConfigurationFileEnum.dns.value 

            if msg_error != "":
                raise Exception(msg_error)

            name_house_value = name_house[NameColumnDfConfigurationFileEnum.valor.value].iloc[0]
            latitud_value = latitud[NameColumnDfConfigurationFileEnum.valor.value].iloc[0]
            longitud_value = longitud[NameColumnDfConfigurationFileEnum.valor.value].iloc[0]
            server_port_value = server_port[NameColumnDfConfigurationFileEnum.valor.value].iloc[0]
            time_zone_value = time_zone[NameColumnDfConfigurationFileEnum.valor.value].iloc[0]
            dns_value = dns[NameColumnDfConfigurationFileEnum.valor.value].iloc[0]

            """ msg_error_values= ""

            if name_house_value == "" or np.isnan(name_house_value):
                msg_error_values = msg_error_values + "En el excel, sección Configuracion, es necesario valor de la propiedad " + NameColumnDfConfigurationFileEnum.nombre_casa.value 
            
            if latitud_value == "" or np.isnan(latitud_value):
                msg_error_values = msg_error_values + "En el excel, sección Configuracion, es necesario valor de la propiedad " + NameColumnDfConfigurationFileEnum.latitud.value 
            
            if longitud_value == "" or np.isnan(longitud_value):
                msg_error_values = msg_error_values + "En el excel, sección Configuracion, es necesario valor de la propiedad " + NameColumnDfConfigurationFileEnum.longitud.value 

            if server_port_value == "" or np.isnan(server_port_value):
                msg_error_values = msg_error_values + "En el excel, sección Configuracion, es necesario valor de la propiedad " + NameColumnDfConfigurationFileEnum.serverPort.value 

            if time_zone_value == "" or np.isnan(time_zone_value):
                msg_error_values = msg_error_values + "En el excel, sección Configuracion, es necesario valor de la propiedad " + NameColumnDfConfigurationFileEnum.timeZone.value 

            if dns_value == "" or np.isnan(dns_value):
                msg_error_values = msg_error_values + "En el excel, sección Configuracion, es necesario valor de la propiedad " + NameColumnDfConfigurationFileEnum.dns.value 


            if msg_error_values != "":
                raise Exception(msg_error_values) """

            name_file_yaml =  "configuration.yaml"

            scconfiguration_dic =ConfigFileUtilUseCase.build_config_dict(name_house_value,
                        latitud_value,
                        longitud_value,
                        'metric',
                        time_zone_value,
                        server_port_value,
                        dns_value,
                        dataframe_yamls_paths_created_groups)

            yaml_content = self.recursive_dict_format(scconfiguration_dic)

            
            #yaml_str =str(scconfiguration_dic).replace("'", '')

            YamlUtilUseCase.save_file_yaml_string(PathsIsmartUseCase.path_join_any_directores([path_save_yaml, name_file_yaml]),yaml_content )
           
   
            
            

            
            
        
        except Exception as exception:
            raise ErrorHandlingUtils.application_error("Error al crear archivo de configuracion.yaml", exception)



    def recursive_dict_format(self, d, level=0):
        indentation = " " * (level * 2)
        output = ""
        for key, value in d.items():
            if isinstance(value, dict):
                output += f"{indentation}{key}:\n{self.recursive_dict_format(value, level + 1)}"
            elif isinstance(value, str) and value.startswith('!'):
                output += f"{indentation}{key}: {value}\n"
            else:
                output += f"{indentation}{key}: {value}\n"
        return output

        
  
