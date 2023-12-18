import socket
import random
from question import Q_and_A

MSG_LEN = 5
random.shuffle(Q_and_A)

# Setting up the server socket for UDP
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #Allow the server to bind to the same port after being restarted, without waiting for the operating system to release it
server_socket.bind((socket.gethostbyname(socket.gethostname()), 12345))

print("Server of the Geo-Genius Game started")
print("Waiting for connection of players ...")
print("======================================")

clients_list = []
participants = {}
marks = {}
mapping = {}
Person = [server_socket]
answer = [-1]
first_client = True
desired_participants = 0

#Receive name, IP Address, and Port number of clients
while True:
    message, address = server_socket.recvfrom(1024)
    client_name = message.decode("utf-8")
    clients_list.append((client_name, address))
    print(f"User {client_name} is joining the game: IP {address[0]}, Port {address[1]}")
    print("=======================================")

    if first_client:
        first_client = False
        server_socket.sendto("You are the first player. Please enter the number of participants (max allowed number is 4):".encode("utf-8"), address)
        num_participants_message, _ = server_socket.recvfrom(1024)
        desired_participants = int(num_participants_message.decode("utf-8"))
        print(f"Number of participants is chosen: {desired_participants}.")
        print("Waiting for other participants to join...")
        print("=======================================")
        
    if len(clients_list) >= desired_participants:
        print("All participants have joined. Starting the game.")
        print("=======================================")
        # Logic to start the game
        break
        