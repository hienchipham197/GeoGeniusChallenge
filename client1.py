from helpers import send_message, init_client_socket, discover_hosts
import threading
import pickle
import json

# username = {'username':None}


if __name__ == '__main__':
    [ip, port] = discover_hosts().split(' ')
    c_socket = init_client_socket(ip, port)
    username = {}
    
    # check if username exists ,if username not found, send a request to get username
    with open('clientstate1.json') as f:
        read = json.load(f)
        if not read['username']:
            c_socket.send(pickle.dumps({'command': 'username_request', 'params':None}))
        else:
            username = read
            c_socket.send(pickle.dumps({'command': 'send_username', 'params':username}))

    # start message listening thread
    send_mes_thread = threading.Thread(target=send_message, args=(c_socket, username))
    send_mes_thread.start()

    while True:
        try:
            data = c_socket.recv(1024)
            if not data:
                print('socket closed')
            res = pickle.loads(data)
            if res['command'] == 'setuser':
                with open('clientstate1.json', 'w') as f:
                    username['username'] = pickle.loads(data)['params']
                    json.dump(username, f)
            elif res['command'] == 'sendall':
                print(res['content'])
            elif res['command'] == 'question':
                print(f"\n\nQuestion: {res['content']['question']}")
                for i in range(len(res['content']['answers'])):
                    print(f"{i+1}. {res['content']['answers'][i]}")
            elif res['command'] == 'reply':
                print(res['content'])

        except ConnectionResetError as e:
            print(e)
            break
    c_socket.close()
    exit()