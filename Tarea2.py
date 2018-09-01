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
from time import time

def nodosins(ins):
    N=[]
    for i in range(len(ins[0])):
        N.append(ins[0][i][0])
    return N

nodo1ins1=nodosins(i1)
nodo1ins2=nodosins(i2)
nodo1ins3=nodosins(i3)
nodo1ins4=nodosins(i4)

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
#c1ins1=costos(i1[0])
#c2ins2=costos(i2[0])
#c3ins3=costos(i3[0])
#c4ins4=costos(i4[0])

def subsets(Nodes):
    ## Return every subset of nodes of size greater than 1 and smaller than n-1.
    U = []
    for i in range(2,len(Nodes),1):
        A = list(it.combinations(Nodes, i))
        for a in A:
            U = U+[a]

    return U


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
def mascerca(c,q,D):
    j=float('inf')
    for i in D:
        if c[q,i]<j:
            p=i
    return p

def heur1(N,c,nodo):
    Nactual=nodo
    copia=N[:]
    copia.pop(copia.index(nodo))
    lista=[nodo]
    while copia!=[]:
        nodo=mascerca(c,Nactual,copia)
        lista.append(nodo)
        copia.pop(copia.index(nodo))
        Nactual=nodo
    c_opti=0
    B=[]
    for i in lista:
        if lista.index(i)!=len(lista)-1:
            c_opti=c_opti + c[i,lista[lista.index(i)+1]]
            B.append((i,lista[lista.index(i)+1]))
        else:
            c_opti=c_opti + c[i,lista[0]]
            B.append((i,lista[0]))
    
    return {'costo optimo':c_opti, 'camino':lista,'arcos utilizados':B}
###############################################################################
#                                   P4
###############################################################################









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

def graficarp5a(x,y,a,b):
    L1=[x,y,a,b]
    Ltama=[6,9,12,15]
    Plt.plot(Ltama,L1)
    Plt.title("Graﬁco del GAP promedio en función del tamanño de la instancia.")
    Plt.xlabel("Tamaño Instancia")
    Plt.ylabel("Promedio GAP")
    
    return Plt.plot(Ltama,L1)

###############################  b)   #########################################
    
def tiemposolSE(li):
    times=[]
    for i in range(len(li)):
        ins=li[i]
        N=Nodos(ins)
        c=costos(ins)
        mod= TSPSE(N,c)
        tiempo=mod.Runtime
        times.append(tiempo)
    return times
#timeSE6=tiemposolSE(i1)
#timeSE9=tiemposolSE(i2)
#timeSE12=tiemposolSE(i3)
#timeSE15=tiemposolSE(i4)
#
#protimeSEn6= promediar(timeSE6)
#protimeSEn9= promediar(timeSE9)
#protimeSEn12= promediar(timeSE12)
#protimeSEn15= promediar(timeSE15)

def tiemposolNF(li):
    times=[]
    for i in range(len(li)):
        ins=li[i]
        N=Nodos(ins)
        c=costos(ins)
        mod= TSPNF(N,c)
        tiempo=mod.Runtime
        times.append(tiempo)
    return times

#timeNF6=tiemposolNF(i1)
#timeNF9=tiemposolNF(i2)
#timeNF12=tiemposolNF(i3)
#timeNF15=tiemposolNF(i4)
#
#protimeNFn6= promediar(timeNF6)
#protimeNFn9= promediar(timeNF9)
#protimeNFn12= promediar(timeNF12)
#protimeNFn15= promediar(timeNF15)


def tiemposolh1(li):
    times=[]
    for i in range(len(li)):
        t1=time()
        ins=li[i]
        N=Nodos(ins)
        c=costos(ins)
        heur1(N,c,0)
        t2=time()
        t3=t2-t1
        times.append(t3)
    return times

#tiempoh1n6=tiemposolh1(i1)
#tiempoh1n9=tiemposolh1(i2)
#tiempoh1n12=tiemposolh1(i3)
#tiempoh1n15=tiemposolh1(i4)
#
#promediotimeh1n6=promediar(tiempoh1n6)
#promediotimeh1n9=promediar(tiempoh1n9)
#promediotimeh1n12=promediar(tiempoh1n12)
#promediotimeh1n15=promediar(tiempoh1n15)

def graficarp5b(x,y,a,b):
    L1=[x,y,a,b]
    Ltama=[6,9,12,15]
    Plt.plot(Ltama,L1)
    Plt.title("Graﬁco del tiempo promedio en función del tamanño de la instancia.")
    Plt.xlabel("Tamaño Instancia")
    Plt.ylabel("Tiempo promedio")
    
    return Plt.plot(Ltama,L1)

###############################  c ############################################
def compararh1SE(li,nodo):
    
    lc=[]
    for i in range (0,len(li)):
        ins=li[i] 
        N= Nodos(ins)
        c=costos(ins)
        mod = TSPSE(N, c)
        print("")
        print("Óptimo",mod.ObjVal)
        print("")    
        modR= heur1(N,c,nodo)
        print("")
        print("Óptimo heuristica 1",modR['costo optimo'])
        print("")
        GAP=modR['costo optimo']/mod.Objval
        print ("GAP =", GAP)
        lc.append(GAP)
    return lc
#GAPSEh1n6=compararh1SE(i1,0)
#GAPSEh1n9=compararh1SE(i2,0)
#GAPSEh1n12=compararh1SE(i3,0)
#GAPSEh1n15=compararh1SE(i4,0)
    
#proGAPSEH1n6=promediar(GAPSEh1n6)
#proGAPSEH1n9=promediar(GAPSEh1n9)
#proGAPSEH1n12=promediar(GAPSEh1n12)
#proGAPSEH1n15=promediar(GAPSEh1n15)

def compararh1NF(li,nodo):
    
    lc=[]
    for i in range (0,len(li)):
        ins=li[i] 
        N= Nodos(ins)
        c=costos(ins)
        mod = TSPNF(N, c)
        print("")
        print("Óptimo",mod.ObjVal)
        print("")    
        modR= heur1(N,c,nodo)
        print("")
        print("Óptimo heuristica 1",modR['costo optimo'])
        print("")
        GAP=modR['costo optimo']/mod.Objval
        print ("GAP =", GAP)
        lc.append(GAP)
    return lc
#GAPNFh1n6=compararh1NF(i1,0)
#GAPNFh1n9=compararh1NF(i2,0)
#GAPNFh1n12=compararh1NF(i3,0)
#GAPNFh1n15=compararh1NF(i4,0)
#
#proGAPNFH1n6=promediar(GAPNFh1n6)
#proGAPNFH1n9=promediar(GAPNFh1n9)
#proGAPNFH1n12=promediar(GAPNFh1n12)
#proGAPNFH1n15=promediar(GAPNFh1n15)

def graficarp5c(x,y,a,b):
    L1=[x,y,a,b]
    Ltama=[6,9,12,15]
    Plt.plot(Ltama,L1)
    Plt.title("Graﬁco del GAP promedio en función del tamanño de la instancia.")
    Plt.xlabel("Tamaño Instancia")
    Plt.ylabel("GAP promedio")
    
    return Plt.plot(Ltama,L1)

# falta la cosa de h2
    
###############################################################################
#                                   P6
###############################################################################

    
##############################  a #############################################

def TSPSESS(N, c):

    mod = Model('TSPSESS')
    x = {}
    for i in N:
        for j in N:
            if j!=i:
                x[i,j] = mod.addVar(vtype = 'B', obj = c[i,j])
    
    mod.update()
    
    for j in N:
        mod.addConstr(quicksum(x[i,j] for i in N if j!= i) + quicksum(x[j,i] for i in N if j!= i) == 2 )
    
    
    mod.__data=x
    return mod

def graficaSESS(Ne):
    N=Nodos(Ne)
    c=costos(Ne)
    mod = TSPSESS(N, c)

    mod.optimize()

    x = mod.__data    
    #Creamos un grafo para dibujar la solución
    E=[]
    for i in N:
        for j in N:
            if i!=j:
                if x[i,j].X==1:
                    E.append((i,j))
    
    position = {}
    for i in N:
        position[i] = (Ne[i][1],Ne[i][2])

    Plt.ion() # interactive mode on
    G = NX.Graph()
    for (i,j) in E:
        G.add_edge(i,j)

    NX.draw(G, position, node_color="red", node_size=150,nodelist=N)
    node_labels=NX.get_node_attributes(G,'s')
    NX.draw_networkx_labels(G,position,labels=node_labels)
    NX.draw(G, position, node_color="blue", node_size=150,nodelist=[0])
    Plt.savefig('TSP_SE_experimento_Sin_ST_'+ str(len(Ne)) +'_10.png', format="PNG")

#    Plt.clf()   # Clear figure
    return 'ok'
#optimo=284.926 
################################ b ############################################
    

def TSPSESb(N,c):
 
    mod = Model('TSPSESb')  
    x = {}
    for i in N:
        for j in N:
            if j!=i:
                x[i,j] = mod.addVar(vtype = 'B', obj = c[i,j])
    
    mod.update()
    
    for i in N:
        mod.addConstr(quicksum(x[i,j] for j in N if j!= i)+quicksum(x[j,i] for j in N if j!= i)==2)
    mod.addConstr(x[0,4]+x[4,0]+x[4,6]+x[6,4]+x[0,6]+x[6,0]<=2)
       # mod.addConstr(quicksum(x[i,j] for j in N[0] if j!= i)==quicksum(x[j,i] for j in N[0] if j!= i))
    
            
    mod.__data=x

    return mod

def graficaSESb(Ne):
    N=Nodos(Ne)
    c=costos(Ne)
    mod = TSPSESb(N, c)

    mod.optimize()

    x = mod.__data    
    #Creamos un grafo para dibujar la solución
    E=[]
    for i in N:
        for j in N:
            if i!=j:
                if x[i,j].X==1:
                    E.append((i,j))
    
    position = {}
    for i in N:
        position[i] = (Ne[i][1],Ne[i][2])

    Plt.ion() # interactive mode on
    G = NX.Graph()
    for (i,j) in E:
        G.add_edge(i,j)
    for i in N:
        G.add_node(i)
        G.node[i]['s']=i

    NX.draw(G, position, node_color="red", node_size=150,nodelist=N)
    node_labels=NX.get_node_attributes(G,'s')
    NX.draw_networkx_labels(G,position,labels=node_labels)
    NX.draw(G, position, node_color="blue", node_size=150,nodelist=[0])
    Plt.savefig('TSP_SE_experimento_Sin_ST_'+ str(len(Ne)) +'_p6b.png', format="PNG")

#    Plt.clf()   # Clear figure
    return 'ok'

############################## c ##############################################
def TSPSESc(N,c):
 
    mod = Model('TSPSESc')  
    x = {}
    for i in N:
        for j in N:
            if j!=i:
                x[i,j] = mod.addVar(vtype = 'B', obj = c[i,j])
    
    mod.update()
    
    for i in N:
        mod.addConstr(quicksum(x[i,j] for j in N if j!= i)+quicksum(x[j,i] for j in N if j!= i)==2)
    mod.addConstr(x[2,9]+x[9,12]+x[9,2]+x[12,9]+x[2,12]+x[12,2]<=2)
    mod.addConstr(x[0,4]+x[4,0]+x[4,6]+x[6,4]+x[0,6]+x[6,0]<=2)
    mod.addConstr(x[0,5]+x[5,0]<=1)
    mod.addConstr(x[0,4]+x[4,0]+x[4,6]+x[6,4]+x[5,6]+x[6,5]+x[5,0]+x[0,5]<=3)
    mod.addConstr(x[0,4]+x[4,0]+x[4,6]+x[6,4]+x[6,15]+x[15,6]+x[15,5]+x[5,15]+x[5,0]+x[0,5]<=4)
    mod.addConstr(x[0,4]+x[4,0]<=1)
    mod.addConstr(x[0,11]+x[11,0]<=1)
    mod.addConstr(x[12,9]+x[9,12]<=1)
    mod.addConstr(x[11,14]+x[14,11]+x[16,14]+x[14,16]+x[16,1]+x[1,16]<=3)
    mod.addConstr(x[15,5]+x[5,15]<=1)
    mod.addConstr(x[11,14]+x[14,11]+x[16,14]+x[14,16]+x[16,1]+x[1,16]+x[1,11]+x[11,1]<=3)
    mod.addConstr(x[11,14]+x[14,11]+x[16,11]+x[11,16]+x[16,1]+x[1,16]+x[1,14]+x[14,1]<=3)
    mod.addConstr(x[12,2]+x[2,12]<=1)
    mod.addConstr(x[1,14]+x[14,1]+x[16,14]+x[14,16]+x[16,1]+x[1,16]<=2)
    mod.addConstr(x[1,14]+x[14,1]+x[16,14]+x[14,16]+x[16,11]+x[11,16]+x[1,11]+x[11,1]<=3)
    mod.addConstr(x[6,4]+x[4,6]<=1)
    mod.addConstr(x[7,10]+x[10,7]<=1)
    mod.addConstr(x[1,16]+x[16,1]<=1)
    
    mod.__data=x

    return mod

def graficaSESc(Ne):
    N=Nodos(Ne)
    c=costos(Ne)
    mod = TSPSESc(N, c)

    mod.optimize()

    x = mod.__data    
    #Creamos un grafo para dibujar la solución
    E=[]
    for i in N:
        for j in N:
            if i!=j:
                if x[i,j].X==1:
                    E.append((i,j))
    
    position = {}
    for i in N:
        position[i] = (Ne[i][1],Ne[i][2])

    Plt.ion() # interactive mode on
    G = NX.Graph()
    for (i,j) in E:
        G.add_edge(i,j)
    for i in N:
        G.add_node(i)
        G.node[i]['s']=i

    NX.draw(G, position, node_color="red", node_size=150,nodelist=N)
    node_labels=NX.get_node_attributes(G,'s')
    NX.draw_networkx_labels(G,position,labels=node_labels)
    NX.draw(G, position, node_color="blue", node_size=150,nodelist=[0])
    Plt.savefig('TSP_SE_experimento_Sin_ST_'+ str(len(Ne)) +'_p6b.png', format="PNG")

#    Plt.clf()   # Clear figure
    return 'ok'
op=[298.424,310.722,311.48,313.229,313.987,314.131,316.181,321.726,327.794,328.678,328.955,332.587,335.907,339.81,345.874,346.597,349.935]
res=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17]
Plt.plot(op,res)
Plt.title("Graﬁco del optimo vs cantidad de restricciones.")
Plt.xlabel("Cantidad de restricciones")
Plt.ylabel("optimos")
################################## d ##########################################

def TSP_Experimenth1(insta):
    
#    N=nodosins(insta)
#    c=costos(insta[0])
    N=Nodos(insta)
    c=costos(insta)
    B=heur1(N,c,0)
    position={}       
    for i in N:
#        position[i] = (insta[0][i][1],insta[0][i][2])
        position[i] = (insta[i][1],insta[i][2])
    
    Plt.ion() # interactive mode on
    G = NX.Graph()    
    for (i,j) in B['arcos utilizados']:
        G.add_edge(i,j)
    
    NX.draw(G, position, node_color="red", node_size=150,nodelist=N)
    node_labels=NX.get_node_attributes(G,'s')
    NX.draw_networkx_labels(G,position,labels=node_labels)
    NX.draw(G, position, node_color="blue", node_size=150,nodelist=[0])

#TSP_Experimenth1(instancia_17csv)
#
#costoh1=' 861.7775945790911
#costooptimo=349.935

###############################################################################
#                                  P7
###############################################################################

#TSP_Experimenth1(instancia_50csv)
#TSP_Experimenth1(instancia_150csv)
#TSP_Experimenth1(instancia_250csv)

#costoh150=' 2904.013187175283
#costoh1150=' 7770.64305590664
#costoh1250=' 13163.643121970219

