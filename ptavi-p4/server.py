#!/usr/bin/python3

"""Clase (y programa principal) para un servidor de eco en UDP simple."""


import socketserver
import sys
import time
import json
import os.path as path


class SIPRegisterHandler(socketserver.DatagramRequestHandler):
    """Register server class."""

    user_dicc = {}  # diccionario que lleva el control de usuarios

    def clean_dicc(self):
        """Check expires and delete the dictionary."""
        user_list = []
        format = "%Y-%m-%d %H:%M:%S"
        Now = time.strftime(format, time.localtime())
        for user in self.user_dicc:
            if self.user_dicc[user][1] < Now:
                user_list.append(user)
        for user in user_list:
            del self.user_dicc[user]

    def handle(self):
        """handle method of the server class."""
        line = self.rfile.read()
        mensaje = line.decode('utf8')
        print(mensaje[0:8])
        if mensaje[0:8] == "REGISTER":
            format = "%Y-%m-%d %H:%M:%S"
            expires = int(mensaje.split(" ")[3])
            tiempo = time.time() + expires
            expires_time = time.strftime(format, time.localtime(tiempo))
            output = mensaje.split(" ")[1]
            ip = self.client_address[0]
            username = output.split("sip:")[1]
            user_list = [ip, expires_time]
            self.json2register()
            self.user_dicc[username] = user_list
            self.clean_dicc()
            try:
                if expires == 0:
                    del self.user_dicc[username]
            except KeyError:
                pass
            print(self.user_dicc)
            respuesta = b"SIP/2.0 200 OK\r\n\r\n"
            self.wfile.write(respuesta)
        else:
            respuesta = b"SIP2.0/ 400 BAD REQUEST\r\n\r\n"
            self.wfile.write(respuesta)
        self.register2json()

    def register2json(self):
        """register users in json file."""
        with open("registered.json", "w") as outfile:
            json.dump(self.user_dicc, outfile, indent=1)

    def json2register(self):
        """check if registered.json exists."""
        try:
            if path.exists("registered.json"):
                with open("registered.json", "r") as data_file:
                    self.user_dicc[username] = json.load(data_file)
        except Exception:
            pass


if __name__ == "__main__":
    # Listens at localhost ('') port 6001
    # and calls the EchoHandler class to manage the request

    try:
        if len(sys.argv) > 3:
            sys.exit("Ussage: server.py ip port")
        else:
            ip = sys.argv[1]
            port = int(sys.argv[2])
    except IndexError:
        sys.exit("Ussage: server.py port")

    serv = socketserver.UDPServer((ip, port), SIPRegisterHandler)
    print("Lanzando servidor UDP de register...")
    try:
        serv.serve_forever()
    except KeyboardInterrupt:
        print("Finalizado servidor")
