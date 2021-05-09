# LOIC
DOS Simulation

These programs are designed to simulate a Denial of Service attack over HTTP. The DosServer is a basic HTTP sever (supporting GET requests only), and DosClient is the actual attacker. 

The server runs as

    python3 DosServer.py < Port Number >

And the client runs as 

    python3 DosClient.py < IP > < Port > < Number of Connections >


The test_data is the file which the client requests, although this can be replaced with any file.