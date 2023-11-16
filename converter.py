import pandas as pd

data = pd.read_csv('donnees_nettoyees.csv')

json_data = data.to_json(orient='records')

with open('donnees_nettoyees.json', 'w') as json_file:
    json_file.write(json_data)
