'''
              expires = int(parameters[3].split("\r\n")[0])
              port = int(parameters[1].split(":")[2])
              user_list = [server, expires, port]
              self.user_dicc[user_sip] = user_list
              print(self.user_dicc)
              try:
                  if expires == 0:
                      del self.user_dicc[user_sip]
              except KeyError:
                  pass
              respuesta = "SIP/2.0 200 OK\r\n\r\n"
              self.wfile.write(bytes(respuesta,'utf-8'))
              write_log(message, received, server, str(port))
              write_log(respuesta, sent_to, server, str(port))
          '''
      '''
      if method == "REGISTER":
          expires = int(parameters[3].split("\r\n")[0])
          port = int(parameters[1].split(":")[2])
          user_list = [server, expires, port]
          self.user_dicc[user_sip] = user_list
          print(self.user_dicc)
          try:
              if expires == 0:
                  del self.user_dicc[user_sip]
          except KeyError:
              pass
          respuesta = "SIP/2.0 200 OK\r\n\r\n"
          self.wfile.write(bytes(respuesta,'utf-8'))
          write_log(message, received, server, str(port))
          write_log(respuesta, sent_to, server, str(port))
      '''
try:
    if expires == 0:
        del self.user_dicc[user_sip]
except KeyError:
    pass
