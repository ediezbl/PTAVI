#!/usr/bin/python3
# -*- coding: utf-8 -*-

from xml.sax import make_parser
from xml.sax.handler import ContentHandler


class SmallSMILLHandler(ContentHandler):

    def __init__(self):
        self.lista = []
        self.elementDicc = {
            "root-layout": ["width", "height", "background-color"],
            "region": ["id", "top", "bottom", "left", "right"],
            "img": ["src", "begin", "dur"],
            "audio": ["src", "begin", "dur"],
            "textstream": ["src", "region"]
        }

    def startElement(self, name, attrs):
        if name in self.elementDicc:
            dicc = {}
            dicc["etiqueta"] = name
            for atributo in self.elementDicc[name]:
                dicc[atributo] = attrs.get(atributo, "")
            self.lista.append(dicc)

    def get_tags(self):
        return self.lista


if __name__ == '__main__':

    parser = make_parser()
    SmallSmill = SmallSMILLHandler()
    parser.setContentHandler(SmallSmill)
    parser.parse(open('karaoke.smil'))
    lista = SmallSmill.get_tags()
    print(lista)
