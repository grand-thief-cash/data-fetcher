import json
from datetime import time

import common.consts.modules_and_index as module_name
from service.download.structs.sdk_download_task import object_decoder
from utils.reader.json_reader import read_json_file
import common.gtm_log as log
import utils.downloader.sdk_downloader as sdk_downloader
import common.mysql_init as mysql_init
import common.drivers.mysql_driver as mysql_driver


def run_task(task_config: str = ""):
    json_string = read_json_file(task_config)
    task = json.loads(json_string, object_hook=object_decoder)

    # validate mysql connection
    mysql_connection = mysql_init.get_connection()
    if mysql_connection is None:
        log.logError("task name: {}, mysql is not connected".format(task.task_name), module_name.MODULE_SERVICE_DOWNLOAD_TASK, "mysql_get_mysql_connection_failed")
        return

    # validate table is existed:
    log.logInfo("task name: {} method name: {} validating table existence".format(task.task_name, task.concrete_task.method_name), module_name.MODULE_SERVICE_DOWNLOAD_TASK, "check_table_existence")
    table_name = "{}_{}".format(task.concrete_task.module, task.concrete_task.method_name)
    isTableExisted = mysql_driver.check_table_exists(table_name)
    if not bool(isTableExisted):
        log.logWarning("task name: {} table name: {}  validating table existence".format(task.task_name, table_name), module_name.MODULE_SERVICE_DOWNLOAD_TASK, "check_table_existence")


    # data fetch
    log.logInfo("task name: {} method name: {} fetch started".format(task.task_name, task.concrete_task.method_name), module_name.MODULE_SERVICE_DOWNLOAD_TASK, "data_fetch_started")
    downloader = sdk_downloader.SDKDownloader()
    result = downloader.invoke(sdkName=task.concrete_task.module, sdkMethod=task.concrete_task.method_name, symbol="主板A股")
    log.logInfo("task name: {} method name: {} fetched: {}items, done!".format(task.task_name, task.concrete_task.method_name,
                                                                       len(result)), module_name.MODULE_SERVICE_DOWNLOAD_TASK, "data_fetch_done")
    # result.to_csv('test_insert_to_database.csv', index=False, encoding='utf8')
    print(result.describe())

    # data insert
    if result.to_sql("test_table1", mysql_connection, schema=None, if_exists="append"):
        print("Data inserted successfully.")
    else:
        print("Data insertion failed.")
    # res = mysql_connection.exec_driver_sql("commit;")
    res = mysql_connection.exec_driver_sql("SHOW tables;")
    print(res.all())

    time.sleep(10)