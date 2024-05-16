import socket
import threading
import json
import parallel_quicksort as pq
from queue import Queue
from datetime import datetime

# Server configuration
PORT = 5000
SERVER = socket.gethostbyname(socket.gethostname())  # Get local server IP address
ADDRESS = (SERVER, PORT)
DISCONNECT_MESSAGE = "DISCONNECT"  # Message to disconnect client
MAXIMUM_BYTES = 2048  # Maximum bytes to receive

# Create server socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDRESS)  # Bind server to address

# Function to respond to client requests
def respondToClient(connection, address):
    print(f"[{getCurrTime()}][CONNECTION] A new client with (address, port): {address} has connected.")

    isConnected = True
    while isConnected:
        receivedArray = connection.recv(MAXIMUM_BYTES).decode()  # Receive data from client
        if receivedArray:
            unpackedArray = json.loads(receivedArray)  # Unpack JSON data from client

            if unpackedArray == DISCONNECT_MESSAGE:
                isConnected = False
                break  # Break loop if client wants to disconnect

            resultQueue = Queue()
            pq.parallelQuicksort(unpackedArray, resultQueue)  # Perform parallel quicksort

            sortedArray = resultQueue.get()
            packedSortedArray = json.dumps(sortedArray)  # Pack sorted array into JSON

            connection.send(packedSortedArray.encode())  # Send sorted array back to client
            print(f"[{getCurrTime()}][SUCCESSFUL] Successfully processed the query of client: {address}")

    print(f"[{getCurrTime()}][DISCONNECTED] Client: {address} has disconnected!")

    connection.close()  # Close connection with client

    print(f"Active connections at the moment: {threading.active_count() - 2}")

# Start server
def start():
    print(f"[{getCurrTime()}][STARTING] SERVER is setting up...")
    server.listen()  # Start listening for incoming connections
    print(f"[{getCurrTime()}][LISTENING] Server is listening on: {SERVER}")
    while True:
        connection, address = server.accept()  # Accept new client connection
        thread = threading.Thread(target=respondToClient, args=(connection, address))  # Create new thread for client
        thread.start()  # Start thread to handle client request
        print(f"Active connections at the moment: {threading.active_count() - 1}")

# Function to get current time
def getCurrTime():
    return datetime.now().strftime("%H:%M:%S")

start()
