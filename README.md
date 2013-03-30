Python-omxplayer-Socket
=======================

Socket Interface for omxplayer using Python.

Example Client usage:

    address = ('', 23000)
    omxSocket = socket.socket( socket.AF_INET, socket.SOCK_DGRAM )
    omxSocket.connect(address)
    omxSocket.send('play /path/to/movie/movie.mkv')
    omxSocket.send('forward_bit')
    omxSocket.send('status')
    playing = omxSocket.recv(1024)
    if playing == 'True':
       omxSocket.send('stop')
    omxSocket.close()
