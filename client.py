#!/usr/bin/env python3
import socket
import threading
from customtkinter import *
from tkinter.scrolledtext import ScrolledText
from CTkMenuBar import *
import ssl

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

def list_users_request(client_socket):
    client_socket.sendall("!users".encode())

def exit_request(client_socket, username, window):
    client_socket.sendall(f"\n[+] The user {username} left.\n".encode())
    client_socket.close()

    window.quit()
    window.destroy()

def run_client():
    host = 'localhost'
    port = 12345
    destination_addr = (host, port)

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket = ssl.wrap_socket(client_socket)
    client_socket.connect(destination_addr)

    username = input("\n[+] Enter username: ")
    client_socket.sendall(username.encode())

    # Window
    window = CTk()
    window.title("Chat")
    window.resizable(width=False, height=False)
    set_appearance_mode("dark")

    #menu
    menu_bar = CTkMenuBar(window)
    user_menu = menu_bar.add_cascade(username + " options")

    dropdown = CustomDropdownMenu(widget=user_menu)
    dropdown.add_option(option="Online users", font=("Arial", 12), command= lambda : list_users_request(client_socket))
    dropdown.add_option(option="Exit", font=("Arial", 12), command= lambda : exit_request(client_socket, username, window))

    text_chat = ScrolledText(window, state='disabled')
    text_chat.pack(padx=5, pady=5)

    frame_entr_btn = CTkFrame(window)
    frame_entr_btn.pack(padx=5, pady=5, fill=BOTH)

    entry_chat = CTkEntry(frame_entr_btn)
    entry_chat.bind("<Return>", lambda _: send_message(client_socket, username, text_chat, entry_chat))
    entry_chat.pack(side=LEFT, fill=BOTH, expand=1)

    send_button = CTkButton(frame_entr_btn, text="Send", command=lambda : send_message(client_socket, username, text_chat, entry_chat))
    send_button.pack(side=RIGHT, padx=5)

    thread = threading.Thread(target=receive_mesage, args=(client_socket, text_chat))
    thread.daemon = True
    thread.start()

    window.mainloop()
    client_socket.close()

if __name__ == "__main__":
    run_client()
