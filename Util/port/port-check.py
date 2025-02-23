import requests

def check_port(ip, port):
    url = "https://canyouseeme.org/"

    # Simulated form data payload (adjust as necessary if the service expects different fields)
    payload = {
        'ip': ip,
        'port': port
    }

    try:
        response = requests.post(url, data=payload)
        response.raise_for_status()  # Raise exception for HTTP errors
        
        if "Success" in response.text:
            print(f"Port {port} on IP {ip} is open.")
        elif "Error" in response.text:
            print(f"Port {port} on IP {ip} is closed.")
        else:
            print("Unexpected response. Please check the service output.")

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")

# Replace with your desired IP and port
ip_address = "10.76.65.133"
port_number = 25565
        
check_port(ip_address, port_number)

