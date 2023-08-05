from sqlalchemy import inspect, MetaData, Table, Column, Integer, Float, String
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import declarative_base

from common import gtm_log as log


def check_table_exists(connection, tablename):
    inspector = inspect(connection)
    return tablename in inspector.get_table_names()


Base = declarative_base()


# deprecated func
def create_table(connection, tablename, fields):
    engine = connection.engine

    metadata = MetaData(bind=engine)
    table = Table(tablename, metadata)

    for field_name, field_type in fields.items():
        if field_type == 'int':
            column = Column(field_name, Integer)
        elif field_type == 'float':
            column = Column(field_name, Float)
        elif field_type == 'double':
            column = Column(field_name, Float)  # 使用 Float 类型表示 double
        elif field_type == 'string':
            column = Column(field_name, String)
        else:
            raise ValueError(f"Invalid field type: {field_type}")

        table.append_column(column)

    metadata.create_all()


def get_table_metadata(connection, table_name):
    metadata = MetaData()
    metadata.reflect(bind=connection)
    table = metadata.tables[table_name]
    return table


def insertDataFrame2Table(connection, table_name, data):
    df = data
    table_meta = get_table_metadata(connection, table_name)
    columns = [col for col in table_meta.columns.keys() if col != 'id']

    data_to_insert = []
    for _, row in df.iterrows():
        data = {col: row[col] for col in columns}
        data_to_insert.append(data)

    try:
        connection.execute(table_meta.insert().values(data_to_insert))
        connection.commit()
        log.logInfo("driver executed insertDataFrame2Table successfully, {} rows inserted".format(len(data)))
    except SQLAlchemyError as e:
        connection.rollback()
        log.logError("driver executed insertDataFrame2Table failed: {}".format(str(e)))
    finally:
        log.logInfo("driver executed insertDataFrame2Table done")
