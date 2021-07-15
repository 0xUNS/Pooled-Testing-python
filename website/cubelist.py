import numpy as np
import math

#Indv = [i for i in range(27)]
#resultats = ['1', '0', '0', '0', '1', '0', '0', '0', '1']

#listIndv = main(Indv)
#print(infectees(resultats, Indv))

def optimaldim(n):
    d = []
    u = int(math.sqrt(n))
    w = 0
    while u > 1:
        w += 1
        u = round(math.sqrt(n/w))
        if (w * u * u - n) >= 0 :
            d.append([u,w])
    y = [x[0]+x[0]+x[1] for x in d]
    i = y.index(min(y))
    return [d[i][0], d[i][0], d[i][1]]

def initialization(Indv):
    u = []
    u = optimaldim(len(Indv))
    id = np.array(Indv)
    id = np.append(id, np.zeros(np.prod(u) -len(id),dtype=int)).reshape(u)
    return u , id
    
def mainlist(Indv):
    u, id =initialization(Indv)
    faceIndv = [[],[],[]]
    listIndv = []
    for i in range(u[0]):
        temp = np.ravel(id[i,:,:])
        faceIndv[0].append( temp.tolist() )
    for i in range(u[1]):
        temp = np.ravel(id[:,i,:])
        faceIndv[1].append( temp.tolist() )
    for i in range(u[2]):
        temp = np.ravel(id[:,:,i])
        faceIndv[2].append( temp.tolist() )
    for i in range(len(faceIndv)):
        for j in range(len(faceIndv[i])):
            listIndv.append(faceIndv[i][j])
    return listIndv

def infectees(resultats, Indv):
    u, id =initialization(Indv)
    face = np.zeros(3*max(u)).reshape(3, max(u))
    k = 0
    for i in range(3):
        for j in range(u[i]):
            face[i,j] = resultats[k]
            k += 1
    infecte = []
    for i in range(u[0]):
        if face[0,i]:
            for j in range(u[1]):
                if face[1,j]:
                    for k in range(u[2]):
                        if face[2,k]:
                            infecte.append(id[i,j,k])
    return infecte