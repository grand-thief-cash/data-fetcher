from typing import Dict

from pandas import DataFrame
from sqlalchemy import Engine

from common.drivers.mysql_driver import check_table_exists


class DataStorage:
    table_name: str
    engine_provider: lambda: Engine
    dtypes_override: Dict

    def __init__(self, table_name: str, engine_provider: lambda: Engine, dtypes_override: Dict):
        self.table_name = table_name
        self.engine_provider = engine_provider
        self.dtypes_override = dtypes_override

    def _get_engine(self) -> Engine:
        return self.engine_provider()

    def table_exists(self):
        return check_table_exists(self.table_name)

    def get(self, where: [str]) -> DataFrame:
        if not where:
            raise Exception('at least 1 where query')

        engine = self._get_engine()

        import pandas
        df = pandas.read_sql_query(f'SELECT * FROM {self.table_name} WHERE {" AND ".join(where)}', engine)
        return df

    def save(self, appends: DataFrame | None, updates: DataFrame | None, removes: DataFrame | None, key_columns: [str]):
        if not self.table_exists():
            if updates is not None or removes is not None or not updates:
                raise Exception('for new table, only support appends data')
            appends.to_sql(self.table_name, self._get_engine(), if_exists='fail', index=False,
                           dtype=self.dtypes_override)
        else:
            engine = self._get_engine()
            if len(appends) > 0:
                appends.to_sql(self.table_name, engine, if_exists='append', index=False)

            if len(updates) > 0:
                # raise Exception('not implemented')
                pass

            if len(removes) > 0:
                if len(key_columns) < 0:
                    raise Exception('need key_columns when remove')

                conn = engine.connect()
                for _, row in removes.iterrows():
                    wheres = []
                    for column in key_columns:
                        wheres.append(f"{column}='{row[column]}'")
                    sql = f"DELETE FROM {self.table_name} WHERE {' AND '.join(wheres)}"
                    conn.exec_driver_sql(sql)
