#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""Clase (y programa principal) para un cliente invite en UDP simple."""

import socket
import sys
method = sys.argv[1]
try:
    if method == "INVITE" or method == "BYE":
        user = sys.argv[2]
        list = user.split(":")
        user_sip = list[0]
        server = user_sip.split("@")[1]
        port = int(list[1])
    else:
        sys.exit("Usage: client.py method receiver@IP:SIPport")
except (IndexError, ValueError):
    sys.exit("Usage: client.py method receiver@IP:SIPport")
# Creamos el socket, lo configuramos y lo atamos a un servidor/puerto
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as my_socket:
    my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    my_socket.connect((server, port))
    message = method + " sip:" + user_sip + " SIP/2.0\r\n\r\n"
    print("Enviando: " + message)
    my_socket.send(bytes(message, 'utf-8'))
    data = my_socket.recv(1024)
    respuesta1 = "SIP/2.0 100 Trying\r\n\r\n"
    respuesta2 = "SIP/2.0 180 Ringing\r\n\r\n"
    respuesta3 = "SIP/2.0 200 OK\r\n\r\n"
    if method == "INVITE":
        if data.decode("utf-8") == respuesta1 + respuesta2 + respuesta3:
            ack = 'ACK' + " sip:" + user_sip + " SIP/2.0\r\n\r\n"
            my_socket.send(bytes(ack, 'utf-8'))
    print(data.decode('utf-8'))
    print("Terminando socket...")

print("Fin.")
