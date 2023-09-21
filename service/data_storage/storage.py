from typing import Dict

from pandas import DataFrame
from sqlalchemy import Connection
from sqlalchemy.exc import ProgrammingError


class DataStorage:
    table_name: str
    connection_provider: lambda: Connection
    dtypes_override: Dict

    def __init__(self, table_name: str, connection_provider: lambda: Connection, dtypes_override: Dict):
        self.table_name = table_name
        self.connection_provider = connection_provider
        self.dtypes_override = dtypes_override

    def _get_connection(self) -> Connection:
        return self.connection_provider()

    def table_exists(self):
        conn = self._get_connection()
        try:
            resp = conn.exec_driver_sql(f"DESCRIBE TABLE {self.table_name}")
        except ProgrammingError as e:
            if e.code == 'f405':
                return False
            raise e
        finally:
            conn.close()

        return True

    def get(self, where: [str]) -> DataFrame:
        if not where:
            raise Exception('at least 1 where query')

        conn = self._get_connection()

        import pandas
        df = pandas.read_sql_query(f'SELECT * FROM {self.table_name} WHERE {" AND ".join(where)}', conn)
        return df

    def save(self, appends: DataFrame | None, updates: DataFrame | None, removes: DataFrame | None, key_columns: [str]):
        if not self.table_exists():
            assert updates is None
            assert removes is None
            assert appends is not None
            assert len(appends.columns) > 0
            self._create_new_table(appends)
        else:
            conn = self._get_connection()
            if len(appends) > 0:
                appends.to_sql(self.table_name, conn, if_exists='append', index=False)
            if len(updates) > 0:
                # raise Exception('not implemented')
                pass
            if len(removes) > 0:
                if len(key_columns) < 0:
                    raise Exception('need key_columns when remove')
                for _, row in removes.iterrows():
                    wheres = []
                    for column in key_columns:
                        wheres.append(f"{column}='{row[column]}'")
                    sql = f"DELETE FROM {self.table_name} WHERE {' AND '.join(wheres)}"
                    conn.exec_driver_sql(sql)
            conn.commit()
            conn.close()

    def _create_new_table(self, df):
        with self._get_connection() as conn:
            return df.to_sql(self.table_name, conn, if_exists='fail', index=False, dtype=self.dtypes_override)
