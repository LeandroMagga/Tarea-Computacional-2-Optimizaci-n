# -*- coding: utf-8 -*-
from gurobipy import *
import math
import random
import networkx as NX #Para crear objetos que son grafos
import matplotlib.pyplot as Plt #Para graficar 
import itertools as it #Paquete con herramientas combinatoriales

N1=[]#lista de nodos
def nodos1(instancia_17csv):
    for p in range(17):
        q=instancia_17csv[p][0]
        N1.insert(p,q)
    return N1
nodos1(instancia_17csv)

A=[]#lista de arcos
def arcos(N1):
    for i in range(17):
        for j in range(17):
            f=(N1[i],N1[j])
            A.insert(i,f)
    return A
arcos(N1)

U={}#coordenadas del nodo i
def coordenadas(N1):
    for i in N1:
            x=instancia_17csv[i][1]
            y=instancia_17csv[i][2]
            U[i]=(x,y)
    return U
coordenadas(N1)

A=[]#lista de arcos
def arcos(N1):
    for i in range(17):
        for j in range(17):
            f=(N1[i],N1[j])
            A.insert(i,f)
    return A
arcos(N1)

c={}# diccionario con los largos euclidianos de cada nodo
def aux(A):
    for z in range(289):
        s=A[z]
        n1=A[z][0]
        n2=A[z][1]
        lo1=instancia_17csv[n1][1]
        lo2=instancia_17csv[n2][1]
        la1=instancia_17csv[n1][2]
        la2=instancia_17csv[n2][2]
        c[s]=math.sqrt(((la2-la1)**2)+((lo2-lo1)**2))
    return c
aux(A)

def subsets(N1):
    ## Return every subset of nodes of size greater than 1 and smaller than n-1.
    S = []
    for i in range(2,len(N1),1):
        B = list(it.combinations(N1, i))
        for a in B:
            S = S+[a]

    return S
#subsets(N1)




def TSP(N1, c):

    mod = Model('TSP')
    
    x = {}
    for i in N1:
        for j in N1:
            if j!=i:
                x[i,j] = mod.addVar(vtype = 'B', obj = c[i,j])
    
    mod.update()
    
    for i in N1:
        mod.addConstr(quicksum(x[i,j] for j in N1 if j!= i)+quicksum(x[j,i] for j in N1 if j!= i)==2)
    
    S = subsets(N1)
    for s in S:
        if len(s)<= (len(N1))/2:
            mod.addConstr(quicksum(x[i,j] for j in s for i in s if j!=i)<=len(s)-1)
    
    mod.__data = x
    return mod




def TSP_Experiment():

    N1, c, U

    mod = TSP(N1, c)

    mod.optimize()

    x = mod.__data    
    #Creamos un grafo para dibujar la solución

    E = [(i,j) for i in N1 for j in N1 if j!=i and x[i,j].X==1]
    position = {}
    for i in N1:
        position[i] = (U[i][0],U[i][1])

    Plt.ion() # interactive mode on
    G = NX.Graph()
    
    G.add_nodes_from(V)
    
    NX.draw(G, position, node_color="red", node_size=80,nodelist=V)
    NX.draw(G, position, node_color="blue", node_size=80,nodelist=['b'])
    Plt.savefig('tsp_instance_'+str(n)+'.png', format="PNG")
    
    for (i,j) in E:
        G.add_edge(i,j)

    NX.draw(G, position, node_color="red", node_size=80,nodelist=V)
    NX.draw(G, position, node_color="blue", node_size=80,nodelist=['b'])
    Plt.savefig('tsp_'+str(n)+'.png', format="PNG")
#    Plt.clf()   # Clear figure
    return 'ok'

