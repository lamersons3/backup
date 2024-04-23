import json
import os

def load_config(file_path):
    with open(file_path, 'r') as f:
        config = json.load(f)

    for section in config:
        if isinstance(config[section], dict):  # chheck if dict
            for key, value in config[section].items():
                if isinstance(value, str) and value.startswith("${") and value.endswith("}"):
                    env_variable = value[2:-1]
                    if env_variable in os.environ:
                        config[section][key] = os.environ[env_variable]

    return config
