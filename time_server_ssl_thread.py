import socket
import ssl
import threading
import ntplib
from datetime import datetime
import pytz

def get_current_time_for_timezone(time_zone):
    ntp_client = ntplib.NTPClient()
    response = ntp_client.request('pool.ntp.org', version=4)

    ntp_time = datetime.utcfromtimestamp(response.tx_time)
    local_time = pytz.utc.localize(ntp_time).astimezone(pytz.timezone(time_zone))

    return local_time.strftime("%Y-%m-%d %H:%M:%S %Z")

def handle_client(client_socket):
    try:
        while True:
            # Receive the requested timezone from the client
            requested_timezone = client_socket.recv(1024).decode('utf-8')
            if not requested_timezone:
                break  # Exit the loop if the client sends an empty string

            # Basic check for a valid timezone
            if not pytz.all_timezones.__contains__(requested_timezone):
                error_message = f"Invalid timezone: {requested_timezone}"
                client_socket.sendall(error_message.encode('utf-8'))
                continue  # Skip processing invalid input

            current_time = get_current_time_for_timezone(requested_timezone)
            client_socket.sendall(current_time.encode('utf-8'))
    except ssl.SSLError as e:
        print(f"SSL Error: {e}")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        client_socket.close()

def main():
    # Define the server address (host, port)
    server_address = ('localhost', 12345)

    # Create a socket (AF_INET for IPv4, SOCK_STREAM for TCP)
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Configure SSL context
    ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    ssl_context.load_cert_chain(certfile='server.crt', keyfile='server.key')

    # Wrap the socket with SSL/TLS
    server_socket = ssl_context.wrap_socket(server_socket, server_side=True)

    # Bind the socket to the server address
    server_socket.bind(server_address)

    # Listen for incoming connections (accept up to 5 connections)
    server_socket.listen(5)
    print(f"Server listening on {server_address}")

    try:
        while True:
            # Wait for a connection
            client_socket, client_address = server_socket.accept()
            print(f"Connection from {client_address}")

            # Use a separate thread to handle each client concurrently
            client_handler = threading.Thread(target=handle_client, args=(client_socket,))
            client_handler.start()
    except KeyboardInterrupt:
        print("Server shutting down...")
    finally:
        # Close the server socket
        server_socket.close()

if __name__ == '__main__':
    main()
