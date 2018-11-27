# -*- coding: utf-8 -*-
import sys
import shlex

from prettytable import PrettyTable


#Kevin Alexander Perez Baires.  00053812
#Fabiola Maria Estrada Mayen    00015313
#Bryan Salvador Marroquin Aldana 00023314
#Jonathan Aelxis Rodriguez Cruz  00012714
#Oscar Efrain Martinez Escobar.  00038814

#Funcion que se encarga de crear la tabla de parseo, obteniendo como parametros la lista de elementos no terminales, elementos terminales, una estructura de datos
#para las producciones, first y follow que son diccionarios
def TablaParseo(listaNoTerminales, ListaTerminales, dicProducciones, dicFirst, dicFollow):
	#obteniendo tamaño de elementos terminales
	total_terminales = len(ListaTerminales)
	#obteniendo tamaño de elementos no terminales
	total_noTerminales = len(listaNoTerminales)
	
	#Creando la tabla con las dimensiones segun el tamaño de los elementos terminales y no terminales de la gramatica
	A = [[0 for i in xrange(total_terminales + 1)] for j in xrange(total_noTerminales + 1)]
	A[0][0] = 'No-Terminales'
	
	global dicGlobal1 
	dicGlobal1= {}
	global dicGlobal2
	dicGlobal2 = {}
	
	#Guardando en un diccionario la lista de elementos terminales
	for i in xrange(total_terminales):
		dicGlobal1[ListaTerminales[i]] = i+1
	
	#Guardando en un diccionario la lista de elementos no terminales	
	for j in xrange(total_noTerminales):
		dicGlobal2[listaNoTerminales[j]] = j+1	
		
	#Ingresando cada elemento en la celda segun su correspondencia de los terminales en las columnas	
	for x in xrange(1, total_terminales + 1):
		A[0][x] = ListaTerminales[x - 1]
		
	#Ingresando cada elemento en la celda segun su correspondencia de los no terminales en las filas	
	for y in xrange(1, total_noTerminales + 1):
		A[y][0] = listaNoTerminales[y - 1]
		
	#para cada valor dentro del diccionario de producciones, se guarda en la celda (i,j) los first de los elementos no terminales, de manera que se construya la tabla
	#según algoritmo dado. Si hay una vacia, se busca en los follows de la produccion, donde colocar la vacia.
	for key, values in dicProducciones.iteritems():
		for list1 in values:
			nt = list1[0]
			a = dicFirst[nt]
			b = dicFollow[nt]
			
			if a:
				for x in xrange(len(a)):
					if a[x] != '^':
						if not A[dicGlobal2[nt]][dicGlobal1[a[x]]]:
							A[dicGlobal2[nt]][dicGlobal1[a[x]]] = list1 
					elif a[x] == '^':
						for y in xrange(len(b)):
							A[dicGlobal2[nt]][dicGlobal1[b[y]]] = list1
	A[total_noTerminales][total_terminales] = 'G -> id1'	

	#rellenar en la tabla, cada celda que no tenga correspondencia entre no terminales y terminales, un error, para mejor manejo de la tabla
	for i in xrange(total_noTerminales + 1):
		for j in xrange(total_terminales + 1):
			if not A[i][j]:
				A[i][j] = 'Error'
		
	#Mostrando la tabla con un formato de tabla.
	xz = PrettyTable([x for x in A[0]])
	xz.align["No-Terminales"] = "l" 
	xz.padding_width = 1 		
	
	for i in xrange(1, total_noTerminales + 1):				
		xz.add_row([x for x in A[i]])
	
	print xz
		
	return A


#Metodo que se encarga de validar que el input de entrada sea valido para la gramatica dada en la tabla de parseo
def ValidarInput(listaInput, TablaParser, Axioma, listaNoTerminales):
	#Pila para el manejo de los elementos que se iran tomando de la tabla
	stack = ['$']
	#Se agrega el axioma de la gramatica a la tabla  
	stack.append(Axioma)
		
	#Algoritmo de validacion del input de entrada segun la tabla de parseo y la gramatica dada.
	while True:
		if stack[-1] == '$' and listaInput[0] == '$':
			return True
			#aceptar
		elif stack[-1] == listaInput[0]:
			stack.pop()
			del listaInput[0]	
			
		elif stack[-1] in listaNoTerminales:
			temp1 = TablaParser[dicGlobal2[stack[-1]]][dicGlobal1[listaInput[0]]]
			
			if temp1 != 'Error' :
				action = temp1
				for i in xrange(len(temp1)):
					if temp1[i] == '>':
						index = i + 2
			
				temp2 = temp1[index:]
				temp3 = temp2[::-1]
				
				if temp3 != '^' and temp3 != '1di':
					stack.pop()
					for item in temp3:
						stack.append(item)	
			 		
				elif temp3 == '1di':
					stack.pop()
					stack.append('id1')
				
				elif temp3 == '^':
					stack.pop()
			else:
				return False
				#rechazar
	return True
	
	

def main():
	inputString = "id1 + id1"
	inputInd = list(shlex.shlex(inputString))
	inputInd.append('$')

	print "INPUT: ",inputString, "\n"
	print "--------------------------------------"
	print "\n"

	#Definiendo las producciones de la gramatica en formato LL(1)
	producciones = {'S': ['S -> TX'], 
				   'X': ['X -> +TX','X -> -TX','X -> ^'],
				   'T': ['T -> FY'],
				   'Y': ['Y -> *FY','Y -> /FY','Y -> ^'],
				   'F': ['F -> (S)','F -> id1']}

	#Ingresando los elementos no terminales de la gramatica
	non_terminales = ['S','X','T','Y','F']
	#Ingresando los elementos terminales de la gramatica
	terminales = ['$','+','-','*','/','(',')','id1']
	
	#Definiendo los first de los elementos no terminales de la gramatica dada
	first = {'S': ['(','id1'],
			 'X': ['+','-','^'],
			 'T': ['(','id1'],
			 'Y': ['*','/','^'],
			 'F': ['(','id1']
			}

	#Definiendo los follow de los elementos no terminales de la gramatica dada
	follow = {'S': ['$',')'],
			  'X': ['$',')'],
			  'T': ['+','-','$',')'],
			  'Y': ['+','-','$',')'],
			  'F': ['*','/','+','-','$',')']
			 }

	#Accioma de la gramatica
	Axioma_state = 'S'

	print "Producciones: ", producciones, "\n"
	print "First: ", first, "\n"
	print "Folow: ", follow, "\n"

	#Obteniendo tabla de parseo
	A = TablaParseo(non_terminales, terminales, producciones, first, follow)

	#Validando el input de entrada
	boolean = ValidarInput(inputInd, A, Axioma_state, non_terminales)

	if boolean == True:
		print "\nPARSER: Input aceptado. . . \n"
	else:
		print "\nPARSER: Input invalido. . . \n"
	return 2


if __name__ == "__main__":
	sys.exit(main())
