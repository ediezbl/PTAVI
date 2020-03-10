#!/usr/bin/python3
import sys
import calcoohija
import csv
entrada = sys.argv[1]
with open(entrada) as fichero:
    for linea in fichero.readlines():
        lista = linea[:-1].split(",")
        operacion = lista[0]
        operadores = lista[1:]
        resultado = float(operadores[0])
        calcuPlus = calcoohija.CalculadoraHija()
        for operando in operadores[1:]:
            resultado = calcuPlus.operar(operacion, resultado, float(operando))
        print(resultado)
