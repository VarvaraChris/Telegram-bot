from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr

#храним названия словарей и направление на токен
class Settings(BaseSettings):
    bot_token: SecretStr
    model_config = SettingsConfigDict(env_file='src/.env', env_file_encoding='utf-8')

name_dict_eng = "Dictionaries/EngDict.json"
name_dict_ch = "Dictionaries/ChDict.json"

config = Settings()