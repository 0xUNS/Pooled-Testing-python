import numpy as np
import math

n = 27 # taille de l'echantillon
m = 1 # individus infecte par le virus


def optimaldim(n):
    # Cette fonction cherche les dimentions du cube pour avoir le nombre minimale des tests
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

def echantillon_all(n, m, u):
    idpositifs = np.random.choice(n,m) # Une liste qui contient ( m ) individus positifs aux virus choisis aleatoirement parmi ( n ) personnes
    cube = np.zeros(n,dtype=int)
    cube[idpositifs] = 1
    cube = np.append(cube,np.zeros(np.prod(u)-n,dtype=int))
    # si cube[i,j,k] = 1 (resp. = 0): la pesonne positive (resp. negative) aux virus
    cube = cube.reshape(u)
    return cube

def faces(cube, u):
    face = np.zeros(3*max(u),dtype=int).reshape(3, max(u)) # un cube (3D) de 27 points contient 9 faces
    
    # Deusiemnt partie pour retrouver si vraiment les personnes choisies aleatoiremt sont les mêmes que nous retrouverons
    
    """ Melanger les prelevements de chaque groupe (faces)
        si face[i,j] = 1 (resp. = 0) : le groupe contient au moins une personne positive (resp. negative) """
    for j in range(u[0]):
        face[0,j] = int(sum(sum(cube[j,:,:])) != 0)
    for j in range(u[1]):
        face[1,j] = int(sum(sum(cube[:,j,:])) != 0)
    for j in range(u[2]):
        face[2,j] = int(sum(sum(cube[:,:,j])) != 0)
    return face

def infectees(face, id, u):
    nbpositif = 0
    infecte = []
    for i in range(u[0]):
        if face[0,i]:
            for j in range(u[1]):
                if face[1,j]:
                    for k in range(u[2]):
                        if face[2,k]:
                            infecte.append(id[i,j,k])
                            nbpositif += 1
                                    
    return infecte, nbpositif

u = optimaldim(n)
id = np.arange(np.prod(u), dtype=int).reshape(u)
cube = echantillon_all(n ,m, u)

face = faces(cube, u)
infecte , nbpositif= infectees(face, id, u)

print("\n Id : \n",id)
print("\n Cube :\n",cube)
print("\n Faces : \n",face)
print("\n Nombre des Tests effectués : ",sum(u))
print(f"\n Nombre probable de personnes infectées par le virus ({nbpositif}). Leur id : {infecte}")
print(f"\nPersonne positives ({sum(sum(sum(cube)))})\nFaces positives ({sum(sum(face))})\nPersonne detecté ({nbpositif})")