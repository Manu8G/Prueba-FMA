import yaml
# from src.utils.utils import path_repo
import logging
import os


class Config:
    def __init__(self, config_path=f"/api/src/config/config.yaml", secrets_path=f"/api/src/config/config-secret.yaml") -> None:
        try:
            # {path_repo}
            logging.info("Loading Config File...")
            # self.config = {} 
            '''
            current_dir = os.path.dirname(os.path.abspath(__file__))  # El directorio actual del archivo
            config_path = os.path.join(current_dir, 'api', 'src', 'config', 'config.yaml')
            secrets_path = os.path.join(current_dir, 'api', 'src', 'config', 'config-secret.yaml')
            
            '''
            
            print("C INIT A1: "+ config_path)
            if os.path.exists(config_path):
                print("C INIT A2")
                self.config = self.load_yaml(config_path)
            else:
                print("C INIT A3")
                raise RuntimeError("Error: config.yaml not found")
            if os.path.exists(secrets_path):
                print("C INIT A4")
                self.secrets = self.load_yaml(secrets_path)
            else:
                print("C INIT A5")
                raise RuntimeError("Error: config-secret.yaml not found")
            self.combine_configs()
            print("C INIT A6")
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