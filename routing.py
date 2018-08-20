# -*- coding: utf-8 -*-
"""
This code implements the "Routing Vehicle Problem with Time Windows" 

We also reproduce an small instance to solve and represent graphically.

This codes are part of the IN4703 - operations management's teaching examples

@author: Bucs
"""

from gurobipy import *
import math
import random
import networkx as NX #Para crear objetos que son grafos
import matplotlib.pyplot as Plt #Para graficar 
import itertools as it #Paquete con herramientas combinatoriales

def VRPTW(K, V, c0, c, t, a, b):
    MM = max(b[i] for i in V)*len(K)
    mod = Model('VRPTW')
    x, s = {}, {}
    
    for i in V:
        s[i] = mod.addVar(vtype = 'C', name='s[%s]' % i)
        for j in V:
            if j!=i:
                for k in K:
                    if i == 'b':
                        x[i,j,k] = mod.addVar(vtype = 'B', obj = c[i,j]+c0, name='x[%s,%s,%s]' % (i,j,k))
                    else:
                        x[i,j,k] = mod.addVar(vtype = 'B', lb = 0, obj = c[i,j], name='x[%s,%s,%s]' % (i,j,k))
                   
    mod.update()
    
    for j in V:
        if j!='b':
            mod.addConstr(quicksum(x[i,j,k] for k in K for i in V if i!=j)  == 1, name='in[%s]' %j)
            mod.addConstr(quicksum(x[j,i,k] for k in K for i in V if i!=j)  == 1, name='out[%s]' %j)   
    
    for k in K:
        for j in V:
            mod.addConstr(quicksum(x[i,j,k] for i in V if i!=j)-quicksum(x[j,i,k] for i in V if i!=j)  == 0, name='flow[%s,%s]' %(j,k))
    

    for k in K:
        mod.addConstr(quicksum(x['b',i,k] for i in V if i!='b')<=1, name='oneTour[%s]' %k)
    
    for i in V:
        mod.addConstr(a[i]<=s[i],  name='TWL[%s]' %i)
        mod.addConstr(s[i]<=b[i],  name='TWU[%s]' %i)
    
    for i in V:
        for j in V:
            if j!='b' and i!=j:
                for k in K:
                    mod.addConstr(s[j]>= s[i]+t[i,j]-(1-x[i,j,k])*MM)
    
    mod.addConstr(s['b']==0)
    mod.__data = x,s
    mod.params.IntFeasTol = 1e-9
    mod.params.DualReductions = 0
    mod.params.MIPGapAbs = 0
    mod.update()
    return mod
    
def CVRP(K, V, c0, c, d, K0):

    mod = Model('CVRP')
    x = {}
    
    for i in V:
        for j in V:
            if j!=i:
                for k in K:
                    if i == 'b':
                        x[i,j,k] = mod.addVar(vtype = 'B', obj = c[i,j]+c0, name='x[%s,%s,%s]' % (i,j,k))
                    else:
                        x[i,j,k] = mod.addVar(vtype = 'B', lb = 0, obj = c[i,j], name='x[%s,%s,%s]' % (i,j,k))
                   
    mod.update()
    for j in V:
        if j!='b':
            mod.addConstr(quicksum(x[i,j,k] for k in K for i in V if i!=j)  == 1, name='in[%s]' %j)
            mod.addConstr(quicksum(x[j,i,k] for k in K for i in V if i!=j)  == 1, name='out[%s]' %j)   
    
    U = subsets(V)
    for u in U:
        if 'b' not in u:
            for k in K:
                mod.addConstr(quicksum(x[i,j,k] for i in u for j in u if j!=i)<=len(u)-1)    
    
    for k in K:
        for j in V:
            mod.addConstr(quicksum(x[i,j,k] for i in V if i!=j)-quicksum(x[j,i,k] for i in V if i!=j)  == 0, name='flow[%s,%s]' %(j,k))
    

    for k in K:
        mod.addConstr(quicksum(x['b',i,k] for i in V if i!='b')<=1)
    
    for k in K:
        mod.addConstr(quicksum(x[i,j,k]*d[i] for i in V for j in V if j!=i)<=K0, name='cap[%s]' %k)

    mod.__data = x
    mod.params.IntFeasTol = 1e-9
    mod.params.DualReductions = 0
    mod.params.MIPGapAbs = 0
    mod.update()
    
    return mod

def TSP(V, c):

    mod = Model('TSP')
    
    x = {}
    for i in V:
        for j in V:
            if j!=i:
                x[i,j] = mod.addVar(vtype = 'B', obj = c[i,j])
    
    mod.update()
    
    for i in V:
        mod.addConstr(quicksum(x[i,j] for j in V if j!= i)>=1)
        mod.addConstr(quicksum(x[i,j] for j in V if j!= i)==quicksum(x[j,i] for j in V if j!= i))
#        mod.addConstr(quicksum(x[i,j] for j in V if j!= i)+quicksum(x[j,i] for j in V if j!= i)==2)
    
    U = subsets(V)
    for u in U:
        if len(u)<= (len(V))/2:
            mod.addConstr(quicksum(x[i,j] for j in u for i in u if j!=i)<=len(u)-1)
    
    mod.__data = x
    return mod
    
def subsets(Nodes):
    ## Return every subset of nodes of size greater than 1 and smaller than n-1.
    U = []
    for i in range(2,len(Nodes),1):
        A = list(it.combinations(Nodes, i))
        for a in A:
            U = U+[a]

    return U
    
    
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
    
def VRPTW_Experiment(n,k):
    K, V, c0, c, t, a, b, x_pos,y_pos, d, K0 = GenerateInstance(n,k)
    mod = VRPTW(K, V, c0, c, t, a, b)
    x,s= mod.__data    
    mod.optimize()
    if mod.status == GRB.status.INFEASIBLE:
        mod.computeIIS()
        mod.write('vrptw.ilp')    
        
    ff = open('sol_vrptw.txt','w')
    for i in V:
        for j in V:
            if i!=j:
                for k in K:
                    if x[i,j,k].X >0.9999:
                        ff.write(str(i) + '\t'+str(j)+'\t'+str(k)+'\n')
    #Creamos un grafo para dibujar la solución
    E = {}
    for k in K:
        E[k] = [(i,j) for i in V for j in V if j!=i and x[i,j,k].X>0.9999]
    position = {}
    for i in V:
        position[i] = (x_pos[i],y_pos[i])
    
    Plt.ion() # interactive mode on
    
    G = NX.Graph()
    
    G.add_nodes_from(V)

    NX.draw(G, position, node_color="red", node_size=80,nodelist=V)
    NX.draw(G, position, node_color="blue", node_size=80,nodelist=['b'])
    Plt.savefig('vrptw_instance_'+str(n)+'_'+str(k)+'_.png', format="PNG")
    Plt.clf()   # Clear figure
    
    for k in K:
        for (i,j) in E[k]:
            G.add_edge(i,j)
        
    NX.draw(G, position, node_color="red", node_size=80,nodelist=V)
    NX.draw(G, position, node_color="blue", node_size=80,nodelist=['b'])
    Plt.savefig('vrptw_'+str(n)+'_'+str(k)+'_.png', format="PNG")
    Plt.clf()   # Clear figure
  
        
    return 'ok'

def CVRP_Experiment(n,k):
    K, V, c0, c, t, a, b, x_pos,y_pos, d, K0 = GenerateInstance(n,k)
    mod = CVRP(K, V, c0, c, d, K0)
    x= mod.__data    
    mod.optimize()
    if mod.status == GRB.status.INFEASIBLE:
        mod.computeIIS()
        mod.write('vrp.ilp')    
        
    ff = open('sol_cvrp.txt','w')
    for i in V:
        for j in V:
            if i!=j:
                for k in K:
                    if x[i,j,k].X > 0.5:
                        ff.write(str(i) + '\t'+str(j)+'\t'+str(k)+'\n')
    
    ff.write('Total Charge \t'+str(sum(d[i] for i in V))+'\n')
    ff.write('Capacity of each truck \t'+str(K0))
    ff.close
    #Creamos un grafo para dibujar la solución
    E = {}
    for k in K:
        E[k] = [(i,j) for i in V for j in V if j!=i and x[i,j,k].X>0.9]
    
    position = {}
    for i in V:
        position[i] = (x_pos[i],y_pos[i])

    Plt.ion() # interactive mode on
    G = NX.Graph()
    
    G.add_nodes_from(V)
    NX.draw(G, position, node_color="red", node_size=80,nodelist=V)
    NX.draw(G, position, node_color="blue", node_size=80,nodelist=['b'])
    Plt.savefig('cvrp_instance_'+str(n)+'_'+str(k)+'_.png', format="PNG")
    Plt.clf()   # Clear figure
    for k in K:
        for (i,j) in E[k]:
            G.add_edge(i,j)


        
    NX.draw(G, position, node_color="red", node_size=80,nodelist=V)
    NX.draw(G, position, node_color="blue", node_size=80,nodelist=['b'])
    Plt.savefig('cvrp_'+str(n)+'_'+str(k)+'_.png', format="PNG")
#    Plt.clf()   # Clear figure
  
        
    return 'ok'
    

TSP_Experiment(9)
CVRP_Experiment(8,3)
VRPTW_Experiment(11,3)


















