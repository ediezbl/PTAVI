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
        try:
            parser.parse(open(filename))
        except FileNotFoundError:
            sys.exit("File has to exist")
        self.lista = SmallSmill.get_tags()

    def __str__(self):
        output = ""
        for elementDicc in self.lista:
            output += elementDicc['etiqueta'] + '\t'
            for atr in elementDicc:
                if atr != "etiqueta" and elementDicc[atr]:
                    output += atr + "=" + '"' + elementDicc[atr] + '"' + "\t"
            output = output[:-1] + '\n'
        return output

    def to_json(self, filesmil, filejson=''):
        if not filejson:
            filejson = filesmil.replace(".smil", ".json")
        with open(filejson, "w") as outfile:
            json.dump(self.lista, outfile, indent=1)

    def do_local(self):
        for elemento in self.lista:
            for atr in elemento:
                if atr != "etiqueta" and elemento[atr].startswith("http://"):
                    url = elemento[atr]
                    Download = url.split("/")[-1]
                    urlretrieve(url, Download)
                    print("Descargando... " + elemento[atr])
                    elemento[atr] = elemento[atr].split("/")[-1]


if __name__ == '__main__':

    if len(sys.argv) != 2:
        sys.exit("ussage karaoke.py file.smill")
    else:
        try:
            filename = sys.argv[1]
        except IndexError:
            sys.exit("Ussage karaoke.py file.smil")
        filejson = "local.json"
        Karaoke = KaraokeLocal(filename)
        print(Karaoke)
        Karaoke.to_json(filename)
        Karaoke.do_local()
        Karaoke.to_json(filejson)
        print(Karaoke)
