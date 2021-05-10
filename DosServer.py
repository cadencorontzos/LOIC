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
import resource         #resource module not supported on windows
import time

#Allows more file opens than normal => more threads can be handled on the server
resource.setrlimit(resource.RLIMIT_NOFILE, (resource.RLIM_INFINITY,resource.RLIM_INFINITY)) #comment out on windows machines#

#Gets server port from cli arguments
if len(sys.argv) == 2:
    serverPort = int(sys.argv[1])
else:
    #if the cl arugments are in wrong format, print and quit program
    print ("Please format as follows:\n\n " + sys.argv[0] + " < Port Number > \n")
    sys.exit(1)

#sets a TCP socket
serverSocket = socket(AF_INET, SOCK_STREAM)
numThreads = 0
serverSocket.bind(('',serverPort))
serverSocket.listen(5)
print("Server is ready to recieve. Press ^C to quit.")

"""
Here are two simple ways that the server could try to protect itself. One is to keep track of the time elapsed, and have a set number of requests per second that is allowed.
Presumably, the allowedReqPerSec could be set based of of average usage, and it could also be made to change by time of day. I've chose 10 because from testing, that is about where the
server starts to slow down.

Another is to keep track of how many clients are connected from the same IP. Stupid, I know. Nonetheless, it could work. I've arbitrarily picked 200, but this could be any number within reason.

"""

#sets us to track req/sec
startTime = time.time()
getTimeElapsed = lambda startTime:  time.time()-startTime
allowedReqPerSec = 10
totRequests = 0

#sets us up to track connections from same IP
connectionsFromIP = {}
allowedConnectionsPerIP = 200


#How the server communicates with a single connection
def singleThread(connectionSocket):
    global totRequests
    while True:
        try:
            #Gets the request
            message = connectionSocket.recv(1024)
            if not message:
                break
          
            message = message.decode()

            #If you want to limit the req/sec, uncomment this block of code
            #It's not perfect but it keeps the server up for a lot longer than normal during attack
            # print(totRequests/getTimeElapsed(startTime))
            # while totRequests/getTimeElapsed(startTime) > allowedReqPerSec:
            #     time.sleep(1)
            # totRequests+=1
            
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
            
        except OSError:
            print("Too many connections, I'm struggling...")

        except IOError:
            #e = sys.exc_info()[0]
            #print('in except '+str(e))

            # Send 404 message
            try:
                connectionSocket.send('HTTP/1.1 404 Not Found\r\n\r\n'.encode())
            except BrokenPipeError:
                print('broken pipe on the 404')
                pass

#This loop will continue to make threads as clients connect
while True:
    # Establish connection
    connectionSocket, addr = serverSocket.accept()
    
    if addr[0] not in connectionsFromIP:
        connectionsFromIP[addr[0]] = 1
    else:
        connectionsFromIP[addr[0]] +=1
    
    #If you want to cap the number of connections a single IP can make, uncomment this block and comment out the three lines below it
    # if connectionsFromIP[addr[0]] > allowedConnectionsPerIP:
    #     connectionSocket.close()
    # else:
    #     start_new_thread(singleThread, (connectionSocket, ))
    #     numThreads+=1
    #     print('Connected to: ' + addr[0] + ': On port # ' + str(addr[1]))
    
    print('Connected to: ' + addr[0] + ': On port # ' + str(addr[1]))
    start_new_thread(singleThread, (connectionSocket, ))
    numThreads+=1
    
    print('Thread Number: ' + str(numThreads))
#Close server socket
serverSocket.close()
