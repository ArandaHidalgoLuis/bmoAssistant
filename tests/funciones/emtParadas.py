import requests
from bs4 import BeautifulSoup
import time

numeroParada = '116'
def bus33():            
    page = requests.get('https://www.emtmalaga.es/emt-mobile/informacionParada.html?codParada='+numeroParada)
    soup = BeautifulSoup(page.text, 'html.parser')
    uls = soup.find_all('div', {'class':'informacion-parada'})
    li = soup.find_all('li', {'class':'ui-li ui-li-static ui-btn-up-c'})

    hr, minute = map(int, time.strftime("%H %M").split())
    # Lista de posibles clases
    classes = ['minutos', 'minutos1', 'minutos2', 'minutos3', 'minutos4']
  
    for ul in uls:
            for cls in classes:                
                try:
                    # Intentar encontrar el elemento con la clase actual
                    bus_numero = ul.find('a', {'data-transition': 'slide', 'rel': 'external'}).getText().strip()
                    minutos = ul.find('span', {'class': cls}).getText().strip()
                    print(f"Bus Número:"+bus_numero+" "+"Tiempo:"+minutos)
                  
                except AttributeError:
                    # Si no se encuentra, pasar a la siguiente clase
                    continue

            # Buscar números de bus dentro del 'div' actual
            


bus33()
