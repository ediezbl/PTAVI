#!/usr/bin/python3
# -*- coding: utf-8 -*-
from xml.sax import make_parser
from xml.sax.handler import ContentHandler
from smallsmilhandler import SmallSMILLHandler
from urllib.request import urlretrieve
import sys
import json

class KaraokeLocal():
    def __init__(self, filename):
        parser = make_parser()
        SmallSmill = SmallSMILLHandler()
        parser.setContentHandler(SmallSmill)
        parser.parse(open(filename))
        self.lista = SmallSmill.get_tags()

    def __str__(self):
        output = ""
        for elementDicc in self.lista:
            output +=  elementDicc['etiqueta'] + '\t'
            for atributo in elementDicc:
                if atributo != "etiqueta" and  elementDicc[atributo]:
                    output += atributo + "=" + elementDicc[atributo]  + "\t"
            output = output[:-1] + '\n'
        return output

    def to_json(self, filejson):
        if filejson.endswith(".smil"):
            filejson = filejson.replace(".smil",".json")

        with open(filejson, "w") as outfile:
            json.dump(self.lista, outfile, indent=1)

    def dolocal(self):
        for elemento in self.lista:
            for atributo in elemento:
                if atributo != "etiqueta":
                    if elemento[atributo].startswith("http://"):
                        url = elemento[atributo]
                        Download = url.split("/")[-1]
                        urlretrieve(url,Download)
                        print("Descargando... " + elemento[atributo])
                        elemento[atributo] = elemento[atributo].split("/")[-1]

if __name__ == '__main__':

    if len(sys.argv) != 2:
        sys.exit("ussage karaoke.py karaoke.smill")
    else:
        try:
            filename = sys.argv[1]
            filejson = "local.json"
            Karaoke = KaraokeLocal(filename)
            print(Karaoke)
            Karaoke.to_json(filename)
            Karaoke.dolocal()
            Karaoke.to_json(filejson)
            print(Karaoke)
        except FileNotFoundError:
            print("File has to exist")
        except IndexError:
            print("Ussage karaoke.py file.smil")
