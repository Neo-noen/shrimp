import shrimp, os
# Example project for learning
datastore = shrimp.JSONDataStore('GameSave')
datastore.setting_disable_logs = True
datastore.new_data_model('saves', {'coins':0, 'level':0, 'xp':0, 'invetory':[]})
datastore.Commit()

print('Example project, type in "coins", "level", "xp" to respectively increase each entry\'s value')

while True:
    GameInput = input('> ')
    try:
        if os.name == 'posix':
            os.system('clear')
        elif os.name == 'nt':
            os.system('cls')

        datastore.increment_data_model('saves', GameInput)
        saveModel = datastore.get_data_model('saves')
        coins = saveModel['coins']
        level = saveModel['level']
        xp = saveModel['xp']
        print(f'Coins: {coins}\nLevels: {level}\nXP: {xp}')
        datastore.Commit()
    except Exception:
        print('You entered an invalid key')
