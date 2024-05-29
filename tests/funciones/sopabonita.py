from bs4 import BeautifulSoup
import requests

numeroParada = input("Escribe el número de parada que deseas consultar: ")

page = requests.get('https://www.emtmalaga.es/emt-mobile/informacionParada.html?codParada='+numeroParada)
soup = BeautifulSoup(page.text, 'html.parser')

liBuses = soup.find_all('ul', {'data-role': 'listview'})

def devolverNBuses():
    bus_identifiers = []

    for ul in liBuses:
        a_tags = ul.find_all('a')
        for a in a_tags:
            bus_id = a.get('title')
            if bus_id:
                bus_identifiers.append(bus_id)

    for identifier in bus_identifiers:
        print(identifier)

def devolverTBuses():
    bus_times = []

    for ul in liBuses:
        span_tags = ul.find_all('span', class_=lambda x: x and x.startswith('minutos'))
        for span in span_tags:
            time_text = span.get_text(strip=True)
            if time_text:
                bus_times.append(time_text)
    for time in bus_times:
        print(time)
devolverNBuses()
devolverTBuses()
