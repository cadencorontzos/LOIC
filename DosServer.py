# Import socket module
from socket import *
import os
from _thread import *
import sys
import resource


resource.setrlimit(resource.RLIMIT_NOFILE, (resource.RLIM_INFINITY,resource.RLIM_INFINITY))

# Prepare server socket
# SOCK_STREAM for TCP, SOCK_DGRAM for UDP
serverSocket = socket(AF_INET, SOCK_STREAM)
numThreads = 0
serverPort = 12000
serverSocket.bind(('',serverPort))
serverSocket.listen(5)

print("Server is ready to recieve")

def singleThread(connectionSocket):
    pass

    while True:
        try:
            #Gets the request
            message = connectionSocket.recv(1024)
            
            if not message:
                break
            
            message = message.decode()
            #print(message)
            #Finds and opens file
            filename = message.split()[1]
            contentLength = os.path.getsize(filename)
            f = open(filename)
            outputdata = f.read()


            # Send one HTTP header line to socket
            connectionSocket.send('HTTP/1.1 200 OK\r\n'.encode())


            #Sends Content Length
            connectionSocket.send(('Content-Length: ' + str(contentLength) + " \r\n").encode())

            #Send object to client
            connectionSocket.send('Data:'.encode())
            connectionSocket.sendall(outputdata.encode())
            connectionSocket.send("\r\n".encode())

          
        except ConnectionResetError:
            pass
            print('connection reset')
        except BrokenPipeError:
            pass
            print('broken pipe')
            
        except OSError as e:
            print(e)
        except IOError:
            e = sys.exc_info()[0]
            print('in except '+str(e))

            # Send 404 message
            try:
                connectionSocket.send('HTTP/1.1 404 Not Found\r\n\r\n'.encode())
            except BrokenPipeError:
                print('broken pipe on the 404')
                pass

            # Close client socket

        

#This loop will continue to make threads as clients connect
while True:
    # Establish connection
    connectionSocket, addr = serverSocket.accept()
    
    print('Connected to: ' + addr[0] + ': On port # ' + str(addr[1]))
    
    start_new_thread(singleThread, (connectionSocket, ))
    
    numThreads+=1
    
    print('Thread Number: ' + str(numThreads))
#Close server socket
serverSocket.close()
