import paho.mqtt.client as mqtt
import time
from datetime import datetime

# MQTT Broker bilgileri
BROKER = "192.168.16.245"  # MQTT broker adresi
PORT = 1883                # MQTT broker portu
TOPIC = "ti/+/+/+/status"  # Wildcard ile topic

USERNAME = "broker"        # Kullanıcı adı
PASSWORD = "aksan2020"     # Şifre

# Mesaj alındığında çağrılan callback fonksiyonu
def on_message(client, userdata, message):
    received_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    topic = message.topic
    payload = message.payload.decode()  # Mesajı string olarak decode et

    # Mesajı ekrana bastır
    print(f"[{received_time}] Received message on topic '{topic}': {payload}")

# MQTT istemcisini oluştur ve ayarları yap
client = mqtt.Client("PythonTestClient")  # İstemci adı
client.username_pw_set(USERNAME, PASSWORD)  # Kullanıcı adı ve şifre
client.on_message = on_message  # Mesaj callback fonksiyonu

# Broker'a bağlan
print("Connecting to broker...")
client.connect(BROKER, PORT)
print("Connected!")

# Wildcard Topic'e abone ol
print(f"Subscribing to topic '{TOPIC}'")
client.subscribe(TOPIC)

# Mesajları almak için loop başlat
client.loop_start()

# Test için bir süre bekle
time.sleep(60)

# MQTT bağlantısını kapat
print("Disconnecting from broker...")
client.loop_stop()
client.disconnect()
print("Disconnected!")
