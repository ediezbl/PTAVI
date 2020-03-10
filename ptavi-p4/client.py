#!/usr/bin/python3

"""Programa cliente UDP que abre un socket a un servidor."""


import socket
import sys
# Constantes. Dirección IP del servidor y contenido a enviar
try:
    if len(sys.argv) > 6:
        sys.exit("Ussage client.py ip port register sip_address expires_value")
    else:
        server = sys.argv[1]
        port = int(sys.argv[2])
        register = sys.argv[3]
        sip_address = sys.argv[4]
        expires = sys.argv[5]
except IndexError:
    sys.exit("Ussage client.py ip port register sip_address expires_value")
# Creamos el socket, lo configuramos y lo atamos a un servidor/puerto
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as my_socket:
    my_socket.connect((server, port))
    expires = "Expires: " + expires + "\r\n\r\n"
    mensaje = "REGISTER sip:" + sip_address + " SIP/2.0\r\n" + expires
    print(mensaje)
    my_socket.send(bytes(mensaje, 'utf-8'))
    data = my_socket.recv(1024)
    print(data.decode('utf-8'))

print("Socket terminado.")
