import threading

import yaml
from sqlalchemy import create_engine
from common.structs import mysql_config

mysql_conn = None
mysql_engine = None
lock = threading.Lock()


def read_mysql_config(file_path):
    with open(file_path, 'r') as file:
        config = yaml.safe_load(file)
    mysqlConfig = mysql_config.MysqlConfig()

    mysqlConfig.ip = config['mysql']['ip']
    mysqlConfig.port = config['mysql']['port']
    mysqlConfig.username = config['mysql']['username']
    mysqlConfig.password = config['mysql']['password']
    mysqlConfig.database = config['mysql']['database']
    mysqlConfig.pool_size = config['mysql']['pool_size']
    mysqlConfig.max_overflow = config['mysql']['max_overflow']
    mysqlConfig.pool_timeout = config['mysql']['pool_timeout']
    mysqlConfig.pool_recycle = config['mysql']['pool_recycle']

    return mysqlConfig

def create_mysql_engine(config):
    try:
        # 创建MySQL连接字符串，并指定mysqlclient作为驱动程序
        connection_string = f'mysql+mysqldb://{config.username}:{config.password}@{config.ip}:{config.port}/{config.database}'

        # 创建数据库引擎，配置连接池
        mysql_engine = create_engine(connection_string, pool_size=config.pool_size, max_overflow=config.max_overflow)

        print('MySQL is connected!')
        return mysql_engine
    except Exception as e:
        print(f'Cannot connect to mysql：{e}')

    return None


def init_connection(config_path):
    print("init MySQL")
    global mysql_engine
    if mysql_engine is None:
        with lock:
            if mysql_engine is None:
                config = read_mysql_config(config_path)
                mysql_engine = create_mysql_engine(config)


def get_connection():
    return mysql_engine.connect()


def get_engine():
    return mysql_engine
