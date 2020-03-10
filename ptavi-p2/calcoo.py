#!/usr/bin/python3


import sys


class Calculadora():

    def suma(self, operando1, operando2):

        return operando1 + operando2

    def resta(self, operando1, operando2):

        return operando1 - operando2

    def operar(self, operador, operando1, operando2):
        if operador == "suma":
            return self.suma(operando1, operando2)
        elif operador == "resta":
            return self.resta(operando1, operando2)


if __name__ == '__main__':

    calcu = Calculadora()
    operador = sys.argv[2]
    try:
        operando1 = float(sys.argv[1])
        operando2 = float(sys.argv[3])
    except ValueError:
        sys.exit("Error: Enteros o decimales ")
    if len(sys.argv) != 4:
        sys.exit("Ussage: calcoo.py operando1 operacion operando2")
    else:
        print(calcu.operar(operador, operando1, operando2))
