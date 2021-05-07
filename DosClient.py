from socket import *
from _thread import *
import resource
import time

NETWORK_UNREACHABLE = 51

#allows us to dictate the number of threads we want to start
numThreads = 0

#allows us to start more threads above what would be the normal limit for your system: basically it lets us do as much as your computer can handle
resource.setrlimit(resource.RLIMIT_NOFILE, (resource.RLIM_INFINITY,resource.RLIM_INFINITY))
print(resource.RLIM_INFINITY)

#simulates a single client
def singleThread():
    try:
       # print('in single thread')
        clientSocket = socket(AF_INET, SOCK_STREAM)
            
        #Asks for the port and the server
        serverName = '192.168.88.14'
        serverPort = 12000
            
        #Establishes socket
        clientSocket.connect((serverName, serverPort))
            
        #Asks for the filename that is being requested
        req = 'test_data4.txt'
            
        while True:
            #Sends the request
            
            clientSocket.send('GET '.encode() +req.encode() +'\r\n\r\n'.encode())
            
#            message = clientSocket.recv(1000)
#            #print(message)
#            while message:
#                #print(message.decode())
#                message = clientSocket.recv(1000)
        
        
    #these exceptions may happen if there are too many concurrent threads/there is a connection issue
    
    
    except ConnectionResetError:
        print('Connection reset by host')
        pass
#    except OSError as e:
#        if e.errorno == NETWORK_UNREACHABLE:
#            print('Congrats, the network cannot be reached')
    except BrokenPipeError:
        print('Broken pipe: you may be starting too many threads too quickly. Increase the delay between threads')
        pass

while numThreads < 20000:
    #print(str(numThreads))
    #starts a new single thread and then sleeps an appropriate ammt of time
    start_new_thread(singleThread, ())
    #time.sleep()
    numThreads+=1
