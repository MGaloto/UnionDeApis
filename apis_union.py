####  Combinacion de APIS


import requests
import json    
from pprint import pprint
import csv
from time import sleep

# Utilizaremos la API de https://home.openweathermap.org/

# Importamos la Key

with open('Claves.txt') as claves: keys = [clave.strip('\n') for clave in claves]


key = keys[0]

# Clave de https://opencagedata.com/

key_geo = keys[1]


# Creamos una tabla con las variables que vamos a capturar

tabla = [['ciudades', 'provincias', 'latitud', 'longitud', 'id', 'temperatura', 'temperatura_max', 'temperatura_min', 'tiempo']]

# Guardamos todas las ciudades que no encuentra:

log_error = open('log_error.txt', 'w')

with open('ciudades_1.csv', 'r') as sucursales:
    entrada = csv.reader(sucursales, delimiter = ';')
    for sucursal in entrada:
        ciudades = sucursal[0]
        provincias = sucursal[1]
        url_geo = 'https://api.opencagedata.com/geocode/v1/json?q=' + ciudades + '&key=' + key_geo + '&language=es&pretty=1'
        objeto_geo = json.loads(requests.get(url_geo).text)
        #pprint(objeto_geo['results'][0]['geometry'])
        lat = objeto_geo['results'][0]['geometry']['lat']
        long = objeto_geo['results'][0]['geometry']['lng']
        print('\n', ciudades, '-->', provincias, '\n')
        url = "http://api.openweathermap.org/data/2.5/weather?lat=" + str(lat) + '&lon=' + str(long) + "&units=metric&lang=es&appid=" + key
        objeto = json.loads(requests.get(url).text)
        if objeto.get('weather') == None: # Este codigo nos sirve por si no encuentra el clima de una de las ciudades
            log_error.write(ciudades + " - no encontrada\n")
            print(" Ciudad no encontrada")
            sleep(2)
        else:            
            latitud = objeto_geo['results'][0]['geometry']['lat']
            longitud = objeto_geo['results'][0]['geometry']['lng']
            id_ = objeto['id']
            temperatura = objeto['main']['temp']
            temperatura_max = objeto['main']['temp_max'] 
            temperatura_min = objeto['main']['temp_min'] 
            tiempo = objeto['weather'][0]['description']
            variables = [ciudades, provincias, latitud, longitud, id_, temperatura, temperatura_max, temperatura_min, tiempo]
            tabla.append(variables)
            sleep(1)
            print('\n', 'Latitud: ', objeto['coord']['lat'], '\n', 'Longitud: ', objeto['coord']['lon'],'\n' ,
            'Id: ',objeto['id'], '\n', 'Temperatura: ',objeto['main']['temp'] , '\n', 'Temperatura Max: ', objeto['main']['temp_max'], '\n',
            'Temperatura Min: ', objeto['main']['temp_min'], '\n', 'Tiempo: ', objeto['weather'][0]['description'])
            

log_error.close()

# Se guarda como CSV 


with open('excelfinal.csv', 'w', newline = '') as excel_final:
    salida = csv.writer(excel_final)
    salida.writerows(tabla)
    



