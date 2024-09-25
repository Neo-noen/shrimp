# shrimp

The `shrimp` module is a light weight data store handling module.
It currently is in it's very early stages of development, therefore might be missing some features or diverse choices of data stores.

`shrimp` only supports JSON file datastores as of now.

Key features:
- Managing multiple datastores at once.
- Commiting to datastores to avoid corruption during runtime.
- Basic CRUD and batched operations with "data models". (not really lol)

```python
import shrimp
datastore = shrimp.JSONDataStore('example') #Creates a JSON file in the current working directory with the name "example"
datastore.new_data_model('example_model', default_data={'example':'example'}) #Creates a new data model "example_model"

# Getting data model data
print(datastore.get_data_model('example_model'))
```

This is how your JSON datastore should be structured after creation.

```json
{
  "player_data_metadata": {
    "created_time": "2024-09-25 07:45:10.657994",
    "last_modified": "2024-09-25 07:46:25.127580"
  },
  "player_data_data": {
    "player": {
      "player_metadata": {
        "status": "active",
        "created_at": "2024-09-25 07:45:20.489322",
        "type": "data_model"
      },
      "player_data": {
        "name": "E",
        "level": 2,
        "health": 76,
        "attack": 10,
        "defense": 5,
        "inventory": [
          "Troll Club"
        ]
      }
    }
  }
}
```
