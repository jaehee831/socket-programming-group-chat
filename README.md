# Multi-Room Chat Application

This project is a multi-room chat application that allows multiple users to communicate in real-time across different chat rooms over a network. The application consists of two main components:

- **`server.py`**: A server program that manages chat rooms and client connections.
- **`client.py`**: A client program with a graphical user interface (GUI) for joining or creating chat rooms and sending messages.

---

## **1. Features**
- Real-time communication across multiple chat rooms.
- User-friendly GUI for chat room management and messaging.
- Server-side management of users and chat rooms.

---

## **2. How to Run the Application**
### **Prerequisites**
1. **Python 3.x**:
   - Ensure Python is installed on your system.
   - Check the version:
     ```bash
     python --version
     ```
2. **Required Libraries**:
   - Built-in libraries: `socket`, `threading`, `tkinter`.
   - No additional installation is needed.

### **Steps**
1. **Download the Code Files**:
   - Save `server.py` and `client.py` in the same directory.
2. **Run the Server**:
   - Open a terminal in the directory where the files are located.
   - Start the server:
     ```bash
     python server.py
     ```
3. **Run the Client**:
   - Open a new terminal for each client instance.
   - Start the client:
     ```bash
     python client.py
     ```

---

## **3. Code Overview**
### **Server (`server.py`)**
- Listens for incoming client connections.
- Manages multiple chat rooms and user sessions.
- Broadcasts messages to all users in the same chat room.

### **Client (`client.py`)**
- Provides a GUI for users to:
  - Join or create chat rooms.
  - Send and receive messages.
- Handles communication with the server.

---

## **4. Future Enhancements**
- Add user authentication for secure access.
- Implement message encryption for privacy.
- Enable file sharing within chat rooms.
- Enhance GUI features for improved usability.
