import pandas as pd

from common.mysql_init import read_mysql_config, create_mysql_connection

pandas_df = pd.read_csv("../../utils/downloader/data1.csv")
print(pandas_df.describe())

config = read_mysql_config("../../config/mysql_config.yml")
mysql_conn = create_mysql_connection(config)

# https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.to_sql.html
# from DataFrame to mysql table
pandas_df.to_sql("test_table1", mysql_conn, schema=None, if_exists="append")

res = mysql_conn.exec_driver_sql("SHOW tables;")
print(res.all())
