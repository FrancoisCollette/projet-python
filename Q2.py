import numpy as np
import matplotlib.pyplot as plt
import RechercheRacine as r
import SimRayon as sim
import constantes as c    # ou encore from constantes import interval y0 dx nbRayons ect...

# ---------- Question 2.4 ----------

# définit la valeur correcte comme z en xf par IVP
# cacule z en xf par Euler pour chaque dx
# erreur commise comme différence des 2 solutions (IVP et Euler) trouvées

def tolerance():
    solIVP = sim.trajetRayonIVP(c.Xinterval, c.y0Tol, c.IVPtol, sim.profilTemperatureLin)
    zIVP = solIVP[1][0][-1] #prendre toute dernière val de z dans y[]
    print('solution par IVP : ', zIVP)
    print('les erreurs en x= 1000m en fonction du pas sont :')
    
    errTab = np.zeros(len(c.dxTab))
    i = 0
    for pas in c.dxTab:
        solEuler = sim.trajetRayonEuler(c.Xinterval, c.y0Tol, pas, sim.profilTemperatureLin)
        zEuler = solEuler[1][0][-1]
        erreur = abs(zEuler - zIVP)
        errTab[i] = erreur
        i += 1
        print(erreur)

    plt.figure(figsize=(15, 10))
    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14)
    plt.title(f"Graphique de l'erreur commise en {c.Xinterval[1]}m en fonction du pas", fontsize=20)
    plt.xlabel('taille du pas (m) (échelle logarithmique)', fontsize=16)
    plt.ylabel('erreur (m)', fontsize=16)

    plt.plot(c.dxTab, errTab, linewidth = 2)
    plt.xscale('log')
    plt.xlim(np.max(c.dxTab), np.min(c.dxTab)) #inverse axe x pour plus de lisibilité : de max -> min
    
    return 0



# ---------- Question 2.5 ----------

# plot la trajectoire z(x) du rayon pour différents i initiaux entre iMin et iMax
# nbAngles étant le nombre d'angles et donc de rayons différents considérés

def parcoursI():
    plt.figure(figsize=(15, 10))
    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14)
    plt.title('Graphique de différents rayons en fonction de i0', fontsize=20)
    plt.xlabel('distance de la source (m)', fontsize=16)
    plt.ylabel('hauteur z du rayon (m)', fontsize=16)

    angle = np.linspace(c.iMin, c.iMax, c.nbRayons)    #avec angles en radians

    for i in angle:
        c.y0[1] = i
        x, y = sim.trajetRayonEuler(c.Xinterval, c.y0, c.dx, sim.profilTemperatureLin)
        plt.plot(x, y[0], 'b', linewidth = 2)
    
    return 0


# ---------- Quetion 3.1 ----------

# fonction retournant la hauter z du rayon en xf (corrigé de -zf) en fct de i0
# si le rayon est absorbé par le sol, retourne None

def z(i0):
    c.y0[1] = i0
    x, y = sim.trajetRayonEuler(c.Xinterval, c.y0, c.dx, sim.profilTemperatureLin)
    if x[-1] < c.Xinterval[1] - c.dx:
        return None
    return y[0, -1] - c.zf


# fonction visant à déterminer les i0 tel que z(xf) = zf ; retourne les i0 trouvés et une variables de statut
# balaye les images produites par quelques angles pour trouver 2 angles produisant une image de part et d'autre de zf
# utilise ces 2 angles comme conditions initiales pour la recherche de racines
# si argument plot = True alors trace le graphe des particuliers rayons trouver et de quelques autres avec parcoursI()
# les rayons absorbés par le sol (z retourne None) entrainent directement l'iteration suivante de la boucle
# si un seul ou pas de rayons atteint zf alors la fonction retourne des None et statut = -1 ou -2

def imagesMultiples(plot):
    angles = np.linspace(c.iMin, c.iMax, c.nbIbalayage)
    solutions = np.array([None, None])
    j = 0
    
    for k in range(len(angles) - 1):
        z0 = z(angles[k])
        z1 = z(angles[k+1])
        
        if z0 is None or z1 is None:
            continue
        if z0 * z1 < 0:
            racine, statut = r.bissection(z, angles[k], angles[k+1], c.racineTol)
            if statut == 0:
                solutions[j] = racine
                j += 1
    
    if plot == True:
        parcoursI()
        for i in solutions:
            if i is None: 
                statut -= 1 
                continue
            x, y = sim.trajetRayonEuler(c.Xinterval, [c.y0[0], i], c.dx, sim.profilTemperatureLin)
            plt.plot(x, y[0], 'r', linewidth = 3, label = f'rayon dont z(xf) = zf avec i0 = {i} (rad)')
            plt.legend(loc='best', fontsize='16')
    
    statut = 0
    return np.array([solutions[0], solutions[1], statut])


# tolerance(interval, c.y0Tol, c.IVPtol, c.dxTab, sim.profilTemperatureLin)
# parcoursI(c.iMin, c.iMax, c.nbRayons, c.Xinterval, c.y0, c.dx)
# imagesMultiples()






