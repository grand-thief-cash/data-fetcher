import yaml
import MySQLdb


def read_mysql_config(file_path):
    with open(file_path, 'r') as file:
        config = yaml.safe_load(file)

    ip = config['mysql']['ip']
    port = config['mysql']['port']
    username = config['mysql']['username']
    password = config['mysql']['password']

    return ip, port, username, password


# 指定你的YAML文件路径
yaml_file = '../config/mysql_config.yml'

# 调用函数读取MySQL连接信息
mysql_ip, mysql_port, mysql_username, mysql_password = read_mysql_config(yaml_file)

# 打印读取到的连接信息
print(f"IP: {mysql_ip}")
print(f"Port: {mysql_port}")
print(f"Username: {mysql_username}")
print(f"Password: {mysql_password}")


def create_mysql_connection(ip, port, username, password):
    try:
        conn = MySQLdb.connect(
            host=ip,
            port=port,  # 将port参数转换为字符串类型
            user=username,
            passwd=str(password)
        )
        print('MySQL连接已成功建立！')
        return conn
    except MySQLdb.Error as e:
        print(f'无法连接到MySQL数据库：{e}')

    return None


# 使用之前读取到的连接信息创建MySQL连接
mysql_conn = create_mysql_connection(mysql_ip, mysql_port, mysql_username, mysql_password)
