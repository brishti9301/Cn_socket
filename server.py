# import socket module 
from socket import * 
import sys  # In order to terminate the program 

def webServer(port=6789):
    serverSocket = socket(AF_INET, SOCK_STREAM)  # Prepare a server socket
    serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    
    # Bind and listen
    serverSocket.bind(('', port))          # Bind the socket to all interfaces and given port
    serverSocket.listen(1)                 # Listen for incoming connections (backlog = 1)

    while True:
        # Establish the connection
        print('Ready to serve...')
        connectionSocket, addr = serverSocket.accept()
        print(f'Connection established with {addr}')

        try:
            message = connectionSocket.recv(1024).decode()

            if not message:
                connectionSocket.close()
                continue

            # Print first request line for clarity
            request_line = message.splitlines()[0]
            print(f'Request: {request_line}')

            filename = message.split()[1]
            f = open(filename[1:])                   # remove leading "/" 
            outputdata = f.read()

            # Send one HTTP header line into socket
            connectionSocket.send("HTTP/1.1 200 OK\r\n\r\n".encode())
            print("Responded with: 200 OK")

            # Send the content of the requested file to the client
            for i in range(0, len(outputdata)):
                connectionSocket.send(outputdata[i].encode())

            connectionSocket.close()

        except IOError:
            # Send response message for file not found
            connectionSocket.send("HTTP/1.1 404 Not Found\r\n\r\n".encode())
            connectionSocket.send("<html><body><h1>404 Not Found</h1></body></html>".encode())
            print("Responded with: 404 Not Found")

            # Close client socket
            connectionSocket.close()

    serverSocket.close()
    sys.exit()  # Terminate the program after sending the corresponding data

if __name__ == "__main__":
    webServer(6789)
