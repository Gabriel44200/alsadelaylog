import requests
import json
from datetime import datetime

# Función para obtener las salidas de la parada
def get_departures(lineId, locationId, stopLocationId):
    url = "https://apps.alsa.es/rest/api/urb/v1/getDeparturesStop/"

    # Autenticación
    auth_data = {
        "authentication": {
            "provider": "ABAMOBILE",
            "token": "91F780040F1FC26A10389C0E730A1672699E25580B572E53",
            "date": 20221104,
            "operation": 521429,
            "time": 203854
        },
        "company": 542,
        "conceCod": 1546,
        "lineId": lineId,
        "locale": "es",
        "locationId": locationId,
        "stopLocationId": stopLocationId,
        "records": 50
    }

    headers = {"Content-Type": "application/json"}

    # Realizar la solicitud POST
    response = requests.post(url, headers=headers, json=auth_data)

    # Verificamos la respuesta
    if response.status_code == 200:
        departures_data = response.json()
        return departures_data
    else:
        print(f"Error al obtener las salidas: {response.status_code}")
        return None

# Función para filtrar y procesar las salidas que han pasado o no
def process_departures(departures):
    processed_data = []

    for departure in departures["info"]:
        # Obtener la hora programada
        scheduled_time = departure["time"]

        # Verificar si la salida ha pasado o no
        if departure["visit"] == 1 and "HA PASADO" in departure["estText"]:
            # Extraer la hora real de paso
            real_pass_time = departure["estText"].split("HA PASADO A LAS")[1].strip()
            
            # Solo necesitamos hora y minutos (HH:MM)
            try:
                real_pass_time = datetime.strptime(real_pass_time, "%H:%M").strftime("%H:%M")
            except ValueError:
                continue  # Si el formato no es correcto, lo ignoramos
        else:
            # Si no ha pasado, poner "N/A"
            real_pass_time = "N/A"

        # Guardar los datos procesados
        processed_data.append({
            "scheduled_time": scheduled_time,
            "real_pass_time": real_pass_time,
            "line_name": departure["lineName"],
            "line_short_name": departure["lineShortName"],
            "destination": departure["destName"]
        })

    return processed_data

# Ejemplo de uso
line = 11151  # Línea que quieres consultar
location = 15001  # Ubicación de la parada
stopLocation = 1  # ID de la parada

departures = get_departures(line, location, stopLocation)

if departures:
    # Procesar las salidas
    processed_departures = process_departures(departures)
    
    # Guardar los datos procesados en un archivo JSON
    with open("processed_departures.json", "w", encoding="utf-8") as f:
        json.dump(processed_departures, f, ensure_ascii=False, indent=4)

    print("Datos procesados y guardados correctamente en 'processed_departures.json'")
