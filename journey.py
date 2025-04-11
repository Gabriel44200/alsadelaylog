import requests
import json
import time

# Autenticación para getLines
auth_lines = {
    "date": 20221104,
    "operation": 174032,
    "provider": "ABAMOBILE",
    "time": 153335,
    "token": "1966E8D2D03754E63DA035CD1A83355ECA6172830A838BD1"
}

# Autenticación para getJourneys
auth_journeys = {
    "date": 20221104,
    "operation": 876884,
    "provider": "ABAMOBILE",
    "time": 153815,
    "token": "441A4420F3234B48A63B5C3B67D85D9BCF757F92746825D8"
}

# Parámetros comunes
company = 542
conceCod = 1546

# Obtener líneas
lines_url = "https://apps.alsa.es/rest/api/urb/v1/getLines/"
lines_payload = {
    "authentication": auth_lines,
    "company": company,
    "conceCod": conceCod
}

headers = {"Content-Type": "application/json"}
response = requests.post(lines_url, headers=headers, json=lines_payload)

if response.status_code == 200:
    lines_data = response.json().get("info", [])
    all_lines = []

    for line in lines_data:
        line_id_general = line.get("id")
        short_name = line.get("shortName")
        print(f"Obteniendo rutas para la línea {short_name} (ID: {line_id_general})")

        # Obtener rutas para cada línea
        journeys_url = "https://apps.alsa.es/rest/api/urb/v1/getJourneys/"
        journeys_payload = {
            "authentication": auth_journeys,
            "company": company,
            "conceCod": conceCod,
            "lineId": line_id_general
        }

        journey_resp = requests.post(journeys_url, headers=headers, json=journeys_payload)
        routes_data = []

        if journey_resp.status_code == 200:
            journeys = journey_resp.json().get("info", [])
            for journey in journeys:
                route_data = {
                    "journeyId": journey.get("id"),
                    "journeyName": journey.get("name"),
                    "routeLineId": journey.get("lineId")
                }
                routes_data.append(route_data)
        else:
            print(f"Error al obtener rutas para la línea {short_name}")

        # Guardamos toda la información de la línea
        all_lines.append({
            "lineShortName": short_name,
            "lineId_general": line_id_general,
            "routes": routes_data
        })

        time.sleep(0.5)  # Pausa para no sobrecargar el servidor

    # Guardamos todo en un archivo JSON
    with open("lineas_y_rutas.json", "w", encoding="utf-8") as f:
        json.dump(all_lines, f, ensure_ascii=False, indent=4)

    print("\nInformación guardada correctamente en 'lineas_y_rutas.json'")
else:
    print(f"Error al obtener líneas: {response.status_code}")
