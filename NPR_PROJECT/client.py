import socket
import json

PORT = 5000
SERVER = "192.168.137.1"
ADDRESS = (SERVER, PORT)
DISCONNECT_MESSAGE = "DISCONNECT"
MAXIMUM_BYTES = 2048

clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def sortArrayOnServer(array):
    json_packed_array = json.dumps(array)
    clientSocket.send(json_packed_array.encode())

    sortedArray = clientSocket.recv(MAXIMUM_BYTES).decode()
    
    print(f"Sorted array is: {sortedArray}")

def connectToServer():
    clientSocket.connect(ADDRESS)

    query = ""
    serverIntroduction()

    while(True):
        query = input("<> ")
        query = query.strip().lower()
        
        if(query == "disconnect"):
            sortArrayOnServer(DISCONNECT_MESSAGE)
            print("Your connection to the server has sucessfully been closed!")
            return

        elif(query == "array"):
            array = readArrayFromInput()
            sortArrayOnServer(array)

        else:
            print("Invalid command, try again!")
            continue

        print("Your query has been sucessfully processed! Make a new query!")


def readArrayFromInput():
    # Ask the user to input the array elements
    input_string = input("Enter the array elements separated by space: ")

    # Split the input string by space to get individual elements
    array = input_string.split()

    # Convert elements to the desired data type if needed
    array = [int(x) for x in array]  # Convert elements to integers

    return array


def serverIntroduction():
    print("You are connected to the server!")
    print("Type \"Disconnect\" to disconnect from the server!")
    print("Type \"Array\" so you can send an array to be sorted to the server!")


connectToServer()



