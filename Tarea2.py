# -*- coding: utf-8 -*-
"""
Created on Thu Aug 30 21:06:46 2018

@author: Takechi25
"""
from gurobipy import *
import math
import random
import networkx as NX
import matplotlib.pyplot as Plt
import itertools as it


def Nodos(f):
    N=[]
    for i in range(len(f)):
        N.append(f[i][0])
    return N

#N1=Nodos(instancia_17csv)
#N2=Nodos(instancia_50csv)
#N3=Nodos(instancia_150csv)
#N4=Nodos(instancia_250csv)



def costos(I):
    c={}
    for i in range(len(I)):
        for j in range(len(I)):
            lo1=float(I[i][1])
            lo2=float(I[j][1])
            la1=float(I[i][2])
            la2=float(I[j][2])
            c[i,j]= math.sqrt(((la2-la1)**2)+((lo2-lo1)**2))
    return c
#c1=costos(instancia_17csv)
#c2=costos(instancia_50csv)
#c3=costos(instancia_150csv)
#c4=costos(instancia_250csv)

def subsets(Nodes):
    ## Return every subset of nodes of size greater than 1 and smaller than n-1.
    U = []
    for i in range(2,len(Nodes),1):
        A = list(it.combinations(Nodes, i))
        for a in A:
            U = U+[a]

    return U

def mindist(N):
    costo=costos(N)
    minimo=10000000
    for i in costo:
        if costo[i]!=0:
            if costo[i]<minimo:
                minimo=costo[i]
    
        
    return minimo

def arcomin(N):  ## retorna un elemento de la tupla de nodos, donde esta tupla tiene la menor distancia de todas las otras tuplas posibles
    arcodist=mindist(N)  #se utiliza la funcion mindist 
    bas=N[1]  # se toma una base fija que no variara sus elementos nunca
    for i in range(len(bas)):
        for j in range(len(bas)):
            a=N[1][i]-N[1][j]
            b=N[2][i]-N[2][j]
            largo=(a**2+b**2)**(0.5)
            if largo==arcodist:
                return i

###############################################################################
#                              P2
###############################################################################
    
def TSPSE(N, c):

    mod = Model('TSPSE')
    x = {}
    for i in N:
        for j in N:
            if j!=i:
                x[i,j] = mod.addVar(vtype = 'B', obj = c[i,j])
    
    mod.update()
    
    for j in N:
        mod.addConstr(quicksum(x[i,j] for i in N if j!= i) + quicksum(x[j,i] for i in N if j!= i) == 2 )
        
    
    U = subsets(N)
    for u in U:
        if 2 < len(u)<= ((len(N))-1)/2:
            mod.addConstr(quicksum(x[i,j] for j in u for i in u if j!=i)<=len(u)-1)
    mod.optimize()
    mod.__data = x
    return mod
            
    
def TSPNF(N, c):

    mod = Model('TSPNF')
    x , f = {} , {}
    for i in  N:
        for j in N:
            if j!=i:
                x[i,j] = mod.addVar(vtype = 'B', obj = c[i,j])
                f[i,j] = mod.addVar(vtype = 'C')
    
    mod.update()
    
    for j in N:
        mod.addConstr(quicksum(x[i,j] for i in N if j!= i)+ quicksum(x[j,i] for i in N if j!= i) == 2 )
    for i in N :
        if i!=1:
            mod.addConstr(quicksum(f[i,j] for j in N if j!= i) - quicksum(f[j,i] for j in N if j!= i) == -1 )  
    for j in N:
        mod.addConstr(quicksum(f[1,j] for j in N if j!= 1) == len(N) -1)
    for i in N:
        for j in N:
            if j !=i:
               mod.addConstr( f[i,j]<=(len(N)-1)*x[i,j])
    for i in N:
        for j in N:
            if j!=i:
                mod.addConstr( f[i,j] >= 0)

    mod.optimize()
    mod.__data = x
    
    return mod
###############################################################################
#                               P3
###############################################################################
    
def Nodos2(datos):
    N=[],l1=[],l2=[],l3=[]
    for lista in datos:
        l1.append(lista[0])
        l2.append(lista[1])
        l3.append(lista[2])
    N.append(l1)
    N.append(l2)
    N.append(l3)
    return N

#n1=Nodos2(instancia_17csv)
#n2=Nodos2(instancia_50csv)
#n3=Nodos2(instancia_150csv)
#n4=Nodos2(instancia_250csv)

def costos(N):
    c={}
    for i in range(len(N[0])):
        for j in range(len(N[0])):
            a=N[1][i]-N[1][j]
            b=N[2][i]-N[2][j]
            dist=(a**2+b**2)**(0.5)
            c[i,j]=dist
    return c

def heur1(N):
    arcos=[]
    z=0
    base=range(len(N[1])) # se toma una base fija que no variara sus elementos nunca y su largo es igual a la cantidad de nodos
    costo=costos(N) # diccionario de costos de las instancias
    Nactual=N[0][1]  # se parte desde el segundo nodo en la lista
    visitados=[]
    while len(N[0])>1:    
        N[0].remove(Nactual) # se remueve el nodo en que estoy parado de los posibles nodos a viajar
        visitados.append(Nactual)  # se agrega el nodo que ya se visito
        dista=[]
        arco=[]
        for i in base: ##cantidad de nodos
            if i not in visitados:
                dista.append(costo[Nactual,i]) # aqui ocurre la magia
                
        arco.append(Nactual)   
        menor=min(dista)
        arco.append(N[0][dista.index(menor)])
        arcos.append(arco)
        z=z+menor
        Nactual=N[0][dista.index(menor)]
    auxiliar=[]  # no se como unir una lista de 2 elementos en otra lista
    auxiliar.append(Nactual)   #por eso creo una lista auxiliar que añade 2 nodos
    auxiliar.append(1)
    arcos.append(auxiliar)   # y luego esta lista auxiliar se agrega a los arcos
    z=z+costo[Nactual,1]
    visitados=visitados+N[0]+[1]
    return arcos,visitados # el N[0] es el ultimo nodo que aun no se agrega pero si se incluyo el gasto
# el 1 es porque vuelve al nodo inicial
    
###############################################################################
#                                   P4
###############################################################################

def heur2(N):
    arcos=[]
    z=0
    base=N[1]
    costo=costos(N)
    Nactual= arcomin(N)
    retorno=arcomin(N)
    visitados=[]
    while len(N[0])>1:    
        N[0].remove(Nactual)
        visitados.append(Nactual)
        dista=[]
        arco=[]
        for i in range(len(base)): ##cantidad de nodos
            if i not in visitados:
                dista.append(costo[Nactual,i]) # aqui ocurre la magia
                
        arco.append(Nactual)       
        menor=min(dista)
        arco.append(N[0][dista.index(menor)])
        arcos.append(arco)
        z=z+menor
        Nactual=N[0][dista.index(menor)]
    auxiliar=[]
    auxiliar.append(Nactual)
    auxiliar.append(retorno)
    arcos.append(auxiliar)
    z=z+costo[Nactual,retorno]
    visitados=visitados+N[0]+[retorno]
    return arcos,visitados

###############################################################################
#                                   P5
###############################################################################
    
def instancias(n):
    I=[]
    for i in range(n):
        x,y={},{}
        x[i] = random.randint(0,100)
        y[i] = random.randint(0,100)
        I.append((i,x[i],y[i]))
    return I

def crear(cantidad,tamano): # crea varias instancias, especificamente de la cantidad especificada y el tamaño especificada
    todas=list(range(cantidad))
    for i in range(cantidad):
        todas[i]= instancias(tamano)   #### aca esta la lista de listas de listas 
    return todas
#i1=crear(15,6)
#i2=crear(15,9)
#i3=crear(15,12)
#i4=crear(15,15)


def TSPSER(N, c):

    modR = Model('TSPSER')
    x = {}
    for i in N:
        for j in N:
            if j!=i:
                x[i,j] = modR.addVar(vtype = 'C', obj = c[i,j])
    
    modR.update()
    
    for j in N:
        modR.addConstr(quicksum(x[i,j] for i in N if j!= i) + quicksum(x[j,i] for i in N if j!= i) == 2 )
        
    
    U = subsets(N)
    for u in U:
        if 2 < len(u)<= ((len(N))-1)/2:
            modR.addConstr(quicksum(x[i,j] for j in u for i in u if j!=i)<=len(u)-1)
    for i in N:
        for j in N:
            if j!=i:
                modR.addConstr( 1 >= x[i,j] >= 0)
    modR.optimize()
    modR.__data = x
    return modR


def TSPNFR(N, c):

    modR = Model('TSPNFR')
    x , f = {} , {}
    for i in  N:
        for j in N:
            if j!=i:
                x[i,j] = modR.addVar(vtype = 'C', obj = c[i,j])
                f[i,j] = modR.addVar(vtype = 'C')
    
    modR.update()
    
    for j in N:
        modR.addConstr(quicksum(x[i,j] for i in N if j!= i)+ quicksum(x[j,i] for i in N if j!= i) == 2 )
    for i in N :
        if i!=1:
            modR.addConstr(quicksum(f[i,j] for j in N if j!= i) - quicksum(f[j,i] for j in N if j!= i) == -1 )  
    for j in N:
        modR.addConstr(quicksum(f[1,j] for j in N if j!= 1) == len(N) -1)
    for i in N:
        for j in N:
            if j !=i:
               modR.addConstr( f[i,j]<=(len(N)-1)*x[i,j])
    for i in N:
        for j in N:
            if j!=i:
                modR.addConstr( f[i,j] >= 0)
    for i in N:
        for j in N:
            if j!=i:
                modR.addConstr( 1 >= x[i,j] >= 0)
    modR.optimize()
    modR.__data = x
    
    
    return modR

    
def graficah1(N):
    
    arcos,nodos=heur2(N)
 
    

    edges = [(i,j) for (i,j) in arcos]
    nodes=[j for j in nodos]
    
    Plt.ion() # interactive mode on
    G = NX.Graph()
    
    G.add_nodes_from(range(len(N[1])))
    
    for (i,j) in edges:
        G.add_edge(i,j)
    position={}
    for i in range(len(N[1])):
        position[i] = (N[1][i],N[2][i])

    
    NX.draw(G, position, node_color="red", node_size=80,nodelist=nodes)
    Plt.savefig('tsp_'+"esto"+'.png', format="PNG")

#    Plt.clf()   # Clear figure
    return 'ok'

def graficaSE(N):
    mod = TSPSE(N)

    mod.optimize()

    x = mod.__data   

    #Creamos un grafo para dibujar la solución

    E = [(i,j) for i in range(len(N[1])) for j in range(len(N[1])) if j!=i and x[i,j].X==1]
    position = {}
    for i in range(len(N[1])):
        position[i] = (N[1][i],N[2][i])

    Plt.ion() # interactive mode on
    G = NX.Graph()
    
    G.add_nodes_from(range(len(N[1])))
    
    for (i,j) in E:
        G.add_edge(i,j)

    NX.draw(G, position, node_color="red", node_size=80,nodelist=range(len(N[1])))
    Plt.savefig('tsp_'+"esto"+'.png', format="PNG")
#    Plt.clf()   # Clear figure
    return 'ok'
####################### a) #########################
    
def compararNF(li):
    lc=[]
    for i in range (0,len(li)):
        ins=li[i] 
        N= Nodos(ins)
        c=costos(ins)
        mod = TSPNF(N,c)
        print("")
        print("Óptimo",mod.ObjVal)
        print("")    
        modR= TSPNFR(N,c)
        print("")
        print("Óptimo relajado",modR.ObjVal)
        print("")
        GAP=modR.ObjVal /mod.ObjVal
        print ("GAP =", GAP)
        lc.append(GAP)
    return lc

def promediar(l):
    sum=0.0
    for i in range(0,len(l)):
        sum=sum+l[i]
 
    return sum/len(l)    

def compararSE(li):
    lc=[]
    for i in range (0,len(li)):
        ins=li[i] 
        N= Nodos(ins)
        c=costos(ins)
        mod = TSPSE(N, c)
        print("")
        print("Óptimo",mod.ObjVal)
        print("")    
        modR= TSPSER(N, c)
        print("")
        print("Óptimo relajado",modR.ObjVal)
        print("")
        GAP=modR.ObjVal /mod.ObjVal
        print ("GAP =", GAP)
        lc.append(GAP)
    return lc

#### NF
#
#GAPNEn6= compararNF(i1)
#GAPNEn9= compararNF(i2)
#GAPNEn12= compararNF(i3)
#GAPNEn15= compararNF(i4)
#
#proGFn6= promediar(GAPNEn6)
#proGFn9= promediar(GAPNEn9)
#proGFn12= promediar(GAPNEn12)
#proGFn15= promediar(GAPNEn15)
#
##SE
#
#GAPSEn6= compararSE(i1)
#GAPSEn9= compararSE(i2)
#GAPSEn12= compararSE(i3)
#GAPSEn15= compararSE(i4)
#
#proGSn6= promediar(GAPSEn6)
#proGSn9= promediar(GAPSEn9)
#proGSn12= promediar(GAPSEn12)
#proGSn15= promediar(GAPSEn15)

def graficarp5(x,y,a,b):
    L1=[x,y,a,b]
    Ltama=[6,9,12,15]
    Plt.subplot(1,2,1)
    Plt.plot(Ltama,L1)
    Plt.title("Graﬁco del GAP promedio en función del tamanño de la instancia.")
    Plt.xlabel("Tamaño Instancia")
    Plt.ylabel("Promedio GAP")
    Plt.savefig('P5'+"a"+'.png', format="PNG")
    
    return Plt.plot(Ltama,L1)

###############################  b)   #########################################

