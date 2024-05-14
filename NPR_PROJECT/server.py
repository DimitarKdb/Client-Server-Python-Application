import socket
import threading
import json
import parallel_quicksort as pq
from queue import Queue
from datetime import datetime

PORT = 5000
#SERVER = "192.168.0.107"
#automatically does the upper thing for us
SERVER = socket.gethostbyname(socket.gethostname())
ADDRESS = (SERVER, PORT)
DISCONNECT_MESSAGE = "DISCONNECT"
MAXIMUM_BYTES = 2048

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDRESS)

def respondToClient(connection, address) : 
    print(f"[{getCurrTime()}][CONECTION] A new client with (address, port): {address} has connected.")

    isConnected = True
    while isConnected:
        recievedArray = connection.recv(MAXIMUM_BYTES).decode() #this line is blocking the program, so it needs a new thread
        if recievedArray:
            unpackedArray = json.loads(recievedArray)

            if(unpackedArray == DISCONNECT_MESSAGE):
                isConnected = False
                break

            resultQueue = Queue()
            pq.parallelQuicksort(unpackedArray, resultQueue)

            sortedArray = resultQueue.get()
            packedSortedArray = json.dumps(sortedArray)

            connection.send(packedSortedArray.encode())
            print(f"[{getCurrTime()}][SUCESSFULL] Sucessfully processed the query of client: {address}")
        

    print(f"[{getCurrTime()}][DISCONNECTED] Client: {address} has disconected!")

    connection.close()

    print(f"Active connections at the moment: {threading.active_count() - 2}")


def start():
    server.listen()
    print(f"[{getCurrTime()}][LISTENING] Server is listening on: {SERVER}")
    while True:
        connection, address = server.accept() #this line is blocking the program, so it needs a new thread
        thread = threading.Thread(target = respondToClient, args=(connection, address))
        thread.start()
        print(f"Active connections at the moment: {threading.active_count() - 1}")



def getCurrTime():
    return datetime.now().strftime("%H:%M:%S")

print(f"[{getCurrTime()}][STARTING] SERVER is setting up...")
start()