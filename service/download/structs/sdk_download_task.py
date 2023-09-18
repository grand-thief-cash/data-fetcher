
class ConcreteTask:
    def __init__(self, module, method_name, input_param, resp_fields, require_data_procession, storage):
        self.module = module
        self.method_name = method_name
        self.input_param = input_param
        self.resp_fields = resp_fields
        self.require_data_procession = require_data_procession

        # Create Storage object if available
        if storage:
            self.storage = Storage(**storage)
        else:
            self.storage = None


class Storage:
    def __init__(self, database_type, database_name, table_name, data_save_mode, fields_mapping_mode, fields_mapping, extra_fields):
        self.database_type = database_type
        self.database_name = database_name
        self.table_name = table_name
        self.data_save_mode = data_save_mode
        self.fields_mapping_mode = fields_mapping_mode
        self.fields_mapping = fields_mapping
        self.extra_fields = extra_fields


class Task:
    def __init__(self, task_name, concrete_task):
        self.task_name = task_name
        self.concrete_task = ConcreteTask(**concrete_task)


def object_decoder(obj):
    if 'task_name' in obj and 'concrete_task' in obj:
        return Task(obj['task_name'], obj['concrete_task'])
    return obj