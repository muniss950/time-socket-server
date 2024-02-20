import socket

def get_time_from_server():
    # Define the server address (host, port)
    server_address = ('localhost', 12345)

    # Create a socket (AF_INET for IPv4, SOCK_STREAM for TCP)
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # Connect to the server
        client_socket.connect(server_address)

        while True:
            # Get the city name from the user
            city_name = input("Enter the city name (e.g., 'New York', 'Paris'): ")

            if not city_name:
                break  # Exit the loop if the user doesn't provide a city name

            # Send the city name to the server
            client_socket.sendall(city_name.encode('utf-8'))

            # Receive data from the server
            data = client_socket.recv(1024)
            print(f"Time in {city_name}: {data.decode('utf-8')}")

    except Exception as e:
        print(f"Error: {e}")

    finally:
        # Clean up the connection
        client_socket.close()

if __name__ == "__main__":
    get_time_from_server()
