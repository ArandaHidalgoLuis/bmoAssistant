import requests
from bs4 import BeautifulSoup
import time

def bus33():            
    page = requests.get('https://www.emtmalaga.es/emt-mobile/informacionParada.html?codParada=3325')
    soup = BeautifulSoup(page.text, 'html.parser')
    uls = soup.find_all('div', {'class':'informacion-parada'})
    hr, minute = map(int, time.strftime("%H %M").split())
    # Lista de posibles clases
    classes = ['minutos', 'minutos1', 'minutos2', 'minutos3', 'minutos4']
    if ( 23<=hr or hr>=7): 
        for cls in classes:
            try:
                # Intentar encontrar el elemento con la clase actual
                 minutos = soup.find('span', {'class': cls}).getText().strip()
                 print(f"{cls}: {minutos}")
                    
            except AttributeError:
                # Si no se encuentra, pasar a la siguiente clase
                continue
    else:
        print("El bus ya no pasa hasta mañana")

