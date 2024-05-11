#!/usr/bin/env python3
import socket
import threading
from customtkinter import *
from tkinter.scrolledtext import ScrolledText

def send_message(client_socket, username, text_chat, entry_chat):
    message = entry_chat.get()
    client_socket.sendall(f"{username} > {message}".encode())

    entry_chat.delete(0, END)
    #text_chat.configure(state='normal')
    #text_chat.insert("end", f"{username} > {message}\n")
    #text_chat.configure(state='disabled')

def receive_mesage(client_socket, text_chat):
    while True:
        try:
            message = client_socket.recv(1024).decode()
            if not message:
                break

            text_chat.configure(state='normal')
            text_chat.insert("end", message)
            text_chat.configure(state='disabled')
        except:
            break


def run_client():
    host = 'localhost'
    port = 12345
    destination_addr = (host, port)

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(destination_addr)

    username = input("\n[+] Enter username: ")
    client_socket.sendall(username.encode())

    # Window
    window = CTk()
    window.title("Chat")
    set_appearance_mode("dark")

    text_chat = ScrolledText(window, state='disabled')
    text_chat.pack(padx=5, pady=5)

    entry_chat = CTkEntry(window)
    entry_chat.bind("<Return>", lambda _: send_message(client_socket, username, text_chat, entry_chat))
    entry_chat.pack(padx=5, pady=5, fill=BOTH)

    thread = threading.Thread(target=receive_mesage, args=(client_socket, text_chat))
    thread.daemon = True
    thread.start()

    window.mainloop()
    client_socket.close()

if __name__ == "__main__":
    run_client()
