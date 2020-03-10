#!/usr/bin/python3

"""Proxy Registrar."""

import socketserver
import sys
import socket
import random
from xml.sax import make_parser
from xml.sax.handler import ContentHandler
import time
import json
import hashlib
import os.path as path


def write_log(sent, str, ip, port):
    """Escribe en el ficher de log."""
    sent = sent.replace("\r\n", " ")
    tiempo = time.time()
    current_time = time.strftime('%Y%m%d%H%M%S', time.localtime(tiempo))
    sent = current_time + " " + str + ip + ":" + port + " " + sent + "\r\n"
    with open(log, 'a') as log_file:
        log_file.write(sent)


def Starting_Finishing(string):
    """Escribe en el fichero de log al inicio y final."""
    tiempo = time.time()
    current_time = time.strftime('%Y%m%d%H%M%S', time.localtime(tiempo))
    str = current_time + " " + string + "\r\n"
    with open(log, 'a') as log_file:
        log_file.write(str)


class XMLHandler(ContentHandler):
    """Manejador del proxy."""

    def __init__(self):
        """Inicializador."""
        self.config = {}
        self.elementDicc = {
            "server": ["name", "ip", "puerto"],
            "database": ["path", "passwdpath"],
            "log": ["path"]
        }

    def startElement(self, name, att):
        """Start Element."""
        if name != "config":
            for atr in self.elementDicc[name]:
                self.config[atr + "_" + name] = att.get(atr, "")

    def get_tags(self):
        """Devuelve un diccionario con las etiquetas."""
        return self.config


# Variables de ejecucion
config = sys.argv[1]

# Parser
parser = make_parser()
cHandler = XMLHandler()
parser.setContentHandler(cHandler)
parser.parse(open(config))
config = cHandler.get_tags()
print(config)

# Variables necesarias para el proxy
server = config["ip_server"]
port = int(config["puerto_server"])
log = config["path_log"]
passwd = config["passwdpath_database"]
file_json = config["path_database"]


class SIPHandler(socketserver.DatagramRequestHandler):
    """Manejador del proxy."""

    user_dicc = {}
    passwd_dicc = {}
    dicc_number = {}

    def register2json(self, file):
        """Escribe en el fichero de json."""
        with open(file, 'w') as outfile:
            json.dump(self.user_dicc, outfile, indent=1)

    def json2register(self, file):
        """Comprueba si existe fichero json."""
        try:
            if path.exists(file):
                with open(file, "r") as data_file:
                    self.user_dicc = json.load(data_file)
        except Exception:
            pass

    def read_json(self, file):
        """Lee el fichero de las contraseñas."""
        try:
            with open(file, 'r') as data_file:
                self.passwd_dicc = json.load(data_file)
        except FileNotFoundError:
            pass

    def clean_dicc(self):
        """Comprueba la fecha de expires."""
        user_list = []
        format = "%Y-%m-%d %H:%M:%S"
        Now = time.strftime(format, time.localtime())
        for user in self.user_dicc:
            if self.user_dicc[user][1] < Now:
                user_list.append(user)
        for user in user_list:
            del self.user_dicc[user]

    def handle(self):
        """Manejador."""
        self.json2register(file_json)
        line = self.rfile.read()
        message = line.decode('utf-8')
        print(message)
        parameters = message.split(" ")
        print(parameters)
        method = parameters[0]
        method_list = ["REGISTER", "INVITE", "BYE", "ACK"]
        user_sip = parameters[1].split(":")[1]
        sent_to = "Sent to" + " "
        if not parameters[1].startswith("sip:"):
            respuesta = "SIP/2.0 400 Bad Request\r\n\r\n"
            self.wfile.write(bytes(respuesta, 'utf-8'))
            write_log(respuesta, sent_to, server, str(port))
        elif not parameters[2].startswith("SIP/2.0"):
            respuesta = "SIP/2.0 400 Bad Request\r\n\r\n"
            self.wfile.write(bytes(respuesta, 'utf-8'))
            write_log(respuesta, sent_to, server, str(port))
        elif method not in method_list:
            respuesta = "SIP/2.0 405 Method Not Allowed\r\n\r\n"
            self.wfile.write(bytes(respuesta, 'utf-8'))
            write_log(respuesta, sent_to, server, str(port))
        else:
            sent_to = "Sent to" + " "
            received = "Received from" + " "
            port = int(config["puerto_server"])
            print(parameters)
            if method == "REGISTER":
                expires = int(parameters[3].split("\r\n")[0])
                if expires == 0:
                    try:
                        del self.user_dicc[user_sip]
                    except KeyError:
                        pass
                    self.register2json(file_json)
                    respuesta = "SIP/2.0 200 OK\r\n\r\n"
                    self.wfile.write(bytes(respuesta, 'utf-8'))
                    write_log(message, received, server, str(port))
                    write_log(respuesta, sent_to, server, str(port))
                elif user_sip in self.user_dicc:
                    respuesta = "SIP/2.0 200 OK\r\n\r\n"
                    self.wfile.write(bytes(respuesta, 'utf-8'))
                    write_log(message, received, server, str(port))
                    write_log(respuesta, sent_to, server, str(port))
                else:
                    if len(parameters) == 4:
                        number = str(random.randint(00000, 10000))
                        self.dicc_number[user_sip] = number
                        respuesta = "SIP/2.0 401 Uauthorized\r\n"
                        respuesta += "WWW-Authenticate: Digest nonce=\""
                        respuesta += self.dicc_number[user_sip] + "\"\r\n\r\n"
                        self.wfile.write(bytes(respuesta, 'utf-8'))
                        write_log(respuesta, sent_to, server, str(port))
                    else:
                        if parameters[4] == "Digest":
                            list_response = parameters[5].split("=")
                            diggest_respons = list_response[1].split("\r\n")[0]
                            print(diggest_respons)
                            f = "%Y-%m-%d %H:%M:%S"  # Format
                            expires = int(parameters[3].split("\r\n")[0])
                            tiempo = time.time() + expires
                            exp_time = time.strftime(f, time.localtime(tiempo))
                            port = int(parameters[1].split(":")[2])
                            self.read_json(passwd)
                            password = self.passwd_dicc[user_sip]
                            hash = hashlib.md5()
                            num = self.dicc_number[user_sip]
                            hash.update(bytes(num, 'utf-8'))
                            hash.update(bytes(password, 'utf-8'))
                            hash.digest()
                            diggest = hash.hexdigest()
                            print(diggest)
                            print(self.dicc_number[user_sip])
                            if diggest == diggest_respons:
                                user_list = [server, exp_time, port]
                                self.user_dicc[user_sip] = user_list
                                self.clean_dicc()
                                print(self.user_dicc)
                                self.register2json(file_json)
                                resp = "SIP/2.0 200 OK\r\n\r\n"  # Respuesta
                                self.wfile.write(bytes(resp, 'utf-8'))
                                write_log(message, received, server, str(port))
                                write_log(resp, sent_to, server, str(port))

            if method == "INVITE" or method == "ACK" or method == "BYE":
                if user_sip not in self.user_dicc:
                    respuesta = "SIP/2.0 404 User Not Found\r\n\r\n"
                    self.wfile.write(bytes(respuesta, 'utf-8'))
                    write_log(message, received, server, str(port))
                    write_log(respuesta, sent_to, server, str(port))
                else:
                    port = self.user_dicc[user_sip][2]
                    with socket.socket(socket.AF_INET,
                                       socket.SOCK_DGRAM) as my_socket:
                        my_socket.setsockopt(socket.SOL_SOCKET,
                                             socket.SO_REUSEADDR, 1)
                        my_socket.connect((server, port))
                        my_socket.send(line)
                        data = my_socket.recv(1024)
                        respuesta1 = b"SIP/2.0 400 Bad Request\r\n\r\n"
                        respuesta2 = b"SIP/2.0 405 Method Not Allowed\r\n\r\n"
                        if data != respuesta1 or data != respuesta2:
                            self.wfile.write(data)


if __name__ == '__main__':

    serv = socketserver.UDPServer((server, port), SIPHandler)
    print("Lanzando servidor UDP proxy ...")
    status = "Starting ... \r\n"
    Starting_Finishing(status)
    try:
        serv.serve_forever()
    except KeyboardInterrupt:
        status = "Finishing ...\r\n"
        Starting_Finishing(status)
        print("Finalizando servidor")
