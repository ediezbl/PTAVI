#!/usr/bin/python3

"""User Agent Server."""

import socketserver
import sys
from xml.sax import make_parser
from uaclient import XMLHandler
import os
import time

# Variables de ejecucion del programa
config = sys.argv[1]

# Parser
parser = make_parser()
cHandler = XMLHandler()
parser.setContentHandler(cHandler)
parser.parse(open(config))
config = cHandler.get_tags()
print(config)

# Variables que van a formar parte del programa
serve = config['ip_uaserver']
port = int(config['puerto_uaserver'])
invite_adress = config["username_account"].split(":")[0]
rtp_port = config["puerto_rtpaudio"]
audio_file = config["path_audio"]
log = config["path_log"]

# sdp
content_type = "Content-Type: application/sdp" + "\r\n\r\n"
v = "v=0\r\n"
o = "o=" + invite_adress + " " + serve + "\r\n"
s = "s=misesion\r\n"
t = "t=0\r\n"
m = "m=audio" + " " + rtp_port + " " + "RTP" + "\r\n\r\n"
sdp = v + o + s + t + m


def write_log(sent, str, ip, port):
    """Escribe en el fichero de log."""
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


class SIPServerHandler(socketserver.DatagramRequestHandler):
    """Manejador del user agent server."""

    def handle(self):
        """Manejador."""
        line = self.rfile.read()
        message = line.decode('utf-8')
        received = "Received from"
        parameters = message.split(" ")
        print(parameters)
        method = parameters[0]
        method_list = ["REGISTER", "INVITE", "ACK", "BYE"]
        user_sip = parameters[1].split(":")[1]
        if not parameters[1].startswith("sip:"):
            respuesta = "SIP/2.0 400 Bad Request\r\n\r\n"
            self.wfile.write(bytes(respuesta, 'utf-8'))
            sent_to = "Send to" + " "
            write_log(respuesta, sent_to, serve, str(port))
        elif not parameters[2].startswith("SIP/2.0"):
            respuesta = "SIP/2.0 400 Bad Request\r\n\r\n"
            self.wfile.write(bytes(respuesta, 'utf-8'))
            sent_to = "Send to" + " "
            write_log(respuesta, sent_to, serve, str(port))
        elif method not in method_list:
            respuesta = "SIP/2.0 405 Method Not Allowed\r\n\r\n"
            self.wfile.write(bytes(respuesta, utf-8))
            sent_to = "Send to" + " "
            write_log(respuesta, sent_to, serve, str(port))
        else:
            sent_to = "Sent to" + " "
            received = "Received from" + " "
            if method == "INVITE":
                respuesta = "SIP/2.0 100 Trying\r\n\r\n"
                respuesta += "SIP/2.0 180 Ringing\r\n\r\n"
                respuesta += "SIP/2.0 200 OK\r\n" + content_type + sdp
                self.wfile.write(bytes(respuesta, 'utf-8'))
                write_log(message, received, serve, str(port))
                write_log(respuesta, sent_to, serve, str(port))
            elif method == "BYE":
                respuesta = "SIP/2.0 200 OK\r\n\r\n"
                self.wfile.write(bytes(respuesta, 'utf-8'))
                write_log(message, received, serve, str(port))
                write_log(respuesta, sent_to, serve, str(port))
            elif method == "ACK":
                aEjecutar = './mp32rtp -i' + " " + serve + '-p'
                aEjecutar += " " + rtp_port + '< ' + audio_file
                print("Vamos a ejecutar ", aEjecutar)
                os.system(aEjecutar)
                write_log(aEjecutar, sent_to, serve, str(port))


if __name__ == '__main__':
    serv = socketserver.UDPServer((serve, port), SIPServerHandler)
    print("Listening...")
    status = "Starting ..."
    Starting_Finishing(status)
    try:
        serv.serve_forever()
    except KeyboardInterrupt:
        status = "Finishing ..."
        Starting_Finishing(status)
        print("Finalizando servidor")
