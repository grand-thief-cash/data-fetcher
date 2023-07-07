import yaml
from sqlalchemy import create_engine
from common.structs import mysql_config
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


# 指定你的YAML文件路径
yaml_file = '../config/mysql_config.yml'

# 调用函数读取MySQL连接信息
mysqlConfig = read_mysql_config(yaml_file)

# 打印读取到的连接信息
# print(mysqlConfig.timeout)


def create_mysql_connection(config):
    try:
        # 创建MySQL连接字符串，并指定mysqlclient作为驱动程序
        connection_string = f'mysql+mysqldb://{config.username}:{config.password}@{config.ip}:{config.port}/{config.database}'

        # 创建数据库引擎，配置连接池
        engine = create_engine(connection_string, pool_size=config.pool_size, max_overflow=config.max_overflow)

        # 建立数据库连接
        conn = engine.connect()

        print('MySQL连接已成功建立！')
        return conn
    except Exception as e:
        print(f'无法连接到MySQL数据库：{e}')

    return None


# 使用之前读取到的连接信息创建MySQL连接
mysql_conn = create_mysql_connection(mysqlConfig)
