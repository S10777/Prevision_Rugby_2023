from flask import Flask, render_template, request
import pandas as pd
import numpy as np
import json

app = Flask(__name__)

match_data = pd.read_csv('rugbydataset_propres.csv')
city_data = pd.read_csv('cities_propres.csv')

with open('donnees_nettoyees.json', 'r') as json_file:
    weather_data = json.load(json_file)

cotes_data = pd.read_csv('fichier_cotes.csv')

city_data['station_id'] = city_data['station_id'].astype(str)

weather_dict = {str(item['station_id']): item for item in weather_data}

weather_df = pd.DataFrame(columns=weather_data[0].keys())

for station_id, city_row in city_data.iterrows():
    station_id = str(city_row['station_id'])
    if station_id in weather_dict:
        weather_row = weather_dict[station_id]
        weather_row_df = pd.DataFrame([weather_row])

        non_empty_columns = weather_row_df.columns[~weather_row_df.isna().all()]
        weather_row_df = weather_row_df[non_empty_columns]
        
        weather_df = pd.concat([weather_df, weather_row_df], ignore_index=True, axis=1)
city_weather_data = pd.concat([city_data, weather_df], axis=1)

def simulate_match(home_team, away_team, temperature, precipitation):
    home_matches = match_data[match_data['home_team'] == home_team]
    away_matches = match_data[match_data['away_team'] == away_team]

    if home_team == away_team:
        error_message = "Oh non! Il semble y avoir une confusion. Choisissez deux équipes différentes pour le match."
        return None, None, None, None, None, error_message

    if home_matches.empty or away_matches.empty:
        return None, None, None, None, None, "Équipes non trouvées, veuillez choisir d'autres équipes."

    avg_home_score = home_matches['home_score'].mean()
    avg_away_score = away_matches['away_score'].mean()

    cotes_row = cotes_data[(cotes_data['home_team'] == home_team) & (cotes_data['away_team'] == away_team)]
    if not cotes_row.empty:
        odd_1 = float(cotes_row['odd_1'].str.replace(',', '.').values[0])
        odd_2 = float(cotes_row['odd_2'].str.replace(',', '.').values[0])
        score_potential = avg_home_score + avg_away_score + temperature - precipitation + odd_1 - odd_2
        return score_potential, avg_home_score, avg_away_score, odd_1, odd_2, None
    else:
        score_potential = avg_home_score + avg_away_score + temperature - precipitation
        return score_potential, avg_home_score, avg_away_score, None, None, None

@app.route('/')
def home():
    return render_template('form.html')

@app.route('/simulate', methods=['POST'])
def simulate():
    home_team = request.form['home_team']
    away_team = request.form['away_team']
    temperature = float(request.form['temperature'])
    precipitation = float(request.form['precipitation'])

    score_potential, avg_home_score, avg_away_score, _, _, error_message = simulate_match(home_team, away_team, temperature, precipitation)

    if error_message:
        return render_template('error.html', error_message=error_message)

    winner = home_team if avg_home_score > avg_away_score else away_team if avg_home_score < avg_away_score else None
    return render_template('result.html', winner=winner)


if __name__ == '__main__':
    app.run(debug=True)
