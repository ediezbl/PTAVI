#!/usr/bin/python3
import sys
import calcoohija
entrada = sys.argv[1]
fichero = open(entrada)
for linea in fichero.readlines():
    lista = linea[:-1].split(",")
    operacion = lista[0]
    operadores = lista[1:]
    resultado = float(operadores[0])
    calcuPlus = calcoohija.CalculadoraHija()
    for operando in operadores[1:]:
        resultado = calcuPlus.operar(operacion, resultado, float(operando))
    print(resultado)
fichero.close()
