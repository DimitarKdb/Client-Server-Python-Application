import socket
import json

# Server configuration
PORT = 5000
SERVER = "192.168.137.1"  # Server IP address
ADDRESS = (SERVER, PORT)
DISCONNECT_MESSAGE = "DISCONNECT"  # Message to disconnect client
MAXIMUM_BYTES = 2048  # Maximum bytes to receive

clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Create client socket

# Function to send array to server and receive sorted array
def sortArrayOnServer(array):
    json_packed_array = json.dumps(array)  # Pack array into JSON
    clientSocket.send(json_packed_array.encode())  # Send JSON data to server

    sortedArray = clientSocket.recv(MAXIMUM_BYTES).decode()  # Receive sorted array from server
    
    print(f"Sorted array is: {sortedArray}")

# Function to connect to server and interact with it
def connectToServer():
    clientSocket.connect(ADDRESS)  # Connect to server

    query = ""
    serverIntroduction()

    while True:
        query = input("<> ")  # Prompt user for input
        query = query.strip().lower()  # Convert input to lowercase and remove leading/trailing spaces
        
        if query == "disconnect":
            sortArrayOnServer(DISCONNECT_MESSAGE)  # Send disconnect message to server
            print("Your connection to the server has successfully been closed!")
            return  # Exit the function and close the connection

        elif query == "array":
            array = readArrayFromInput()  # Read array from user input

            if(array == -1):
                continue

            sortArrayOnServer(array)  # Send array to server for sorting

        else:
            print("Invalid command, try again!")  # Notify user of invalid command
            continue  # Continue loop for new input

        print("Your query has been successfully processed! Make a new query!")

# Function to read array input from user
def readArrayFromInput():

    input_string = input("Enter the array elements separated by space: ")  # Prompt user for array input

    array = input_string.split()  # Split input string by space to get individual elements
 
    try:
        array = [int(x) for x in array]  # Convert elements to integers
    except:
        print("Array input was invalid, please try another query!")
        return -1

    return array


# Function to display server introduction message
def serverIntroduction():
    print("You are connected to the server!")
    print("Type \"Disconnect\" to disconnect from the server!")
    print("Type \"Array\" to send an array to be sorted to the server!")


# Call function to connect to server and start interaction
connectToServer()
