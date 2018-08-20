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

def GenerateInstance(n,kk):
    K = range(kk)
    V = ['b']+list(range(n))
    
    c0=100
    x,y={},{}
    
    for i in V:
        x[i] = random.randint(0,100)
        y[i] = random.randint(0,100)
    c,t={},{}
    for i in V:
        for j in V:
            c[i,j] = math.sqrt((x[i]-x[j])**2 +(y[i]-y[j])**2)  
            t[i,j] =random.uniform(0.4,1)*c[i,j]+2
    
    a, b = {},{}
    for i in V:
        a[i] = random.uniform(0,100)
        b[i] = 100+a[i]      
    a['b']=0
    b['b']=sum(b[i] for i in V)
    d = {}
    for i in V:
        if i == 'b':
            d['b']=0
        else:
            d[i]= random.uniform(10,20)
    
    if kk >0:
        K0 = random.uniform(1.2,1.5)*sum(d[i] for i in V)/kk
    else:
        K0 =0
    return K, V, c0, c, t, a, b, x,y, d, K0

def TSP_Experiment(n):

    K, V, c0, c, t, a, b, x_pos,y_pos, d, K0 = GenerateInstance(n,0)

    mod = TSP(V, c)

    mod.optimize()

    x = mod.__data    
    #Creamos un grafo para dibujar la solución

    E = [(i,j) for i in V for j in V if j!=i and x[i,j].X==1]
    position = {}
    for i in V:
        position[i] = (x_pos[i],y_pos[i])

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