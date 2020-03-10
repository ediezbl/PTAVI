#!/usr/bin/python3
"""
Clase (y programa principal) para un servidor de eco en UDP simple
"""

import socketserver
import sys

class SIPRegisterHandler(socketserver.DatagramRequestHandler):
    dicc = {}
    """
    Echo server class
    """

    def handle(self):
        """
        handle method of the server class
        (all requests will be handled by this method)
        """
        respuesta = b"SIP2.0/200 OK\r\n\r\n"
        for line in self.rfile:
            print(line.decode('utf-8'))
            try:
                output = line.decode('utf-8').split(" ")[1]
                username = output.split("sip:")[1]
                self.wfile.write(respuesta)
            except IndexError:
                continue
            self.dicc[username] = self.client_address[0]
        print(self.dicc)
if __name__ == "__main__":
    # Listens at localhost ('') port 6001
    # and calls the EchoHandler class to manage the request
    port = int(sys.argv[1])
    serv = socketserver.UDPServer(('', port), SIPRegisterHandler)

    print("Lanzando servidor UDP de eco...")
    try:
        serv.serve_forever()
    except KeyboardInterrupt:
        print("Finalizado servidor")
