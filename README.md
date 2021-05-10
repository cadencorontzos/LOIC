# LOIC
DOS Simulation

These programs are designed to simulate a Denial of Service attack over HTTP. The DosServer is a basic HTTP sever (supporting GET requests only), and DosClient is the actual attacker. The test_data4.txt and test_data5.txt are the files which the client can request, although this can be replaced with any file(ASCII characters only).

The server runs as

    python3 DosServer.py < Port Number >

And the client runs as 

    python3 DosClient.py < Server IP > < Server Port > < Number of Connections >

Use ^C to quit either program.

NOTE: On Windows, the resource module is not supported by default like on Mac and Linux. Comment out those lines in both the client and server(indicated with comments).

There are some preventative measures built into the server. There are blocks of commented code that support these; uncomment to try.
