from helpers import IP, handle_client_queue, handle_server_queue, lb_discover_hosts, create_server_socket, lb_handle_client, lb_listen_to_node, send_broadcast,BROADCAST_PORT_LB, leader_vote
import threading



node_list = []
node_socket_list = []
leader_node_socket_index = {'index':None}
lb_port = 12344
lb_broadcast_port = 12354
lb_addr = f'{IP} {lb_port}'
client_list = {}
client_mes_queue = []
server_mes_queue = []


if __name__ == '__main__':

   # start listening broadcast from servers 
   broadcast_receive_thread = threading.Thread(target=lb_discover_hosts, args= (node_list, node_socket_list, leader_node_socket_index)) 
   broadcast_receive_thread.start()

   #start sending broadcast to client
   broadcast_sending_thread = threading.Thread(target=send_broadcast, args=(lb_addr, lb_broadcast_port, BROADCAST_PORT_LB ))
   broadcast_sending_thread.start()

   # initialize leader node
   while leader_node_socket_index['index'] is None:
      if len(node_socket_list) >= 1:
         leader_node_socket_index['index']=leader_vote(node_socket_list.__len__())
   node_socket = node_socket_list[leader_node_socket_index['index']]

   print('initialize leader node')

   # start listening node messages 
   listen_node_mes_thread = threading.Thread(target=lb_listen_to_node, args=(node_socket_list,leader_node_socket_index, server_mes_queue ))
   listen_node_mes_thread.start()

   # start handle client message queue thread
   handle_message_client_thread = threading.Thread(target=handle_client_queue, args=(client_mes_queue, node_socket_list, leader_node_socket_index))
   handle_message_client_thread.start()

   # start server message queue thread
   handle_message_server_thread = threading.Thread(target=handle_server_queue, args=(server_mes_queue, client_list))
   handle_message_server_thread.start()


   lb_socket = create_server_socket(IP, lb_port)
   while True:
      
      client, addr = lb_socket.accept()
      client_thread = threading.Thread(target=lb_handle_client, args=(client, addr, client_mes_queue, client_list))
      client_thread.start()

      


    
   
    