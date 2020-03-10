#!/usr/bin/python3

"""User Agent Client."""

import socket
import sys
from xml.sax import make_parser
from xml.sax.handler import ContentHandler
import os
import time
import hashlib


def write_log(sent, str, ip, port):
    """Escribe en el fichero de log."""
    sent = sent.replace("\r\n", " ")
    tiempo = time.time()
    current_time = time.strftime('%Y%m%d%H%M%S', time.localtime(tiempo))
    sent = current_time + " " + str + ip + ":" + port + " " + sent + "\r\n"
    with open(log, 'a') as log_file:
        log_file.write(sent)


class XMLHandler(ContentHandler):
    """Manejador de useragent."""

    def __init__(self):
        """Inicializador."""
        self.config = {}
        self.elementDicc = {
            "account": ["username", "passwd"],
            "uaserver": ["ip", "puerto"],
            "rtpaudio": ["puerto"],
            "regproxy": ["ip", "puerto"],
            "log": ["path"],
            "audio": ["path"]
        }

    def startElement(self, name, att):
        """Start Element."""
        if name != "config":
            for atr in self.elementDicc[name]:
                self.config[atr + "_" + name] = att.get(atr, "")

    def get_tags(self):
        """Devuelve un diccionario de etiquetas."""
        return self.config


# Socket
if __name__ == '__main__':

    # Variables de ejecucion
    config = sys.argv[1]
    method = sys.argv[2]
    opcion = sys.argv[3]

    # Parser
    parser = make_parser()
    cHandler = XMLHandler()
    parser.setContentHandler(cHandler)
    parser.parse(open(config))
    config = cHandler.get_tags()
    print(config)

    # Variables necesarias para el cliente
    server = config["ip_regproxy"]
    port = int(config["puerto_regproxy"])
    sip_address = config["username_account"]
    rtp_port = config["puerto_rtpaudio"]
    invite_address = config["username_account"].split(":")[0]
    audio_file = config["path_audio"]
    log = config["path_log"]
    passwd = config["passwd_account"]
    send = 'sent to ' + server + ":" + str(port) + " "
    tiempo = time.time()
    current_time = time.strftime('%Y%m%d%H%M%S', time.localtime(tiempo))
    # sdp
    content_type = "Content-Type: application/sdp" + "\r\n\r\n"
    v = "v=0\r\n"
    o = "o=" + invite_address + " " + server + "\r\n"
    s = "s=misesion\r\n"
    t = "t=0\r\n"
    m = "m=audio" + " " + rtp_port + " " + "RTP" + "\r\n"
    sdp = v + o + s + t + m
    sent_to = "Sent to" + " "
    received = "Received from" + " "
    # Mandando el mensaje al proxy
    if method == "REGISTER":
        message = method + " sip:" + sip_address + " SIP/2.0\r\n"
        try:
            int(opcion)
        except ValueError:
            sys.exit("Usage uaclient.py config method opcion")
        expires = "Expires: " + opcion + "\r\n\r\n"
        message += expires
        write_log(message, sent_to, server, str(port))
    elif method == "INVITE":
        message = method + " sip:" + opcion + " SIP/2.0\r\n" + content_type
        message += sdp
        write_log(message, sent_to, server, str(port))
    elif method == "BYE":
        message = method + " sip:" + opcion + " SIP/2.0\r\n\r\n"
        status = message.replace("\r\n", " ")
        write_log(message, sent_to, server, str(port))

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as my_socket:
        my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        my_socket.connect((server, port))
        my_socket.send(bytes(message, 'utf-8'))
        data = my_socket.recv(1024)
        received_data = data.decode('utf-8')
        write_log(received_data, received, server, str(port))
        respuesta1 = "SIP/2.0 100 Trying\r\n\r\n"
        if method == "INVITE":
            if data.decode('utf-8').startswith(respuesta1):
                sent_to = "sent to" + " "
                ack = "ACK" + " sip:" + opcion + " SIP/2.0\r\n\r\n"
                my_socket.send(bytes(ack, 'utf-8'))
                data_list = data.decode("utf-8").split("\r\n")
                audio = data_list[11].split(" ")
                rtp_port = audio[1]
                aEjecutar = './mp32rtp -i' + " " + server + " " + '-p '
                aEjecutar += " " + rtp_port + '< ' + audio_file
                print("Vamos a ejecutar ", aEjecutar)
                os.system(aEjecutar)
                write_log(ack, sent_to, server, str(port))
                write_log(aEjecutar, sent_to, server, str(port))
        elif method == "REGISTER":
            respuesta2 = "SIP/2.0 401 Uauthorized\r\n"
            sent_to = "sent_to" + " "
            if data.decode('utf-8').startswith(respuesta2):
                received_data = data.decode('utf-8')
                list_data = received_data.split("\r\n")
                number = list_data[1].split("=")[1].split("\"")[1]
                print(number)
                hash = hashlib.md5()
                hash.update(bytes(number, 'utf-8'))
                hash.update(bytes(passwd, 'utf-8'))
                hash.digest()
                diggest = hash.hexdigest()
                message = method + " sip:" + sip_address + " SIP/2.0\r\n"
                try:
                    int(opcion)
                except ValueError:
                    sys.exit("Usage uaclient.py config method opcion")
                expires = "Expires: " + opcion + "\r\n"
                message += expires
                message += "Authorization: Digest response="
                message += diggest + "\r\n\r\n"
                my_socket.send(bytes(message, 'utf-8'))

        print(data.decode('utf-8'))
        print("Terminando socket...")
        print("Fin.")
