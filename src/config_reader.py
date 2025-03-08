from pydantic_settings import BaseSettings
from pydantic import SecretStr

#храним названия словарей и направление на токен
class Settings(BaseSettings):
    bot_token: SecretStr

name_dict_eng = "Dictionaries/EngDict.json"
name_dict_ch = "Dictionaries/ChDict.json"

config = Settings()
