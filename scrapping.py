import requests
from bs4 import BeautifulSoup
import csv

url = "https://www.betclic.fr/coupe-du-monde-2023-s5/coupe-du-monde-2023-c34"

response = requests.get(url)

if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')
    
    elements = soup.find_all(class_="oddButtonWrapper loading ng-tns-c2707410650-102 ng-trigger ng-trigger-oddsStateAnimation")

    data = []

    for element in elements:
        element_text = element.text.strip()
        
        data.append([element_text])

    with open("scrapping.csv", "w", newline='', encoding='utf-8') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(["Data"])
        csv_writer.writerows(data)

    print("Données enregistrées dans le fichier scrapping.csv")

else:
    print("La requête a échoué avec le code :", response.status_code)
