#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    This program is free software; you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation; either version 3 of the License,
    or (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
    See the GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program; if not, see <http://www.gnu.org/licenses/>.

    Client example:
        address = ('', 23000)
        omxSocket = socket.socket( socket.AF_INET, socket.SOCK_DGRAM )
        omxSocket.connect(address)
        omxSocket.send('play /path/to/movie/movie.mkv omxsound=hdmi')
        omxSocket.send('forward_bit')
        omxSocket.send('status')
        playing = omxSocket.recv(1024)
        if playing[0:4] == 'True':
           omxSocket.send('stop')
        omxSocket.close()
     
"""

__author__ = "Stefan Gansinger"
__version__ = "0.2"
__email__ = "stifi.s@freenet.de"
__credits__ = ["Robin Rawson-Tetley", "Johannes Baiter", "JugglerLKR"]



import pexpect
import select
import socket
import sys
from pipes import quote

# OMXPLAYER = "/usr/bin/omxplayer.bin"
OMXPLAYER = "/usr/bin/omxplayer"
LDPATH = "/opt/vc/lib:/usr/lib/omxplayer"

QUIT_CMD = 'q'
PAUSE_CMD = 'p'
TOGGLE_SUBS_CMD = 's'
FORWARD_BIT_CMD = "\033[C"
FORWARD_LOT_CMD = "\033[A"
REWIND_BIT_CMD = "\033[D"
REWIND_LOT_CMD = "\033[B"


class omxPlayerSocket():

    def __init__(self, address = ('', 23000)):
        self.omxSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.status = {'playing': False}
        self.playUrl = ""
        try:
            self.omxSocket.bind(address)
        except socket.error, msg:
            sys.stderr.write("[ERROR] %s.\n" % msg[1])
            sys.exit(1)

    def startSocket(self):   
        while True:
            msg = "" 
            
            # test if new object is in omxSocket, using a timeout of 10.0s --> "polling for messages"
            if select.select([self.omxSocket],[],[],10.0)[0]:
                # FIXME: maintain message length
                msg, clientAddr = self.omxSocket.recvfrom(4096) 
        
            if msg != "":
            
                if 'halt' in msg:
                    msg = ""
                    try:
                        omxProcess.send(QUIT_CMD)
                        if omxProcess.isalive():
                            omxProcess.wait()
                    except NameError:
                        # no Process created so far
                        pass
        
                    self.omxSocket.close()
                    break
               
                if 'kill' in msg:
                    try:
                        omxProcess.send(QUIT_CMD)
                        omxProcess.close(force=True)
                    except NameError:
                        # nothing to kill
                        pass
                if 'status' in msg:
                    if self.status['playing'] == True:
                        self.omxSocket.sendto(str(self.status['playing']) + self.playUrl,clientAddr)
                    else:
                        self.omxSocket.sendto(str(self.status['playing']),clientAddr)

                if 'play' in msg:
                    self.playUrl = msg[len('play '):]
                    self.playUrl = self.playUrl[0:self.playUrl.rfind("omxsound")-1]
                    sound=msg[msg.rfind("omxsound=")+9:]
                    msg = ""
                    cmd = [OMXPLAYER,"-r","-o",sound,quote(self.playUrl)]
                    
                    try:
                        omxProcess
                    except NameError:
                        # no omxProcess created so far
                        # print("play: " + self.playUrl)
                        omxProcess = pexpect.spawn(' '.join(cmd), env = {"LD_LIBRARY_PATH" : LDPATH})
                        self.status = {'playing': True}
                    else:
                        # only play if not already    
                        if not omxProcess.isalive():
                            # print("play: " + self.playUrl)
                            omxProcess = pexpect.spawn(' '.join(cmd), env = {"LD_LIBRARY_PATH" : LDPATH})
                            self.status = {'playing': True}
        
            try:
                omxProcess
            except NameError:
                # no Process created so far --> ignore all commands
                pass 
            else:
                # always ask for process status to prevent zombie process 
                if omxProcess.isalive():
                    if msg == 'pause':
                        omxProcess.send(PAUSE_CMD)
        
                    if msg == 'stop':
                        omxProcess.send(QUIT_CMD)
                        omxProcess.wait() 
                        self.status = {'playing': False}
        
                    if msg == 'forward_bit':
                        omxProcess.send(FORWARD_BIT_CMD)
        
                    if msg == 'rewind_bit':
                        omxProcess.send(REWIND_BIT_CMD)
        
                    if msg == 'forward_lot':
                        omxProcess.send(FORWARD_LOT_CMD)
        
                    if msg == 'rewind_lot':
                        omxProcess.send(REWIND_LOT_CMD)

                    if msg == 'toggle_subs':
                        omxProcess.send(TOGGLE_SUBS_CMD)
                else:
                    self.status = {'playing': False}
        
        self.omxSocket.close()


if __name__ == "__main__":
    socket = omxPlayerSocket()
    socket.startSocket()
