import socket
import time

def get_time_from_server():
    # Define the server address (host, port)
    server_address = ('localhost', 12345)

    while True:
        # Create a socket (AF_INET for IPv4, SOCK_STREAM for TCP)
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            # Connect to the server
            client_socket.connect(server_address)

            while True:
                # Get the location from the user
                location = input("Enter time zone (e.g., 'America/New_York', 'UTC'): ")

                if not location:
                    break  # Exit the loop if the user doesn't provide a location

                # Send the location to the server
                try:
                    client_socket.sendall(location.encode('utf-8'))
                except socket.error as e:
                    print(f"Error sending data: {e}")
                    break  # Exit the inner loop on error

                try:
                    # Receive data from the server
                    data = client_socket.recv(1024)
                    print(f"Time in {location}: {data.decode('utf-8')}")
                except socket.error as e:
                    print(f"Error receiving data: {e}")
                    break  # Exit the inner loop on error

        except socket.error as e:
            print(f"Connection error: {e}")
            print("Reconnecting in 5 seconds...")
            time.sleep(5)
            continue  # Retry the outer loop on connection error

        except Exception as e:
            print(f"Error: {e}")

        finally:
            # Clean up the connection
            client_socket.close()

if __name__ == "__main__":
    get_time_from_server()
