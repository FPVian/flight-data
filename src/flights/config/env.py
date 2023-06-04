from pathlib import Path
from dataclasses import dataclass
import os
from typing import Optional


@dataclass
class Environs:
    '''
    Use this class to create different combinations of settings for different environments.
    New environments can be created by adding a new entry in the environments dict.
    
    New groups and grouped dataclasses should be added to the defaults list for the appropriate environment(s).
    Don't forget to add new groups and dataclasses in settings.py.

    The '__self__' string is a placeholder for the Config class.
    '_self_' at the top of a list indicates that the settings in the Config class will be overwritten by other classes.
    Matching dictionaries will always be merged.
    '''
    environment_variable: str = 'SKYVIZ_ENV'
    project_root: Path = Path(__file__).resolve().parents[3]

    @property
    def env(self) -> Optional[str]:
        env = os.environ.get(self.environment_variable)
        if env is None:
            try:
                env = open(f'{self.project_root}/.env').read().strip()
            except FileNotFoundError:
                pass
        return env

    environments = {
        'default': [
            '_self_',
            {'general': 'general_dev'},
            {'db': 'sqlite'},
            {'api': 'api_dev'},
            {'api/adsb_exchange': 'adsb_exchange_dev'},
            {'logs': 'logs_dev'},
        ],

        'dev': [
            '_self_',
            {'general': 'general_dev'},
            {'db': 'postgres_docker'},
            {'api': 'api_dev'},
            {'api/adsb_exchange': 'adsb_exchange_dev'},
            {'logs': 'logs_dev'},
        ],

        'prod': [
            '_self_',
            {'general': 'general_prod'},
            {'db': 'postgres_docker'},
            {'api': 'api_prod'},
            {'api/adsb_exchange': 'adsb_exchange_prod'},
            {'logs': 'logs_prod'},
        ],

        'debug': [
            '_self_',
            {'general': 'general_dev'},
            {'db': 'postgres_docker'},
            {'api': 'api_dev'},
            {'api/adsb_exchange': 'adsb_exchange_dev'},
            {'logs': 'logs_debug'},
        ]
    }

    def defaults_list(self) -> list:
        defaults = self.environments['default']
        if self.env:
            defaults = self.environments[self.env]
        hydra_overrides = [
            {'override hydra/hydra_logging': 'none'},
            {'override hydra/job_logging': 'none'},
        ]
        defaults.extend(hydra_overrides)
        return defaults