#!/usr/bin/env python3
import socket

def run_client():
    host = 'localhost'
    port = 123435
    destination_addr = (host, port)

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(destination_addr)

    username = input("\n[+] Enter username: ")
    client_socket.sendall(username.encode())

if __name__ == "__main__":
    run_client()
