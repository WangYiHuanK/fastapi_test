# -*- coding: utf-8 -*-
import io
import os
from contextlib import contextmanager
from functools import lru_cache
from io import StringIO
from dotenv.main import DotEnv
from pydantic import BaseSettings, Field
from typing import Optional


def my_get_stream(self):
    """重写python-dotenv读取文件的方法，使用utf-8，支持读取包含中文的.env配置文件"""
    if isinstance(self.dotenv_path, StringIO):
        yield self.dotenv_path
    elif os.path.isfile(self.dotenv_path):
        with io.open(self.dotenv_path, encoding='utf-8') as stream:
            yield stream
    else:
        if self.verbose:
            print("File doesn't exist %s", self.dotenv_path)
        yield StringIO('')


DotEnv._get_stream = contextmanager(my_get_stream)


class Settings(BaseSettings):
    """System configurations."""
    ENVIRONMENT: Optional[str] = Field(None, env="ENVIRONMENT")
    # API版本号
    API_VERSION_STR = "/api/v3"

    # token过期时间8小时
    ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 60 * 8

    # 算法
    ALGORITHM = "HS256"

    # 产品名称
    PRODUCTION_NAME = "gatherone_crm"

    # 允许访问的源
    ALLOW_ORIGINS = [
        '*'
    ]

    # 加载.env文件的配置
    class Config:
        env_file = ".env"
        case_sensitive = True


class DevConfig(Settings):
    """Development configurations."""

    # Mysql
    MYSQL_SERVER: Optional[str] = Field(None, env="DEV_MYSQL_SERVER")
    MYSQL_USER: Optional[str] = Field(None, env="DEV_MYSQL_USER")
    MYSQL_PASSWORD: Optional[str] = Field(None, env="DEV_MYSQL_PASSWORD")
    MYSQL_DB_NAME: Optional[str] = Field(None, env="DEV_MYSQL_DB_NAME")
    MYSQL_PORT: Optional[int] = Field(None, env="DEV_MYSQL_PORT")


class ProdConfig(Settings):
    """Production configurations."""

    # Mysql
    MYSQL_SERVER: Optional[str] = Field(None, env="PROD_MYSQL_SERVER")
    MYSQL_USER: Optional[str] = Field(None, env="PROD_MYSQL_USER")
    MYSQL_PASSWORD: Optional[str] = Field(None, env="PROD_MYSQL_PASSWORD")
    MYSQL_DB_NAME: Optional[str] = Field(None, env="PROD_MYSQL_DB_NAME")
    MYSQL_PORT: Optional[int] = Field(None, env="PROD_MYSQL_PORT")


class FactoryConfig:
    """Returns a config instance dependending on the ENV_STATE variable."""

    def __init__(self, env_state: Optional[str]):
        self.env_state = env_state

    def __call__(self):

        if self.env_state == "development":
            return DevConfig()

        elif self.env_state == "production":
            return ProdConfig()


@lru_cache()
def get_configs():
    """加载一下环境文件"""
    from dotenv import load_dotenv
    load_dotenv(encoding='utf-8')
    return FactoryConfig(Settings().ENVIRONMENT)()


configs = get_configs()
