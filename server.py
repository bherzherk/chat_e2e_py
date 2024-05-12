#!/usr/bin/env python3
import socket
import threading
import ssl

def p(trace):
    print(f"[+] {trace}")

def client_thread(client_socket, clients, usernames):
    username  = client_socket.recv(1024).decode()
    usernames[client_socket] = username

    #print(f"The username is: {username}")
    
    for client in clients:
        if client is not client_socket:
            client.sendall(f"\n[+] The user {username} has joined to the chat.\n".encode())

    while True:
        try:
            message = client_socket.recv(1024).decode()

            if not message:
                break

            if message == "!users":
                client_socket.sendall(f"\n[+] Users connected: {', '.join(usernames.values())}\n".encode())
                continue

            for client in clients:
                client.sendall(f"{message}\n".encode())
        except:
            break

    client_socket.close()
    clients.remove(client_socket)
    del usernames[client_socket]

def run_server():
    host = 'localhost'
    port = 12345
    server_addr = (host, port)

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # Wait time
    server_socket.bind(server_addr)
    server_socket = ssl.wrap_socket(server_socket, keyfile="server-key.key", certfile="server-cert.pem", server_side=True)
    server_socket.listen()

    p("Server listening...")

    clients = []
    usernames = {}

    while True:
        client_socket,client_addr = server_socket.accept()
        clients.append(client_socket)

        p("New client")
        p(client_addr)
        
        thread = threading.Thread(target=client_thread, args=(client_socket, clients, usernames))
        thread.daemon = True
        thread.start()

    server_socket.close()

if __name__ == '__main__':
    run_server()
