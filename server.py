#The MIT License (MIT)

#Copyright (c) 2014 Boudjada Messaoud

#Permission is hereby granted, free of charge, to any person obtaining a copy
#of this software and associated documentation files (the "Software"), to deal
#in the Software without restriction, including without limitation the rights
#to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#copies of the Software, and to permit persons to whom the Software is
#furnished to do so, subject to the following conditions:

#The above copyright notice and this permission notice shall be included in all
#copies or substantial portions of the Software.

#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#SOFTWARE.
import socket
import select
class ChatServer:
    def __init__( self, port ):
        self.port = port;
        self.srvsock = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
        self.srvsock.setsockopt( socket.SOL_SOCKET, socket.SO_REUSEADDR, 1 )
        self.srvsock.bind( ("", port) )
        self.srvsock.listen( 5 )
        self.names=[]
        self.password=[]
        self.descriptors = [self.srvsock]
        print 'ChatServer started on port %s' % port
    def run( self ):
        while 1:
            # Await an event on a readable socket descriptor
            (sread, swrite, sexc) = select.select( self.descriptors, [], [] )
            # Iterate through the tagged read descriptors
            for sock in sread:
                # Received a connect to the server (listening) socket
                if sock == self.srvsock:
                    self.accept_new_connection()
                else:
                    # Received something on a client socket
                    str = sock.recv(1050)
                    # Check to see if the peer socket closed
                    if str == '':
                        host,port = sock.getpeername()
                        str = 'Client left %s:%s\r\n' % (host, port)
                        #self.broadcast_string( str, sock )
                        sock.close()
                        self.descriptors.remove(sock)
                    else:
                        
                        host,port = sock.getpeername()
                        newstr = '[%s:%s] %s' % (host, port, str)
                        self.broadcast_string( str, sock )
                        
    def broadcast_string( self, str, omit_sock ):
        for sock in self.descriptors:
            if sock != self.srvsock:# and sock != omit_sock:
                host,port = sock.getpeername()
                if host in str:
                    host1,port1 = omit_sock.getpeername()
                    n=len(host)
                    str=host1+": "+str[n:]
                    sock.send(str)
                    print str+"\n"
                    
                    
        
    def accept_new_connection( self ):
        newsock, (remhost, remport) = self.srvsock.accept()
       
        self.descriptors.append( newsock )
        str = 'Client joined %s:%s \r\n' % (remhost, remport)
        print str
       
myServer = ChatServer( 2626 )
myServer.run()
        
