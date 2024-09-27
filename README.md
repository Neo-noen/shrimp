# shrimp

The `shrimp` module is a light weight data store handling module.
It currently is in it's very early stages of development, therefore might be missing some features or diverse choices of data stores.
`shrimp` only supports JSON file datastores as of now.

# Key features:
- Managing multiple datastores at once.
- Commiting to datastores to avoid corruption during runtime.
- Basic CRUD and batched operations with "data models". (not really lol)
- The ability to disable logs, set default data,... for individual datastores, providing customization.

# Example
Here is a minimal example of how you would generally use the `shrimp` module.

```python
import shrimp
datastore = shrimp.JSONDataStore('example') #Creates a JSON file in the current working directory with the name "example"
datastore.new_data_model('example_model', default_data={'example':'example'}) #Creates a new data model "example_model"

# Getting data model data
print(datastore.get_data_model('example_model'))
```

# Datastore Structure
This is how your JSON datastore should be structured after creation.

```json
{
  "player_data_metadata": {
    "created_time": "2024-09-25 07:45:10.657994",
    "last_modified": "2024-09-25 07:46:25.127580"
  },
  "player_data_data": {}
}
```

*this sounded way too AI generated*
