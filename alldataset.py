import pandas as pd

df_matchs = pd.read_csv('cities_propres.csv')
df_villes = pd.read_csv('countries_propres.csv')
df_pays = pd.read_csv('rugbydataset_propres.csv')
df_meteo = pd.read_csv('donnees_nettoyees.csv')

print("Colonnes de df_matchs :")
print(df_matchs.columns)
print("\nColonnes de df_villes :")
print(df_villes.columns)
print("\nColonnes de df_pays :")
print(df_pays.columns)
print("\nColonnes de df_meteo :")
print(df_meteo.columns)

df_complet = df_villes.merge(df_pays, left_on='country', right_on='home_team', how='inner')

df_complet = df_matchs.merge(df_complet, left_on='city_name', right_on='city', how='inner')

df_complet = df_meteo.merge(df_complet, left_on='city_name', right_on='city', how='inner')

df_complet.to_csv('total.csv', index=False)

print("\nFusion terminée. Les données fusionnées ont été enregistrées dans 'total.csv'.")
