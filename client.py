import socket
import sys
import threading

# Setting up the client socket for UDP
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# Replace 'localhost' with the actual IP address of your server if it's different
server_address = (socket.gethostbyname(socket.gethostname()), 12345)

# Prompting user for their name
name = (input("Welcome to the Geo Genius Challenge! Please enter your name: "))
if not name:
    print("You must enter a name to join the game.")
    sys.exit()

# Sending the name to the server
client_socket.sendto(name.encode("utf-8"), server_address)

# The first client joining the game must choose number of participants
try:
    while True:
        message, _ = client_socket.recvfrom(1024)
        instruction = message.decode("utf-8")
        print(instruction)

        if "Please enter the number of participants" in instruction:
            num_participants = input("Enter the number of participants: ")
            client_socket.sendto(num_participants.encode("utf-8"), server_address)
            break

except Exception as e:
    print(f"An error occurred: {e}")
finally:
    client_socket.close()