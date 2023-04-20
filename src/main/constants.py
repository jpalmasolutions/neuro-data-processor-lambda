import os
import yaml

CWD = os.getcwd()
CONFIG_PATH = f"{CWD}/src/resources/yaml/config.yaml"
with open(CONFIG_PATH, "r") as config_file:
    CONFIG: dict = yaml.load(config_file, Loader=yaml.SafeLoader)
