#imports de librerias
import speech_recognition as sr

#imports de funciones
from funciones.polen import airQuality
from funciones.emt import bus33
from funciones.foto import sacarFoto
#from funciones.bmopedia import bmoPedia
from funciones.reproductor import seleccionar_y_reproducir_playlist

activationword = 'bmo'

#Metodo escucha de comandos
def parseCommand():
    listener = sr.Recognizer()
    listener.lang = "es-ES"   
    print('Escuchando comando')
    with sr.Microphone() as source:
        listener.pause_threshold = 1
        input_speech = listener.listen(source)

    try:
        print('Reconociendo voz')
        query = listener.recognize_google(input_speech, language='en_gb')
        print(f'El reconocimiento es: {query}')

    except Exception as exception:
        print('Error de reconocimiento')
        print(exception)
        return None
    
    return query

#Metodo bucle main
if __name__ == '__main__':

    while True:
        #Instrucciones parseadas y separadas
        query = parseCommand().lower().split()
        print(query)
        #
        if query[0] == activationword:
            query.pop(0)

            #Querry Scrappy bus 33  
            if query[0] == 'bus':
                    if 'time' in query:
                         bus33()
                    else:
                        query.pop(0)
                        speech = ' '.join(query)

            #Querry Calidad del aire
            if query[0] == 'air':
                    if 'quality' in query:
                         airQuality()
                    else:
                        query.pop(0)
                        speech = ' '.join(query)

            #Querry Sacar foto
            if query[0] == 'take':
                    if 'photo' in query:
                         sacarFoto()
                    else:
                        query.pop(0)
                        speech = ' '.join(query)

            

            #Querry Reproducir música
            if query[0] == 'play':
                    if 'playlist' in query:
                        seleccionar_y_reproducir_playlist()
                    else:
                        query.pop(0)
                        speech = ' '.join(query)  

        if query[0] == activationword:
            parseCommand()
        else:
            parseCommand()