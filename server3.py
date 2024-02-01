import threading
from helpers import create_server_socket, handle_client, send_broadcast, IP, BROADCAST_PORT_SERVER


server_port = 12342
broadcast_port_bind = 12352

node_addr = f'{IP} {server_port}'

game_conf = {
    'difficulty': 'easy',
    'num_of_player': 3,
    'countdown': 10
}

if __name__ == '__main__':

    # sending broadcast 
    send_broadcast_thread = threading.Thread(target=send_broadcast, args=(node_addr,broadcast_port_bind, BROADCAST_PORT_SERVER))
    send_broadcast_thread.start()

    # creating server threads 
    server = create_server_socket(IP, server_port)
    while True:
        client, addr = server.accept()
        # start new thread to handle client 
        client_thread = threading.Thread(target=handle_client, args=(client, addr, game_conf))
        client_thread.start()
    
