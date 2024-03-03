import socket
import time
import ssl

def get_time_from_server(client_socket):
    print("Enter the timezone (e.g., 'America/New_York') or press Enter to exit: ")
    while True:
        # Get the desired timezone from the user
        time_zone = input('>> ')

        if not time_zone:
            break  # Exit the loop if the user doesn't provide a timezone

        # Send the requested timezone to the server
        client_socket.sendall(time_zone.encode('utf-8'))

        # Receive data from the server
        data = client_socket.recv(1024)
        print(f"Time in {time_zone}: {data.decode('utf-8')}")

def main():
    # Define the server address (host, port)
    server_address = ('localhost', 12345)

    while True:
    # Create a socket (AF_INET for IPv4, SOCK_STREAM for TCP)
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Configure SSL context
        ssl_context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
        ssl_context.load_verify_locations(cafile='server.crt')  # Specify the server's certificate

    # Wrap the socket with SSL/TLS
        client_socket = ssl_context.wrap_socket(client_socket, server_hostname='localhost')

        try:
        # Connect to the server
            client_socket.connect(server_address)

        # Call the function to get time from the server
            get_time_from_server(client_socket)

        except socket.error as e:
            print(f"Connection error: {e}")
            print("Reconnecting in 5 seconds...")
            time.sleep(5)
            continue  # Retry the outer loop on connection error
        except Exception as e:
            print(f"Error: {e}")
        finally:
            # Clean up the connection
            break

    client_socket.close()

if __name__ == "__main__":
    main()

