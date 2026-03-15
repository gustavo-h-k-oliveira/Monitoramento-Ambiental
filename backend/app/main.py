import threading
from mqtt.consumer import start_mqtt_consumer

def main():
    mqtt_thread = threading.Thread(target=start_mqtt_consumer)
    mqtt_thread.start()

    print("Backend iniciado")

if __name__ == "__main__":
    main()