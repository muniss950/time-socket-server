import socket
import ssl
import threading
import ntplib
from datetime import datetime,timezone
import pytz
import logging
from time import ctime
from tzlocal import get_localzone
import geo

logging.basicConfig(filename='socket.log', level=logging.INFO, format='%(asctime)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

def get_current_time_for_timezone(time_zone):
    ntp_client = ntplib.NTPClient()
    response = ntp_client.request('pool.ntp.org', version=4)

    ntp_time = datetime.utcfromtimestamp(response.tx_time)
    local_time = pytz.utc.localize(ntp_time).astimezone(pytz.timezone(time_zone))

    return local_time.strftime("%Y-%m-%d %H:%M:%S %Z")
# def get_ntp_time(server='pool.ntp.org'):
#     # Create an NTP client
#     ntp_client = ntplib.NTPClient()
#     # Query the NTP server for the current time
#     response = ntp_client.request(server)
#     
#     # Extract and return the current time
#     ntp_time = ctime(response.tx_time)
#     return ntp_time

def get_current_time_for_location(location):
    time_zone=geo.get_timezone_for_location(location);
    res_time=get_current_time_for_timezone(time_zone)
    return  res_time
def get_ntp_time(server='pool.ntp.org'):
    # Create an NTP client
    ntp_client = ntplib.NTPClient()

    # Query the NTP server for the current time
    response = ntp_client.request(server,version=4)
    
    # Convert NTP time to a datetime object in UTC
    ntp_timestamp = response.tx_time
    ntp_time = datetime.utcfromtimestamp(ntp_timestamp)
    server_time_zone=str(get_localzone())
    # .replace(tzinfo=server_time_zone)

    local_time = pytz.utc.localize(ntp_time).astimezone(pytz.timezone(server_time_zone))
    # Convert to your local time zone
    # local_time = utc_time.astimezone()

    return local_time.strftime("%Y-%m-%d %H:%M:%S %Z")

def handle_client(client_socket,client_address):
    try:
        logging.info(f"Connection from {client_socket.getpeername()}")
        while True:
            # Receive the requested timezone from the client
            requested_timezone = client_socket.recv(1024).decode('utf-8')
            # print(type(requested_timezone))
            if not requested_timezone:
                break  # Exit the loop if the client sends an empty string
            if requested_timezone=="getServerTime":
                current_time=get_ntp_time()
                client_socket.sendall(current_time.encode('utf-8'))
                continue
            if requested_timezone=="getServerTimeZone":
                server_timezone=str(get_localzone())
                client_socket.sendall(server_timezone.encode('utf-8'))
                continue
                
            # Basic check for a valid timezone
            if not pytz.all_timezones.__contains__(requested_timezone):
                current_time=get_current_time_for_location(requested_timezone) #requested_timezone is the input(can vary)
                # error_message = f"Invalid timezone: {requested_timezone}"
                client_socket.sendall(current_time.encode('utf-8'))
                continue  # Skip processing invalid input

            current_time = get_current_time_for_timezone(requested_timezone)
            client_socket.sendall(current_time.encode('utf-8'))
    except ssl.SSLError as e:
        print(f"SSL Error: {e}")
        logging.error(f"SSL Error: {e}")
    except Exception as e:
        print(f"Error: {e}")
        logging.error(f"Error: {e}")
    finally:
        logging.info(f"Disconnection from {client_address}")
        print(f"Disconnection from {client_address}")
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
            client_handler = threading.Thread(target=handle_client, args=(client_socket,client_address))
            client_handler.start()
    except KeyboardInterrupt:
        print("Server shutting down...")
    finally:
        # Close the server socket
        server_socket.close()

if __name__ == '__main__':
    main()
