#!/usr/bin/python3
import socket
import threading

# [TO DO] IMPLEMENTAR EM CLASSES PARA TER ACESSO A VARIAVEIS GLOBAIS
# [TO DO] IMPLEMENTAR USE CASE EM COMMAND: q
# [TO DO] É NECESSARIO UTILIZAR 2 THREADS?
# [TO DO] CHAMAR METODO RECEIVE APOS UTILIZAR METODO SEND?(COM 1 THREAD)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

HOST = '127.0.0.1'
PORT = 4001

s.bind((HOST, PORT))

s.listen()

def receive(client, address):
    while True:
        try:
            data = client.recv(1024).decode('utf-8')

            if not data or 'closed' in data:
                print(f'Connection with host: {address} closed')

            print(f'{address}>>>: {data}')
            print(f'{address}>>>: Enter a new command')
        except:
            print(f'Failed to receive data from host: {address}')

def send(client, address):
    while True:
        try:
            cmd = input(f"{address}>>>: ")

            client.send(cmd.encode('utf-8'))
        except:
            print(f'Failed to send command to client')

def main():
    print('Server started')

    while True:
        client, address = s.accept()
        print(f'New connection: {str(address)}')

        send_thread = threading.Thread(group=None, target=send, args=(client, address), daemon=True)
        send_thread.start()

        receive_thread = threading.Thread(group=None, target=receive, args=(client, address), daemon=True)
        receive_thread.start()

if __name__ == '__main__':
    main()