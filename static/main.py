import requests
from bs4 import BeautifulSoup

url = 'https://forms.gle/RMZibV5X6tYx2LEL9'

response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

form_elements = soup.find_all('input') + soup.find_all('select') + soup.find_all('textarea')

for element in form_elements:
    print(element['name'])