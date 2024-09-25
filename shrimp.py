import json, os, datetime, inspect, typing

# Log Types
LOGTYPE_INFO = 'INFO'
LOGTYPE_WARN = 'WARNING'
LOGTYPE_ERROR = 'ERROR'
LOGTYPE_CRITICAL = 'CRITITCAL'

#Log color table
LOG_COLORS = {LOGTYPE_INFO : '\033[92m',
              LOGTYPE_WARN : '\033[93m',
              LOGTYPE_ERROR : '\033[91m',
              LOGTYPE_CRITICAL : '\033[91m'}

#Type constants
DATA_MODEL_TYPE_DATA_STACK = 'data_stack'
DATA_MODEL_TYPE_NORMAL = 'data_model'

class JSONDataStore():
    """Creates a new datastore in JSON format within the current directory.\n 
    If it exists, it will load it instead.
    If `disable_logs` is true then no logs will be shown with any operation on this datastore."""

    def __init__(self, file_name: str):
        self.data = {}
        self.metadata = {}
        self.backup_data = {}
        self.datastore_file = file_name + '.json'
        self.file_name = file_name

        #Data settings
        self.data_default_data = {}
        self.data_auto_update = True
        self.data_batch_limit = 20
        self.data_datastore_file_limit = 5 * 1024 * 1024

        #Setting variables
        self.setting_disable_logs = False
        self.setting_clear_logs_on_start = False

        current_dir = os.path.dirname(os.path.abspath(__file__))
        if os.path.exists(path=f'{current_dir}/{file_name}.json'):
            self.log(LOGTYPE_INFO, f'Loading datastore "{file_name}"')
            try:
                with open(f'{file_name}.json', 'r+') as datastore:
                    loaded_datastore = json.load(datastore)
                    self.data = loaded_datastore[f'{file_name}_data']
                    self.metadata = loaded_datastore[f'{file_name}_metadata']
            except Exception:
                self.log(LOGTYPE_CRITICAL, 'DATASTORE IS EMPTY, ATTEMPTING TO ROLL BACK')
                with open(self.datastore_file, 'w') as datastore:
                    json.dump({}, datastore)   
        else:
            with open(f'{file_name}.json', 'w') as datastore:
                self.log(LOGTYPE_INFO, f'Creating new datastore "{file_name}"')
                self.metadata = {
                        'created_time' : str(datetime.datetime.now()),
                        'last_modified' : str(datetime.datetime.now())
                        }
                self.update_datastore()

    def data_settings(self, default_data: dict={}, auto_update: bool=True, routine_check: bool=True):
        self.data_default_data = default_data
        self.data_auto_update = auto_update
        self.data_routine_check = routine_check

    def update_datastore(self):
        """Updates the current datastore if called from `Commit()` or the load innitilazation"""

        caller = inspect.stack()[1].function

        if caller == '__init__' or caller == 'Commit':
            with open(self.datastore_file, 'w') as f:
                self.metadata['last_modified'] = str(datetime.datetime.now())
                self.backup_data = self.data

                json.dump({f'{self.file_name}_metadata':self.metadata, f'{self.file_name}_data':self.data}, f, indent=2)
                self.log(LOGTYPE_INFO, 'Updated datastore')
            return

        else:   
            self.log(LOGTYPE_ERROR, f'DATA UPDATE CALL REJECTED, ATTEMPTED TO CALL FROM "{caller}"')
            return

    def new_data_model(self, data_model_key: str,default_data: dict=None):
        """Creates a new data model with a `data_model_key` and assigns it a default data of `default_data`"""

        if not default_data:
            default_data = self.data_default_data

        if data_model_key in self.data.keys():
            self.log(LOGTYPE_WARN, f'Data model "{data_model_key}" already exists, therefore not created')
            return
        
        self.log(LOGTYPE_INFO, f'Creating new data model with key "{data_model_key}"')

        data_model_metadata = {'status':'active','created_at':str(datetime.datetime.now()), 'type':DATA_MODEL_TYPE_NORMAL}

        self.data[data_model_key] = {f'{data_model_key}_metadata':data_model_metadata, f'{data_model_key}_data':default_data}
        self.log(LOGTYPE_INFO, f'Created data model')

    def delete_data_model(self, data_model_key: str):
        """Deletes a data model with the specified `data_model_key`"""

        if not data_model_key in self.data.keys(): 
            self.log(LOGTYPE_ERROR, f'Data model with key "{data_model_key}" was not found')
            return
        
        else:
            self.log(LOGTYPE_INFO, f'Deleting data model with key "{data_model_key}"')
            del self.data[data_model_key]
            self.log(LOGTYPE_INFO, 'Successfully deleted')

    def edit_data_model(self, data_model_key: str, new_data: dict):
        """Edit a data model with the new provided `new_data`"""

        if not data_model_key in self.data.keys(): 
            self.log(LOGTYPE_ERROR, f'Data model with key "{data_model_key}" was not found')
            return
        
        else:
            self.log(LOGTYPE_INFO, f'Editting data model with data key "{data_model_key}"')
            self.data[data_model_key][f'{data_model_key}_data'] = new_data
            self.log(LOGTYPE_INFO, 'Successfully editted')


    def get_data_model(self, data_model_key: str, get_metadata=False,pretty_print=False):
        """Returns a data model's current data"""

        self.log(LOGTYPE_INFO, f'Getting data model with data key "{data_model_key}"')

        if not data_model_key in self.data.keys():
            self.log(LOGTYPE_ERROR, f'Data model with data key "{data_model_key}" was not found')
            return
        self.log(LOGTYPE_INFO, 'Data model retrieved successfully')
        if not pretty_print: 
            if not get_metadata :return self.data[data_model_key][f'{data_model_key}_data']
            elif get_metadata: return self.data[data_model_key][f'{data_model_key}_metadata']
        else: return json.dumps(self.data[data_model_key], indent=3)

    def increment_data_model(self, data_model_key: str, entry_name: str, increment_value: int = 1):
        """Increases a data model's numeric data (if it has any) by `increment_value`"""

        if not data_model_key in self.data.keys():
            self.log(LOGTYPE_ERROR, f'Data model with data key "{data_model_key}" was not found')
            return
        
        data_model_data = self.data[data_model_key][f'{data_model_key}_data']

        if entry_name in data_model_data and type(data_model_data[entry_name]) == int:
            self.data[data_model_key][f'{data_model_key}_data'][entry_name] += increment_value

    def add_entry(self, data_model_key: str, entry_name: str, entry_value: any):
        if not data_model_key in self.data.keys():
            self.log(LOGTYPE_ERROR, f'Data model with data key "{data_model_key}" was not found')
            return
        if entry_name in self.data[data_model_key][f'{data_model_key}_data']:
            self.log(LOGTYPE_ERROR, f'Data entry with name "{entry_name}" already exists in data model "{data_model_key}"')
        else:
            self.data[data_model_key][f'{data_model_key}_data'][entry_name] = entry_value

    def edit_entry(self, data_model_key: str, entry_name: str, new_entry_value: any):
        if not data_model_key in self.data.keys():
            self.log(LOGTYPE_ERROR, f'Data model with data key "{data_model_key}" was not found')
            return
        if entry_name in self.data[data_model_key][f'{data_model_key}_data']:
            self.data[data_model_key][f'{data_model_key}_data'][entry_name] = new_entry_value

    def list_data_models(self, include_metadata=False):
        """Lists all data models, consider disabling logs to clearly see the data models."""
        print(f'All data models of datastore "{self.file_name}"')
        for data_index, data_model in enumerate(self.data):
            data_model_metadata = self.get_data_model(data_model, get_metadata=True)
            print(f'{data_index+1}. {data_model}')
            if include_metadata:
                print('-Status: ',data_model_metadata['status'])
                print('-Created at: ', data_model_metadata['created_at'])
    
    def batch_add_dm_single_value(self, batch_data_model_keys: list, single_default_data: dict=None):
        """Batch adds data models with the provided `single_default_data`"""

        if len(batch_data_model_keys) > self.data_batch_limit:
            self.log(LOGTYPE_WARN, f'Operation exceeds batch limit of {self.data_batch_limit}.')
            return
        
        for data_model in batch_data_model_keys:
            if data_model in self.data.keys():
                self.log(LOGTYPE_WARN, f'Data model "{data_model}" already exists, skipped')

            else:
                self.new_data_model(data_model, single_default_data)


    def batch_edit_dm_single_value(self, batch_data_model_keys: list, new_data: dict):
        """Batch edits data models in `batch_data_model_keys` if they exist and replace their data contens with `new_data`"""

        if len(batch_data_model_keys) > self.data_batch_limit:
            self.log(LOGTYPE_WARN, f'Operation exceeds batch limit of {self.data_batch_limit}.')
            return
        
        for data_model in batch_data_model_keys:
            if not data_model in self.data.keys():
                self.log(LOGTYPE_WARN, f'Data model "{data_model}" does not exist, skipped')
            else:
                self.data[data_model] = new_data


    def batch_delete_dm(self, batch_data_model_keys: str):
        """Batch delete data models"""

        if len(batch_data_model_keys) > self.data_batch_limit:
            self.log(LOGTYPE_WARN, f'Operation exceeds batch limit of {self.data_batch_limit}.')
            return
        
        for data_model in batch_data_model_keys:
            if data_model in self.data.keys():
                del self.data[data_model]
                self.log(LOGTYPE_INFO, f'Deleted data model "{data_model}"')
            else:
                self.log(LOGTYPE_WARN, f'Data model "{data_model}" does not exist, skipped')

    def batch_add_entries(self, batch_data_model_keys: list, entry_name: str, entry_value: any):
        """Batch adds entries in all of `batch_data_model_keys` with `entry_name` and `entry_value`"""

        if len(batch_data_model_keys) > self.data_batch_limit:
            self.log(LOGTYPE_WARN, f'Operation exceeds batch limit of {self.data_batch_limit}.')
            return
        
        for data_model in batch_data_model_keys:

            self.add_entry(data_model, entry_name, entry_value)

    def Commit(self):
        """Commit all changes made in `self.data` variable to the file."""

        self.log(LOGTYPE_INFO, f'DATA COMMIT CALLED FROM DATASTORE "{self.file_name}"')
        self.log(LOGTYPE_INFO, 'CHECKING DATASTORE INTEGRITY')

        try:
            with open(self.datastore_file) as f:
                json.load(f)
        except Exception:
            self.log(LOGTYPE_ERROR, '[COMMIT REJECTED] DATASTORE IS EMPTY. ATTEMPTING TO ROLLBACK')
            return
        
        self.log(LOGTYPE_INFO, 'DATASTORE IS FINE. CHECKING DATA')
        if self.data is None:
            self.log(LOGTYPE_ERROR, '[COMMIT REJECTED] DATA DOES NOT EXIST')
        else:
            self.log(LOGTYPE_INFO, 'DATA IS FINE. UPDATING DATASTORE')
            self.update_datastore()

    class data_stack:
        
        def __init__(self, datastore: 'JSONDataStore',data_stack_name, start_data, data_stack_type):
            self.main_datastore_data = datastore.data
            self.main_datastore_metadata = datastore.metadata
            self.datastore = datastore
            self.data: dict = start_data
            self.metadata = {'status':'active','created_at':str(datetime.datetime.now()), 'type':DATA_MODEL_TYPE_DATA_STACK}
            self.name = data_stack_name
            self.data_stack_type = data_stack_type

        def add_stack(self, name: str, value: any):
            if name in self.data.keys():
                self.datastore.log(LOGTYPE_WARN, f'Another stack within the data stack exists with name "{name}"')
                return
            
            self.data[name] = value

        def commit_to_datastore(self):
            if self.data_stack_type == 'new_data_model' and self.name not in self.main_datastore_data:
                self.main_datastore_data[self.name] = {f'{self.name}_metadata':self.metadata, f'{self.name}_data':self.data}

            elif self.name in self.main_datastore_data and self.data_stack_type == 'edit_data_model':   
                self.main_datastore_data[self.name][f'{self.name}_data'] = self.data

            else:
                self.datastore.log(LOGTYPE_WARN, f'A data model with the same name has already exist or it did not exist when trying to edit ("{self.name}")')
                return
            
            self.datastore.Commit()

    def new_data_stack(self, start_data: dict, data_stack_name: str, data_stack_commit_type: typing.Literal['new_data_model', 'edit_data_model']) -> data_stack:
        """Creates a new `data stack` used for managing temporary session data, and can be later commited to main datastore.\n
        `data_stack_name` is the name used for when you try to commit the data stack to the datastore, `data_stack_commit_type` is how it is commited.\n
        A `data stack` can also be referred to as a data model in a normal datastore"""

        new_data_stack = self.data_stack(self, data_stack_name, start_data,data_stack_commit_type)
        return new_data_stack

    def log(self, logtype: str, message: str):
        if not self.setting_disable_logs:
            print(f'{LOG_COLORS[logtype]}[{logtype}] - {message}.')
