import json

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
        log.logError("task name: {}, mysql is not connected".format(task.task_name))
        return

    # validate table is existed:
    log.logInfo("task name: {} method name: {} validating table existence".format(task.task_name, task.concrete_task.method_name))
    table_name = "{}_{}".format(task.concrete_task.module, task.concrete_task.method_name)
    isTableExisted = mysql_driver.check_table_exists(mysql_connection, table_name)
    if not bool(isTableExisted):
        log.logError("task name: {} table name: {}  validating table existence".format(task.task_name, table_name))


    # data fetch
    log.logInfo("task name: {} method name: {} fetch started".format(task.task_name, task.concrete_task.method_name))
    downloader = sdk_downloader.SDKDownloader()
    result = downloader.invoke(sdkName=task.concrete_task.module, sdkMethod=task.concrete_task.method_name)
    log.logInfo("task name: {} method name: {} fetched: {}items, done!".format(task.task_name, task.concrete_task.method_name,
                                                                       len(result)))

    # data insert
    mysql_driver.insertDataFrame2Table(connection=mysql_connection, table_name=table_name, data=result)
