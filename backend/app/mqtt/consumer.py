import json
import paho.mqtt.client as mqtt

from app.database.db import insert_sensor_data

# MQTT_BROKER = "192.168.86.8"

MQTT_BROKER = "10.64.89.110"
MQTT_PORT = 1883
MQTT_TOPIC = "iot/esp32/environment"

def on_connect(client, userdata, flags, rc):

    print("Conectado ao broker MQTT com código de resultado: " + str(rc))

    client.subscribe(MQTT_TOPIC)
    print("Inscrito no tópico: " + MQTT_TOPIC)

def on_message(client, userdata, msg):

    try:
        payload = json.loads(msg.payload.decode())

        device_id = payload["device_id"]
        temperature = payload["temperature"]
        humidity = payload["humidity"]
        lux = payload["lux"]

        print(f"Dados recebidos do dispositivo {device_id}:")
        print(f"Dispositivo: {device_id}, Temperatura: {temperature}°C, Umidade: {humidity}%, Lux: {lux} lux")
        print(50 * "-")

        insert_sensor_data(device_id, temperature, humidity, lux)

    except Exception as e:
        print("Erro ao processar a mensagem MQTT: " + str(e))

def start_mqtt_consumer():

    client = mqtt.Client()

    client.on_connect = on_connect
    client.on_message = on_message

    try:
        client.connect(MQTT_BROKER, MQTT_PORT, 60)
    except Exception as e:
        print(f"Não foi possível conectar ao broker MQTT ({MQTT_BROKER}:{MQTT_PORT}): {e}")
        print("Continuando sem consumir dados MQTT. Você ainda pode consultar os dados existentes no banco de dados.")
        return

    client.loop_forever()
