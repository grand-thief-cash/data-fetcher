import pandas as pd

from common.mysql_init import read_mysql_config, init_connection, get_connection

pandas_df = pd.read_csv("../../utils/downloader/data1.csv")
# pandas_df = pd.read_csv("../../service/download/test_insert_to_database.csv")

print(pandas_df.describe())

# config = read_mysql_config()
init_connection("../../config/mysql_config.yml")

mysql_conn = get_connection()

# https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.to_sql.html
# from DataFrame to mysql table
pandas_df.to_sql("test_table1", mysql_conn, schema=None, index=False, if_exists="replace")

res = mysql_conn.exec_driver_sql("SHOW tables;")
print(res.all())
res = mysql_conn.exec_driver_sql("SELECT COUNT(*) FROM test_table1;")
print(res.all())
