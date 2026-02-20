def bissection(f, x0, x1, tol):
    a = f(x0)
    b = f(x1)
    if a*b > 0:
        x = 0
        statut = 1
        print("Erreur: les 2 valeurs choisies sont de même signe")
        return [x, statut]
    
    elif a == 0:
        print(x0, " est une racine")
        statut = 0
        return [x0, statut]
    
    elif b == 0:
        print(x1, " est une racine")
        statut = 0
        return [x1, statut]
    
    imgX = 1000
    x = x0
    while abs(x1 - x0) > tol:
        x = (x0 + x1)/2
        imgX = f(x)
        
        if imgX*a > 0:
            x0 = x
        elif imgX*b > 0:
            x1 = x
        else:
            print("on est pil à la racine")
            break
    statut = 0
    return [x, statut]





def secante(f, x0, x1, tol):
    x = 1000
    p = x0# valeur précédente
    c = x1# valeur courante
    i = 0
    while  i <= 25 and abs(x - p) > tol :
        fp = f(p)
        fc = f(c)
        if fp == fc:
            print("erreur : division par 0 dans l'algorythme de la sécante car f(xn) = f(xn-1)")
            statut = -1
            break
        x = c - fc*( (c - p) / (fc - fp) )
        p =c
        c = x
        i += 1    
    if i > 25: statut = -1 #la fct n'a pas convergé
    else: statut = 0
    return [x, statut]




#test
from numpy.polynomial import Polynomial as poly
f = poly([-1, 2, 1])
rslt = bissection(f, -2, 1, 1e-6)
print(rslt)
rslt = secante(f, -2, 1, 1e-6)
print(rslt)