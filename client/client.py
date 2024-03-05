import socket
import time
import ssl
class EmptyInputError(Exception):
    pass

def setTime(client_socket):
    time_zone=input("Enter the time_zone for setting time: ")
    # Send the requested timezone to the server
    client_socket.sendall(time_zone.encode('utf-8'))

    # Receive data from the server
    data = client_socket.recv(1024)
    print(f"New Time set: {data.decode('utf-8')}")
    return time_zone 

def syncTime(client_socket):
    time_zone="getServerTimeZone"
    # Send the requested timezone to the server
    client_socket.sendall(time_zone.encode('utf-8'))

    # Receive data from the server
    data = client_socket.recv(1024)
    newTimeZone=data.decode('utf-8')
    print(f"New Timezone Set: {newTimeZone}")
    print(f"Current Time: {getlocaltime(client_socket,newTimeZone)}")
    return newTimeZone 

def getlocaltime(client_socket,local_time_zone):
    # Send the requested timezone to the server
    client_socket.sendall(local_time_zone.encode('utf-8'))

    # Receive data from the server
    data = client_socket.recv(1024)
    currLocalTime=data.decode('utf-8')
    print(f"{currLocalTime}")
    return currLocalTime 

def get_time_from_server(client_socket):
    print("1. Enter the timezone (e.g., 'America/New_York') or location(e.g., 'New Delhi')\n2. Enter 'getServerTime' to get the server's local time\n3. Enter 'getTime' to get local time\n4. Enter 'setTime' to set the local time\n5. Enter 'syncTime' to sync with server's time\n6. Press Enter to exit: ")

    local_time_zone='NULL'
    while True:
        # Get the desired timezone from the user
        time_zone = input('>> ')
        
        if not time_zone:
            break  # Exit the loop if the user doesn't provide a timezone
        if time_zone=='': 
            break
        if time_zone=="setTime":
            local_time_zone=setTime(client_socket)
            continue
        if time_zone=="getTime":
            if local_time_zone=='NULL':
                local_time_zone=setTime(client_socket)
                continue
            getlocaltime(client_socket,local_time_zone)
            continue
        if time_zone=='syncTime':     
            local_time_zone=syncTime(client_socket)
            continue
        # Send the requested timezone to the server
        client_socket.sendall(time_zone.encode('utf-8'))

        # Receive data from the server
        data = client_socket.recv(1024)
        
        print(f"Time in {time_zone}: {data.decode('utf-8')}")
    return time_zone

def main():
    # Define the server address (host, port)
    server_address = ('localhost', 12345)

    while True:
        # print(1)
    # Create a socket (AF_INET for IPv4, SOCK_STREAM for TCP)
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # print(2)
    # Configure SSL context
        ssl_context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
        ssl_context.load_verify_locations(cafile='server.crt')  # Specify the server's certificate
        # print(3)
    # Wrap the socket with SSL/TLS
        client_socket = ssl_context.wrap_socket(client_socket, server_hostname='localhost')
        # print(4)
        try:
        # Connect to the server
            client_socket.connect(server_address)

        # Call the function to get time from the server
            inp=get_time_from_server(client_socket)
            if inp=='': 
                break

        except socket.error as e:
            print(f"Connection error: {e}")
            print("Reconnecting in 5 seconds...")
            time.sleep(5)
            continue  # Retry the outer loop on connection error
        except Exception as e:
            print(f"Error: {e}")
        except EmptyInputError:
            break

        # finally:
        #     # Clean up the connection
        #     break

    client_socket.close()

if __name__ == "__main__":
    main()

