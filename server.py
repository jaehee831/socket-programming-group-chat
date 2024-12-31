import socket
import threading

# Server settings
HOST = '127.0.0.1'
PORT = 5000

# Data structure to store chat rooms and clients
chat_rooms = {}

def handle_client(client_socket):
    client_socket.send("Welcome!".encode())
    
    current_room = None
    while True:
        try:
            msg = client_socket.recv(1024).decode()
            if not msg:
                break

            if msg.startswith('/create'):
                room_name = msg.split(' ', 1)[1]
                if room_name in chat_rooms:
                    client_socket.send("The room already exists.".encode())
                else:
                    chat_rooms[room_name] = []
                    client_socket.send(f"Room '{room_name}' created.".encode())

            elif msg.startswith('/join'):
                room_name = msg.split(' ', 1)[1]
                if current_room:
                    client_socket.send("You have to leave your current room first.".encode())
                elif room_name in chat_rooms:
                    chat_rooms[room_name].append(client_socket)
                    current_room = room_name
                    client_socket.send(f"Joined room '{room_name}'.".encode())
                else:
                    client_socket.send(f"Room '{room_name}' does not exist.".encode())
                    
            elif msg.startswith('/leave'):
                if current_room and client_socket in chat_rooms[current_room]:
                    chat_rooms[current_room].remove(client_socket)
                    client_socket.send(f"Left room '{current_room}'.".encode())
                    current_room = None
                else:
                    client_socket.send("You're not in a room.".encode())
                    
            else:
                # Send message to all clients in the current room
                if current_room:
                    for client in chat_rooms[current_room]:
                        if client != client_socket:
                            client.send(f"{msg}".encode())
                else:
                    client_socket.send("Join a room to send messages.".encode())

        except:
            break

    client_socket.close()
    remove_client(client_socket, current_room)

def remove_client(client_socket, room_name):
    if room_name and client_socket in chat_rooms.get(room_name, []):
        chat_rooms[room_name].remove(client_socket)

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(5)
    print("Server started on port", PORT)
    
    while True:
        client_socket, client_address = server_socket.accept()
        print(f"New connection from {client_address}")
        threading.Thread(target=handle_client, args=(client_socket,)).start()

if __name__ == "__main__":
    main()
