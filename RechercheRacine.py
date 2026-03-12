import numpy as np #nécessaire pour la correction apparemment
def bissection(f, x0, x1, tol):
    a = f(x0)
    b = f(x1)
    
    if abs(a) < tol:
        print(x0, " est une racine")
        statut = 0
        return [x0, statut]
    
    elif abs(b) < tol:
        print(x1, " est une racine")
        statut = 0
        return [x1, statut]
    
    elif a*b > 0:   #arrêt si les 2 vals sont de même signe
        x = 0
        statut = 1
        print("Erreur: les 2 valeurs choisies sont de même signe")
        return [x, statut]
    
    x = x0
    while abs(x1 - x0) > tol:
        x = (x0 + x1)/2
        imgX = f(x)
        
        if abs(imgX) < tol: #on tombe pile sur la racoine en divisant l'intervalle
            return [x, 0]
        
        if imgX*a > 0:
            x0 = x
        elif imgX*b > 0:
            x1 = x
        
    statut = 0
    return [x, statut]



def secante(f, x0, x1, tol):
    x = c = x1          #initialisation de x à nombre quelquonque, c : val courante
    p = x0              # p : val précédente
    i = 0
    fp = f(p)
    fc = f(c)
    
    if abs(fp) < tol:
        print(x0, " est une racine")
        statut = 0
        return [x0, statut]
    
    elif abs(fc) < tol:
        print(x1, " est une racine")
        statut = 0
        return [x1, statut]
    
    while  abs(x - p) > tol :
        if abs(fp - fc) < 1e-15:
            print("erreur : division par 0 dans l'algorythme de la sécante car f(xn) = f(xn-1)")
            return [x, -1]
        
        x = c - fc*( (c - p) / (fc - fp) )
        p = c
        fp = fc
        c = x
        fc = f(c)
        i += 1
        
        if i >= 50: return [x, -1] #la fct n'a pas convergé

    return [x, 0]

