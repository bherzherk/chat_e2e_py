#!/usr/bin/env python3
import socket
import threading
from customtkinter import *
from tkinter.scrolledtext import ScrolledText

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
#    entry_chat.bind("Return", lambda)
    entry_chat.pack(padx=5, pady=5, fill=BOTH)

    window.mainloop()
    client_socket.close()

if __name__ == "__main__":
    run_client()
