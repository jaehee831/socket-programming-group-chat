import socket
import threading
import tkinter as tk
from tkinter import scrolledtext, messagebox

HOST = '127.0.0.1'
PORT = 5000

class ChatClient:
    def __init__(self, root):
        self.root = root
        self.root.title("Multi-Room Chat Client")
        
        # Room selection
        self.room_entry = tk.Entry(self.root, width=20)
        self.room_entry.pack(padx=20, pady=5)
        
        # Buttons for room management
        tk.Button(self.root, text="Create Room", command=self.create_room).pack(pady=2)
        tk.Button(self.root, text="Join Room", command=self.join_room).pack(pady=2)
        tk.Button(self.root, text="Leave Room", command=self.leave_room).pack(pady=2)
        
        # Chat area
        self.chat_area = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, state='disabled')
        self.chat_area.pack(padx=20, pady=5)
        
        # Message input field
        self.msg_entry = tk.Entry(self.root, width=50)
        self.msg_entry.pack(padx=20, pady=5)
        self.msg_entry.bind("<Return>", self.send_message)
        
        # Connection settings
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.current_room = None  # Track the current room
        self.stop_receiving = False  # To stop receiving messages after leaving a room

        try:
            self.client_socket.connect((HOST, PORT))
            threading.Thread(target=self.receive_messages, daemon=True).start()
        except Exception as e:
            messagebox.showerror("Connection Error", f"Unable to connect to server: {e}")
            self.root.destroy()

    def create_room(self):
        room_name = self.room_entry.get()
        if room_name:
            self.client_socket.send(f"/create {room_name}".encode())
            self.current_room = room_name
            self.stop_receiving = False  # Reset stop_receiving

    def join_room(self):
        room_name = self.room_entry.get()
        if room_name:
            self.client_socket.send(f"/join {room_name}".encode())
            self.current_room = room_name
            self.stop_receiving = False  # Reset stop_receiving

    def leave_room(self):
        if self.current_room:
            self.client_socket.send(f"/leave {self.current_room}".encode())
            self.current_room = None
            self.stop_receiving = True  # Prevent further messages from being displayed
            
            # Clear chat history in the UI
            self.chat_area.config(state='normal')
            self.chat_area.delete('1.0', tk.END)
            self.chat_area.config(state='disabled')

    def receive_messages(self):
        while True:
            try:
                msg = self.client_socket.recv(1024).decode()
                if msg:
                    # If the client has left the room, stop displaying messages
                    if not self.stop_receiving:
                        self.chat_area.config(state='normal')
                        self.chat_area.insert(tk.END, msg + '\n')
                        self.chat_area.config(state='disabled')
                        self.chat_area.see(tk.END)
            except:
                break

    def send_message(self, event=None):
        msg = self.msg_entry.get()
        if msg and self.current_room:
            # Display own message in the chat area before sending to server
            self.chat_area.config(state='normal')
            self.chat_area.insert(tk.END, f"You: {msg}\n")
            self.chat_area.config(state='disabled')
            self.chat_area.see(tk.END)

            # Send message to server
            self.client_socket.send(msg.encode())
            self.msg_entry.delete(0, tk.END)

    def on_closing(self):
        self.client_socket.close()
        self.root.destroy()

# Tkinter main window
root = tk.Tk()
client = ChatClient(root)
root.protocol("WM_DELETE_WINDOW", client.on_closing)
root.mainloop()
