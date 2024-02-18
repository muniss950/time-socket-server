import socket
import ntplib
from datetime import datetime
import pytz

URL='time.google.com'
# Define the server address (host, port)
server_address = ('localhost', 12345)

# Create a socket (AF_INET for IPv4, SOCK_STREAM for TCP)
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the server address
server_socket.bind(server_address)

# Listen for incoming connections (accept up to 5 connections)
server_socket.listen(5)
print(f"Server listening on {server_address}")

def get_current_time(time_zone):
    try:
        # Use NTP to get the current time
        ntp_client = ntplib.NTPClient()
        response = ntp_client.request(URL, version=4)

        # Convert NTP time to the specified time zone using pytz
        ntp_time = datetime.utcfromtimestamp(response.tx_time)
        local_time = pytz.utc.localize(ntp_time).astimezone(pytz.timezone(time_zone))

        return local_time.strftime("%Y-%m-%d %H:%M:%S %Z")
    except ntplib.NTPException:
        return "Error getting NTP time"
    except pytz.UnknownTimeZoneError:
        return "Unknown time zone"

while True:
    # Wait for a connection
    client_socket, client_address = server_socket.accept()
    print(f"Connection from {client_address}")

    try:
        # Receive the requested time zone from the client
        requested_time_zone = client_socket.recv(1024).decode('utf-8')

        # Get the current time for the requested location
        current_time = get_current_time(requested_time_zone)

        # Send the current time to the client
        client_socket.sendall(current_time.encode('utf-8'))
    finally:
        # Clean up the connection
        client_socket.close()
