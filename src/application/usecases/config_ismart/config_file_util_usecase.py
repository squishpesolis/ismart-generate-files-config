
import yaml
import os.path
import pandas as pd

from src.application.usecases.utils.string_util_usecase import StringUtilUseCase

from src.application.usecases.enums.names_columns_excel_ismart_configuration_enum import ColumnsNameExcelConfigISmart
from src.application.usecases.enums.name_column_df_scene import NameColumnDfSceneEnum
from src.application.usecases.enums.name_column_df_configuration_file import NameColumnDfConfigurationFileEnum
from src.application.usecases.enums.entities_ismart_demos_enum import EntitiesIsmartDemosEnum
from src.application.usecases.enums.domain_entities_ismart_enum import DomainEntitiesIsmartEnum


class ConfigFileUtilUseCase():
    def __init__(self) -> None:
        pass
        

    @staticmethod
    def build_config_dict(name_house: str,
                        latitude: str,
                        longitude: str,
                        unit_system:str,
                        time_zone: str,
                        port_smart_home: int,
                        dns:str) -> dict:

        data = {
            'homeassistant': {
                'name': name_house,      
                'latitude': latitude,              
                'longitude': longitude,           
                'unit_system': unit_system,
                'time_zone': time_zone,
                'packages': {
                    'pack_1': '!include_dir_merge_named ismart/config/',
                    'pack_2': '!include_dir_merge_named ismart/servicios/',
                    'pack_3': '!include_dir_merge_named ismart/integraciones/'
                }
            },
            'frontend': {
                'development_repo': '/share/frontend',
                'themes': '!include_dir_merge_named themes'
            },
            'automation generales': '!include_dir_list ismart/automatizaciones/generales/',
            'automation principal': '!include_dir_list /ismart/principal/',
            'automation ui': '!include automations.yaml',
            'scene': '!include_dir_merge_list ismart/scenes/',
            'lovelace': {
                'mode': 'storage',
                'dashboards': {
                    'lovelace-yaml-optimized': {
                        'mode': 'yaml',
                        'title': 'FloorPlan',
                        'icon': 'mdi:home',
                        'show_in_sidebar': True,
                        'filename': 'www/ismart/planos/plano-main.yaml'
                    }
                }
            },
            'http': {},
            'default_config': '',
            'tts': [
                {
                    'platform': 'google_translate'
                }
            ],
            'script': '!include scripts.yaml'

        }

        if dns == 'GODADDY':
            data['http'] = {
                            'server_port': port_smart_home,
                            'ssl_certificate': '/ssl/fullchain.pem',
                            'ssl_key': '/ssl/privkey.pem'
                        }
        if dns == 'DUCKDNS':
            data['http'] = {
                            'use_x_forwarded_for': True,
                            'trusted_proxies': [
                                '172.30.33.0/24'
                            ],
                            'ip_ban_enabled': True,
                            'login_attempts_threshold': 5
                        }
                

        sensor1 = {'sensor1 prueba': 'value sensor'}

        data.update(sensor1)

        return data
    

    @staticmethod
    def build_df_empty_to_build_scenes():

        columnsName = [NameColumnDfSceneEnum.name_.value,
                       NameColumnDfSceneEnum.area.value,
                       NameColumnDfSceneEnum.icon.value,
                       NameColumnDfSceneEnum.domain.value,
                       NameColumnDfSceneEnum.entity.value,
                       NameColumnDfSceneEnum.value_.value,
                       NameColumnDfSceneEnum.orden_view.value
                       ]
         
        return pd.DataFrame(columns=columnsName)
    
    @staticmethod
    def build_df_empty_to_build_scenes_view():

        columnsName = [NameColumnDfSceneEnum.id.value,
                       NameColumnDfSceneEnum.name_.value,
                       NameColumnDfSceneEnum.icon.value,
                       NameColumnDfSceneEnum.orden_view.value,
                       NameColumnDfSceneEnum.area.value
                       ]
         
        return pd.DataFrame(columns=columnsName)