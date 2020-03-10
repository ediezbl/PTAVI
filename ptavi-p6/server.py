#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""Clase (y programa principal) para un servidor de eco en UDP simple."""


import socketserver
import sys
import os


class EchoHandler(socketserver.DatagramRequestHandler):
    """Invite server class."""

    def handle(self):
        """handle method of the server class."""
        line = self.rfile.read()
        message = line.decode("utf-8")
        method = message.split(" ")[0]
        message_list = message.split(" ")
        if not message_list[1].startswith("sip:"):
            respuesta = b"SIP/2.0 400 Bad Request\r\n\r\n"
            self.wfile.write(respuesta)
        elif not message_list[2].startswith("SIP/2.0"):
            respuesta = b"SIP/2.0 400 Bad Request\r\n\r\n"
            self.wfile.write(respuesta)
        else:
            if method == "INVITE":
                respuesta = b"SIP/2.0 100 Trying\r\n\r\n"
                respuesta += b"SIP/2.0 180 Ringing\r\n\r\n"
                respuesta += b"SIP/2.0 200 OK\r\n\r\n"
                self.wfile.write(respuesta)
            elif method == "BYE":
                respuesta = b"SIP/2.0 200 OK\r\n\r\n"
                self.wfile.write(respuesta)
            elif method not in ['INVITE', 'BYE', 'ACK']:
                respuesta = b"SIP/2.0 405 Method Not Allowed\r\n\r\n"
                self.wfile.write(respuesta)
            elif method == "ACK":
                aEjecutar = './mp32rtp -i 127.0.0.1 -p 23032 < ' + audio_file
                print("Vamos a ejecutar ", aEjecutar)
                os.system(aEjecutar)


if __name__ == "__main__":

    try:
        ip = sys.argv[1]
        port = int(sys.argv[2])
        audio_file = sys.argv[3]
    except (ValueError, IndexError, FileNotFoundError):
        sys.exit("Usage server.py ip port audio_file ")
    serv = socketserver.UDPServer((ip, port), EchoHandler)
    print("Listening...")
    try:
        serv.serve_forever()
    except KeyboardInterrupt:
        print("Finalizado servidor")
