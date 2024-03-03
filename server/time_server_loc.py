import socket
import ntplib
from datetime import datetime
import pytz
from geopy.geocoders import Nominatim

# Define the server address (host, port)
server_address = ('localhost', 12345)

# Create a socket (AF_INET for IPv4, SOCK_STREAM for TCP)
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the server address
server_socket.bind(server_address)

# Listen for incoming connections (accept up to 5 connections)
server_socket.listen(5)
print(f"Server listening on {server_address}")

def get_current_time_for_location(city_name):
    geolocator = Nominatim(user_agent="location_info")
    location = geolocator.geocode(city_name)

    if location:
        # Get the time zone for the location
        time_zone = str(pytz.timezone(geolocator.timezone_at(latlng=(location.latitude, location.longitude))))
        
        # Use NTP to get the current time in that time zone
        ntp_client = ntplib.NTPClient()
        response = ntp_client.request('pool.ntp.org', version=4)
        
        ntp_time = datetime.utcfromtimestamp(response.tx_time)
        local_time = pytz.utc.localize(ntp_time).astimezone(pytz.timezone(time_zone))

        return local_time.strftime("%Y-%m-%d %H:%M:%S %Z")
    else:
        return f"Time information not available for {city_name}"

while True:
    # Wait for a connection
    client_socket, client_address = server_socket.accept()
    client_socket.settimeout(10)  # Set a 10-second timeout for this client
    print(f"Connection from {client_address}")

    try:
        # Receive the requested city name from the client
        requested_city = client_socket.recv(1024).decode('utf-8')

        # Get the current time for the requested city
        current_time = get_current_time_for_location(requested_city)

        # Send the current time to the client
        client_socket.sendall(current_time.encode('utf-8'))
    except Exception as e:
        print(f"Error: {e}")
    finally:
        # Clean up the connection
        client_socket.close()
