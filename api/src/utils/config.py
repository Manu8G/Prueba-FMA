import yaml
from utils import path_repo
import logging
import os


class Config:
    def __init__(self, config_path=f"{path_repo}/FastAPI/config/config.yaml", secrets_path=f"{path_repo}/FastAPI/config/config-secret.yaml") -> None:
        try:
            logging.info("Loading Config File...")
            if os.path.exists(config_path):
                self.config = self.load_yaml(config_path)
            else:
                raise RuntimeError("Error: config.yaml not found")
            if os.path.exists(secrets_path):
                self.secrets = self.load_yaml(secrets_path)
            else:
                raise RuntimeError("Error: config-secret.yaml not found")
            self.combine_configs()

            logging.info("Loaded config successfully")
        except Exception as e:
            logging.error(str(e))

    def load_yaml(self, path):
        with open(path, 'r') as file:
            
            return yaml.safe_load(file)

    def combine_configs(self):
        self.config.update(self.secrets)

    def get(self, key, default=None):
        keys = key.split('.')
        value = self.config
        for k in keys:
            value = value.get(k, default)
            if value is default:
                break
        return value