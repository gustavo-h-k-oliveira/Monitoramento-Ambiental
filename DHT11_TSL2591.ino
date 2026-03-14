#include <WiFi.h>
#include <PubSubClient.h>
#include <DHT.h>
#include <Wire.h>
#include <Adafruit_TSL2591.h>
#include <ArduinoJson.h>

#define DHTPIN 4
#define DHTTYPE DHT11

const char* ssid = "NOME_REDE_WIFI";
const char* password = "*SENHA_REDE_WIFI*";

const char* mqtt_server = "IP_SERVIDOR_MQTT";
const char* topic = "iot/esp32/environment";

WiFiClient espClient;
PubSubClient client(espClient);

DHT dht(DHTPIN, DHTTYPE);
Adafruit_TSL2591 tsl = Adafruit_TSL2591(2591);

void setup_wifi() {

  Serial.println();
  Serial.print("Conectando ao WiFi: ");
  Serial.println(ssid);

  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println();
  Serial.println("WiFi conectado!");
  Serial.print("IP: ");
  Serial.println(WiFi.localIP());
}

void reconnect() {

  while (!client.connected()) {

    Serial.print("Conectando ao MQTT...");

    if (client.connect("ESP32Client")) {

      Serial.println("conectado!");

    } else {

      Serial.print("falhou, rc=");
      Serial.print(client.state());
      Serial.println(" tentando novamente em 2s");

      delay(2000);
    }

  }

}

void setup() {

  Serial.begin(115200);

  Serial.println("ESP32 Iniciado");

  setup_wifi();

  client.setServer(mqtt_server, 1883);

  dht.begin();

  if (!tsl.begin()) {
    Serial.println("Erro TSL2591");
  }

}

void loop() {

  if (!client.connected()) {
    reconnect();
  }

  client.loop();

  float temp = dht.readTemperature();
  float hum = dht.readHumidity();

  if (isnan(temp) || isnan(hum)) {
    Serial.println("Erro leitura DHT");
    delay(2000);
    return;
  }

  sensors_event_t event;
  tsl.getEvent(&event);

  float lux = event.light;

  StaticJsonDocument<128> doc;

  doc["device_id"] = "esp32_01";
  doc["temperature"] = temp;
  doc["humidity"] = hum;
  doc["lux"] = lux;

  char buffer[128];
  serializeJson(doc, buffer);

  if (!client.publish(topic, buffer)) {
    Serial.println("Falha ao publicar MQTT");
  }

  Serial.println(buffer);

  delay(5000);

}