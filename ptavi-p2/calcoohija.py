#!/usr/bin/python3

import sys
import calcoo


class CalculadoraHija(calcoo.Calculadora):

    def multiplicacion(self, operando1, operando2):
        return operando1 * operando2

    def division(self, operando1, operando2):
        try:
            return operando1 / operando2
        except ZeroDivisionError:
            return("No se puede dividir entre cero")

    def operar(self, operador, operando1, operando2):
        if operador == "mul":
            return self.multiplicacion(operando1, operando2)
        elif operador == "div":
            return self.division(operando1, operando2)
        else:
            return calcoo.Calculadora.operar(self, operador, operando1, operando2)


if __name__ == '__main__':

    calcuHija = CalculadoraHija()
    operador = sys.argv[2]
    try:
        operando1 = float(sys.argv[1])
        operando2 = float(sys.argv[3])
    except ValueError:
        sys.exit("Error, los parametros introducidos no son enteros")
    if len(sys.argv) != 4:
        sys.exit("Ussage: calcoohija.py operando1 operacion operando2")
    else:
        print(calcuHija.operar(operador, operando1, operando2))
