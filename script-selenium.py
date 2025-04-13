from datetime import datetime, timedelta
from telebot import types
import requests
import telebot
import time
import json

# app = Flask(__name__)

apiKeyTrak = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1aWQiOiI2YWVmYWEyMC1hM2JlLTExZWYtOGUxOS1mYjgwN2Q2MGFjZDQiLCJzdWJJZCI6IjY3MzdmYzgyZDg4NjdiMzY1NjhjMjJlOSIsImlhdCI6MTczMTcyMjM3MH0.0CUNFvvwKeBZ7Rgg9FTSdirMD__FEzqUy-wL97GPaK0'
# apiKeyTrak = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1aWQiOiIyOWZiMmYzMC1hNjFiLTExZWYtOGYyYi02MWZjMzM4YzVlNDIiLCJzdWJJZCI6IjY3M2JmMzFiZTlhNDhmMmRhMTBlMTY0NiIsImlhdCI6MTczMTk4MjEwN30.il_d4cFtld8jC7jKJtfl-jGQ2JfipcXytZzH-_GgZX4'
# URL y datos de la solicitud
url = 'https://parcelsapp.com/api/v3/shipments/tracking'

# Bot
tokenBot = '7684872345:AAF24QUuyblnN3LLeIjiUkP34cvm9ZPhW1E'
bt = telebot.TeleBot(tokenBot, parse_mode=None) # You can set parse_mode by default. HTML or MARKDOWN
bt.remove_webhook()
# Diccionario para almacenar temporalmente la información del usuario
user_data = {}
count = 1

@bt.message_handler(commands=['start', 'help'])
def send_welcome(message):
    print('aaaaaaa', flush=True)
    # or add KeyboardButton one row at a time:
    markup = types.ReplyKeyboardMarkup()
    itembta = types.KeyboardButton('Trackear mi pedido')
    itembtb = types.KeyboardButton('Nada')
    markup.row(itembta)
    markup.row(itembtb)
	# bot.reply_to(message, "Hola en que te puedo ayudar ;)")
    bt.send_message(message.chat.id, "Choose one:", reply_markup=markup)
    
    
# Maneja las opciones seleccionadas por el usuario
@bt.message_handler(func=lambda message: True)
def handle_option(message):
    selected_option = message.text  # Obtener el texto de la opción seleccionada
    user_id = message.chat.id  # Identificador único del usuario
    
    # Registrar o manejar la opción
    if selected_option == 'Trackear mi pedido':
        if user_id not in user_data:
            user_data[user_id] = {"string": None, "tracking": False, "states": [], "lastState": None}  # Inicializar datos para el usuario
            
        bt.send_message(message.chat.id, f"Hola {message.chat.id}\nHas seleccionado: Trackear mi pedido")
        bt.send_message(message.chat.id, "Por favor, ingresa un IdTracking:")
        bt.register_next_step_handler(message, get_string)  # Esperar el string del usuario
    elif selected_option == 'Nada':
        bt.send_message(message.chat.id, "Has seleccionado: Nada")
        send_welcome(message)
    else:
        if user_id in user_data:
            if selected_option == 'Cada Hora':
                bt.send_message(message.chat.id, "1h")
                tiempo(message, 1)
            elif selected_option == 'Cada 2':
                bt.send_message(message.chat.id, "2h")
                tiempo(message, 2)
            elif selected_option == 'Cada 3':
                bt.send_message(message.chat.id, "3h")
                tiempo(message, 3)
            elif selected_option == 'Cada 5':
                bt.send_message(message.chat.id, "5h")
                tiempo(message, 5)
            else:
                bt.send_message(message.chat.id, "Opción no reconocida")
                send_welcome(message)
        else:
            send_welcome(message)

# Función para manejar el ingreso del string
def get_string(message):
    print(f"mi user {user_data}", flush=True)
    
    user_data[message.chat.id]['string'] = message.text  # Guardar el string ingresado
    bt.send_message(message.chat.id, "Ahora indica cuantas veces al dia quieres que se revise el estado de tracking:")
    # bt.register_next_step_handler(message, get_number)  # Esperar el número del usuario
    markup = types.ReplyKeyboardMarkup()
    itembta = types.KeyboardButton('Cada Hora')
    itembtb = types.KeyboardButton('Cada 2')
    itembtc = types.KeyboardButton('Cada 3')
    itembtd = types.KeyboardButton('Cada 5')
    markup.row(itembta, itembtb)
    markup.row(itembtc, itembtd)
	# bot.reply_to(message, "Hola en que te puedo ayudar ;)")
    bt.send_message(message.chat.id, "Choose one:", reply_markup=markup)

# # Función para manejar el ingreso del número
# def get_number(message):
#     try:
#         user_data['number'] = int(message.text)  # Intentar convertir a número
#         bt.send_message(message.chat.id, f"Has ingresado: String = {user_data['string']}, Número = {user_data['number']}")
#         # Aquí puedes agregar la lógica para manejar el string y el número
#     except ValueError:
#         bt.send_message(message.chat.id, "El valor ingresado no es un número válido. Por favor, intenta de nuevo.")
#         bt.register_next_step_handler(message, get_number)  # Volver a solicitar el número

# Funcion que calcula las veces a notificar
def tiempo(message, timeR):
    # Obtener la hora actual
    hora_actual = datetime.now()
    
    # Calcular la hora dentro de 5 días
    hora_futura = hora_actual + timedelta(days=2)
    
    # Calcular la diferencia en horas
    diferencia_horas = (hora_futura - hora_actual).total_seconds() / 3600
    nTimes =  diferencia_horas / timeR
    timesRequest = round(nTimes)
    print(f"Solicita n {timeR} total {timesRequest}", flush=True)
    for i in range(timesRequest):
        print(f"chat {message}")
        print(f"chat id {message.chat.id}")
        user_data[message.chat.id]['tracking'] = True
        ojbTraking = track_shipment(message)
        # ojbTraking = {'tracking': '281833789154', 'status': 'delivered', 'days_in_trans': {'t': 'Days in transit', 'val': '6'}, 'origin': 'United States', 'destination': 'United States', 'lastState': {'location': 'Miami, FL', 'date': '2024-11-21T14:16:00Z', 'carrier': 0, 'status': 'Delivered'}, 'states': [{'location': 'Miami, FL', 'date': '2024-11-21T14:16:00Z', 'carrier': 0, 'status': 'Delivered'}]}
        print(f"mi trak=>\n{ojbTraking}", flush=True)
        if ojbTraking == 'Error' :
            bt.send_message(message.chat.id, "No existe ese idTracking o ya expiro, ingrese uno actual.\nIntente nuevamente")
            user_data[message.chat.id]['tracking'] = False
            send_welcome(message)
            # i = timesRequest
            break
        else:
            # bt.send_message(message.chat.id, f"Alerta {i+1}")
            # bt.send_message(message.chat.id, str(ojbTraking))
            response = ""
            lenghtRequest = len(ojbTraking['states'])
            lenghtUser = len(user_data[message.chat.id]['states'])
            if ( lenghtUser < lenghtRequest ):
            # if i == 0 :
                response = f"Su tracking lleva {ojbTraking['days_in_trans']['val']} días en transito\nEl ultimo estado es:\n * Fecha: {ojbTraking['lastState']['date']}\n * Estado: {ojbTraking['lastState']['status']}\n * Ubicacion: {ojbTraking['lastState']['location']}"
            # else:
            #     response = "Tranckon"
                user_data[message.chat.id]['lastState'] = ojbTraking['lastState']
                user_data[message.chat.id]['states'] = ojbTraking['states']
                
                # bt.send_message(message.chat.id, json.dumps(ojbTraking, indent=2))
                bt.send_message(message.chat.id, response, disable_notification=False )
            # else:
            #     bt.send_message(message.chat.id, "=====", disable_notification=False )

        notification = timeR*3600
        print(f'notifica en {notification}\n\n', flush=True)
        time.sleep(notification)
        print("fin sleep")
        # time.sleep(5)
    user_data[message.chat.id]['tracking'] = False
    bt.send_message(message.chat.id, "Se ha agotado la cantidad de chequeos de estado de su pedido.\nSi desea seguir siendo informado, por favor, vuelva a realizar el proceso.", disable_notification=False)



##//// Consulta el servicio
# # @app.route('/track-shipment', methods=['GET'])
def track_shipment(message):
    
    # # time_wait = request.json.get('time')
    # tracking_id = request.json.get('trackingId')
    tracking_id = user_data[message.chat.id]['string']
    destination_country = 'United States'
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
    print(f"data para el trak {data}")
    # Realiza la solicitud POST
    response = requests.post(url, json=data)
    hayUuid = False
    if response.status_code == 200:
        # print(f'el trak ==>\n{response.json()}')
        try:
            # Get UUID from response
            # uuid = response.json()['uuid']
            # uuid = json.get('uui', None)
            uuid = response.json().get('uuid', None)
            print(f'el uuid {uuid}', flush=True)
            if ( uuid is not None ):
                hayUuid = True
                response = check_tracking_status(uuid)
        except Exception as e:
            # Maneja cualquier otro tipo de error
            print(f"Error inesperado: {e}", flush=True)
            # response = jsonToObject(response.json()['shipments'][0] )
        
    else:
        print(f'no hay dataa {response.text}', flush=True)
        
    # Devuelve la respuesta de la API
    # return jsonify(response)
    if ( hayUuid == False):
        print(f"json del track {response.json()}")
        if response.json().get('shipments'):
            return jsonToObject(response.json()['shipments'][0] )
        else:
            return 'Error'
    else:
        print(f"hay {response}")
        return response

# Function to check tracking status with UUID
def check_tracking_status(uuid):
    response = requests.get(url, params={'apiKey': apiKeyTrak, 'uuid': uuid})
    print(f'el respo =>\n{response.json()}', flush=True)
    try:
        if response.status_code == 200:
            if response.json()['done']:
                print('Tracking complete', flush=True)
                try:
                    print(f"check track status {response.json()}")
                    response = jsonToObject(response.json()['shipments'][0] )
                except Exception as e:
                    print(f"Error inesperado al ler json a obj: {e}", flush=True)
                    response = 'error'
            # else:
            #     print('Tracking in progress...', flush=True)
            #     time.sleep(time_wait) # sleep for N sec
            #     check_tracking_status()
        else:
            print(response.text, flush=True)
    except Exception as e:
        # Maneja cualquier otro tipo de error
        print(f"Error inesperado: {e}", flush=True)
        response = 'error'
    return response

def jsonToObject(jsonReq):
    _json = jsonReq
    global count
    print(f"convert to json")
    try:
        dys = _json.get('attributes')
        print(f"222 to json {dys}")
        # print(f'ddd {dys}')
        days_transit = {'t': 'Days in transit', 'val': '0'}
        
        # Recorrer los atributos para encontrar "days_transit"
        for attribute in dys:
            if attribute.get('l') == 'days_transit':
                days_transit = {'t': 'Days in transit', 'val': attribute.get('val')}
                break
        # print(f"el json {_json}")
        # Crear el objeto con las claves correctas
        myObject = {
            # 'h':'hh'
            "tracking": _json['trackingId'],
            "status": _json['status'],
            "days_in_trans": days_transit,  # Aquí debes usar days_transit, no toda la lista
            "origin": 'no',
            "destination": _json.get('destination', 'Aun no destino'),
            "lastState": _json['lastState'],
            "states": _json['states']
        }
        count += 1
        print("obj converted")
        return myObject
    except Exception as e:
        print(f"Error jsontoobj: {e}", flush=True)

# Polling robusto
while True:
    try:
        print("Iniciando el polling...")
        bt.polling(non_stop=True, timeout=120)
    except Exception as e:
        print(f"Ocurrió un error: {e}")
        print("Reintentando en 5 segundos...")
        time.sleep(5)

# if __name__ == '__main__':
#     app.run(debug=True)
