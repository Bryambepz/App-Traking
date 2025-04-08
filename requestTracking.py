from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

# apiKeyTrak = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1aWQiOiI2YWVmYWEyMC1hM2JlLTExZWYtOGUxOS1mYjgwN2Q2MGFjZDQiLCJzdWJJZCI6IjY3MzdmYzgyZDg4NjdiMzY1NjhjMjJlOSIsImlhdCI6MTczMTcyMjM3MH0.0CUNFvvwKeBZ7Rgg9FTSdirMD__FEzqUy-wL97GPaK0'
apiKeyTrak = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1aWQiOiIyOWZiMmYzMC1hNjFiLTExZWYtOGYyYi02MWZjMzM4YzVlNDIiLCJzdWJJZCI6IjY3M2JmMzFiZTlhNDhmMmRhMTBlMTY0NiIsImlhdCI6MTczMTk4MjEwN30.il_d4cFtld8jC7jKJtfl-jGQ2JfipcXytZzH-_GgZX4'
# URL y datos de la solicitud
url = 'https://parcelsapp.com/api/v3/shipments/tracking'

@app.route('/track-shipment', methods=['GET'])
def track_shipment():
    
    # # time_wait = request.json.get('time')
    tracking_id = request.json.get('trackingId')
    # tracking_id = user_data[message.chat.id]['string']
    destination_country = request.json.get('destinationCountry')
    # print(f"es el tra {tracking_id}")

    data = {
        "shipments": [
            {
                "trackingId": tracking_id,
                "destinationCountry": destination_country
            }
        ],
        "languaje": "es",
        "apiKey": f"{apiKeyTrak}"  # Reemplaza con tu clave API
    }

    # Realiza la solicitud POST
    response = requests.post(url, json=data)
    if response.status_code == 200:
        # print(f'el trak ==>\n{response.json()}')
        try:
            # Get UUID from response
            uuid = response.json()['uuid']
            print(f'el uuid {uuid}')
            response = check_tracking_status(uuid)
        except Exception as e:
            # Maneja cualquier otro tipo de error
            print(f"Error inesperado: {e}")
            # response = jsonToObject(response.json()['shipments'][0] )
        
    else:
        print(response.text)
        
    # Devuelve la respuesta de la API
    # return jsonify(response)
    return jsonToObject(response.json()['shipments'][0] )

# Function to check tracking status with UUID
def check_tracking_status(uuid):
    response = requests.get(url, params={'apiKey': apiKeyTrak, 'uuid': uuid})
    priny(f'el respo =>\n{response}')
    try:
        if response.status_code == 200:
            if response.json()['done']:
                print('Tracking complete')
                response = jsonToObject(response.json()['shipments'] )
            # else:
            #     print('Tracking in progress...')
            #     time.sleep(time_wait) # sleep for N sec
            #     check_tracking_status()
        else:
            print(response.text)
    except Exception as e:
        # Maneja cualquier otro tipo de error
        print(f"Error inesperado: {e}")
        response = 'error'
    return response

def jsonToObject(json):
    dys = json['attributes']
    # print(f'ddd {dys}')
    days_transit = None
    
    # Recorrer los atributos para encontrar "days_transit"
    for attribute in dys:
        if attribute.get('l') == 'days_transit':
            days_transit = {'t': 'Days in transit', 'val': attribute.get('val')}
            break

    # Crear el objeto con las claves correctas
    myObject = {
        # 'h':'hh'
        "tracking": json['trackingId'],
        "status": json['status'],
        "days_in_trans": days_transit,  # Aquí debes usar days_transit, no toda la lista
        "origin": json['origin'],
        "destination": json['destination'],
        "lastState": json['lastState'],
        "states": json['states']
    }
    
    return myObject

if __name__ == '__main__':
    app.run(debug=True)
