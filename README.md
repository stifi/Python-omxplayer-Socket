Python-omxplayer-Socket
=======================

Socket Interface for omxplayer using Python.

    address = ('', 23000)
    omxSock = socket.socket( socket.AF_INET, socket.SOCK_DGRAM )
    omxSock.connect(address)
    omxSock.send('play /path/to/movie/movie.mkv')
    omxSock.send('forward_bit')
    status = omxSock.send('status')
    omxSock.send('stop')
    omxSock.close()
