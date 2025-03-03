from user_config import (
    DEFAULT_ENVIRONMENT,
    DATA_DIRECTORY_NAME,
    NEW_DRUG_APPROVALS_FILENAME,
)
from utils.config_loader import get_env_variable

ENV = get_env_variable("ENV", DEFAULT_ENVIRONMENT)


class BaseConfig:
    FILENAME_MAPPING = {
        'NEW_DRUG_APPROVALS_FILENAME': NEW_DRUG_APPROVALS_FILENAME,
    }


class LocalConfig(BaseConfig):
    ENV = 'local'
    DATA_DIR_NAME = DATA_DIRECTORY_NAME



def get_config():
    return LocalConfig()


CONFIG = get_config()