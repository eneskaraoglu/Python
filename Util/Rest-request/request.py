import requests
import json

# Servis URL'si
url = "http://192.168.16.176:8082/addRecord"

# JSON verisi
payload = {
    "key1": "value1",
    "key2": "value2",
    "key3": "value3"
}

try:
    # HTTP POST isteği gönderme
    print("Sending request to the service...")
    response = requests.post(url, json=payload, timeout=10)

    # Yanıt kodunu kontrol et
    print(f"HTTP Status Code: {response.status_code}")
    
    # Yanıt içeriğini yazdır
    if response.status_code == 200:
        print("Response:", response.json())
    else:
        print(f"Failed with status code {response.status_code}")
        print("Error response:", response.text)

except requests.exceptions.Timeout:
    print("The request timed out!")
except requests.exceptions.ConnectionError:
    print("Failed to connect to the server!")
except requests.exceptions.RequestException as e:
    print(f"An error occurred: {e}")
