import socket

def start_server(host, port):
    try:
        # Create a socket object
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        # Bind the socket to the host and port
        server_socket.bind((host, port))
        
        # Listen for incoming connections
        server_socket.listen(5)
        print(f"Server is running on {host}:{port}")

        while True:
            # Accept a client connection
            client_socket, client_address = server_socket.accept()
            print(f"Connection received from {client_address}")

            # Receive data from the client
            data = client_socket.recv(1024).decode()
            print(f"Received data: {data}")

            # Send a response
            response = "Hello! You are connected to the server."
            client_socket.send(response.encode())

            # Close the client connection
            client_socket.close()

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        server_socket.close()

# Replace with your desired host and port
host = "0.0.0.0"  # Localhost
port = 25565

start_server(host, port)
