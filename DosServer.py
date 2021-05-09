#Author: Caden Corontzos
#May 2021

"""

An HTTP server capable of handling multiple connections. This server only supports GET requests. It does this
via multithreading. This is really only meant as an avenue for testing that does not involve breaking the law. 

"""

from socket import *
import os
from _thread import *
import sys
import resource

#Allows more file opens than normal => more threads can be handled on the server
resource.setrlimit(resource.RLIMIT_NOFILE, (resource.RLIM_INFINITY,resource.RLIM_INFINITY))

#sets a TCP socket
serverSocket = socket(AF_INET, SOCK_STREAM)
numThreads = 0

#Gets server port from cli arguments
if len(sys.argv) == 2:
    serverPort = int(sys.argv[1])
else:
    #if the cl arugments are in wrong format, print and quit program
    print ("Please format as follows:\n\n " + sys.argv[0] + " < Port Number > \n")
    sys.exit(1)


serverSocket.bind(('',serverPort))
serverSocket.listen(5)
print("Server is ready to recieve")

#How the server communicates with a single connection
def singleThread(connectionSocket):
    
    while True:
        try:
            #Gets the request
            message = connectionSocket.recv(1024)
            if not message:
                break
            message = message.decode()
          
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

        #handles various exceptions that may occur  
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
