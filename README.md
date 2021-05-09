# LOIC
DOS Simulation

These programs are designed to simulate a Denial of Service attack over HTTP. The DosServer is a basic HTTP sever (supporting GET requests only), and DosClient is the actual attacker. The test_data4.txt file is the file which the client requests, although this can be replaced with any file.

The server runs as

    python3 DosServer.py < Port Number >

And the client runs as 

    python3 DosClient.py < IP > < Port > < Number of Connections >

Use ^C to quit either program.
