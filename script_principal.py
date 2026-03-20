import numpy as np
import time
import matplotlib.pyplot as plt
import RechercheRacine as r
import SimRayon as sim
import matplotlib.image as img
import constantes as c


# ----- variable globale pour Q4 ------
y0 = c.y0
# nécessaire pour modifier la hauteur initiale de chaque pixel



# ---------- Question 2.4 ----------

# définit la valeur correcte comme z en xf par IVP
# cacule z en xf par Euler pour chaque dx ainsi que le temps de calcul nécessaire à Euler
# erreur commise comme différence des 2 solutions (IVP et Euler) trouvées
# plot un graphique de l'erreur et du temps de calcul en fonction du pas

def tolerance():
    solIVP = sim.trajetRayonIVP(c.Xinterval, c.y0Tol, c.IVPtol, sim.profilTemperatureLin)
    zIVP = solIVP[1][0][-1] #prendre toute dernière val de z dans y[]
    print('solution par IVP : ', zIVP)
    print('les erreurs en x= 1000m en fonction du pas sont :')
    
    errTab = np.zeros( len(c.dxTab) )
    tempsTab = np.zeros( len(c.dxTab) )
    i = 0
    for pas in c.dxTab:
        t0 = time.perf_counter()
        solEuler = sim.trajetRayonEuler(c.Xinterval, c.y0Tol, pas, sim.profilTemperatureLin)
        tf = time.perf_counter()
        
        zEuler = solEuler[1][0][-1]
        erreur = abs(zEuler - zIVP)
        errTab[i] = erreur
        tempsTab[i] = tf - t0
        i += 1
        print(erreur)
    
    fig, ax1 = plt.subplots(figsize=(15, 10))       # Double axe Y pour superposer erreur et temps
    ax1.set_xlabel('taille du pas (m) (échelle logarithmique)', fontsize=16)
    ax1.set_ylabel('erreur (m)', fontsize=16, color='b')
    ax1.plot(c.dxTab, errTab, 'b', linewidth=2, label='erreur')
    ax1.tick_params(axis='y', labelcolor='b', labelsize = 12)
    ax1.set_xscale('log')
    ax1.set_xlim(np.max(c.dxTab), np.min(c.dxTab))
    
    ax2 = ax1.twinx()                               # deuxième axe Y qui partage le même axe X
    ax2.set_ylabel('temps de calcul (s)', fontsize=16, color='g')
    ax2.plot(c.dxTab, tempsTab, 'g', linewidth=2, label='temps')
    ax2.tick_params(axis='y', labelcolor='g', labelsize = 12)
    
    plt.title("Erreur et temps de calcul en fonction du pas", fontsize=24)
    fig.legend(loc='lower left',fontsize=16)
    return 0



# ---------- Question 2.5 ----------

# plot la trajectoire z(x) du rayon pour différents i initiaux entre iMin et iMax
# nbAngles étant le nombre d'angles et donc de rayons différents considérés

def parcoursI():
    plt.figure(figsize=(20, 10))
    ax = plt.gca()                              # Récupère l'axe actuel (Get Current Axis)
    ax.spines['top'].set_color('none')          # cache les bordures du haut et de droite
    ax.spines['right'].set_color('none')
    ax.spines['bottom'].set_position('zero')    # déplace l'axe x et l'axe y à la position 0
    ax.spines['left'].set_position('zero')
    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14)
    plt.title('Graphique de différents rayons en fonction de i0', fontsize=20, fontweight='bold', pad=20)
    plt.xlabel('distance de la source (m)', fontsize=16)
    plt.ylabel('hauteur z du rayon (m)', fontsize=16)

    angle = np.linspace(c.iMin, c.iMax, c.nbRayons)    #avec angles en radians

    for i in angle:
        y0[1] = i
        x, y = sim.trajetRayonEuler(c.Xinterval, y0, c.dx, sim.profilTemperatureLin)
        plt.plot(x, y[0], color = 'skyblue', linewidth = 2)
        
    return 0


# ---------- Quetion 3.1 ----------

# fonction retournant la hauter z du rayon en xf (corrigé de -zf) en fct de i0
# si le rayon est absorbé par le sol, retourne None

def z(i0):
    y0_local = np.array([y0[0], i0])  # prend z0 courant mais sans modifier c.y0
    
    x, y = sim.trajetRayonEuler(c.Xinterval, y0_local, c.dx, sim.profilTemperatureLin)
    if x[-1] < c.Xinterval[1] :
        return None
    return y[0, -1] - c.zf


# fonction visant à déterminer les i0 tel que z(xf) = zf ; retourne les i0 trouvés et une variables de statut
# balaye les images produites par quelques angles pour trouver 2 angles produisant une image de part et d'autre de zf
# utilise ces 2 angles comme conditions initiales pour la recherche de racines
# si argument plot = True alors trace le graphe des particuliers rayons trouver et de quelques autres avec parcoursI()
# les rayons absorbés par le sol (z retourne None) entrainent directement l'iteration suivante de la boucle
# si un seul ou pas de rayons atteint zf alors la fonction retourne des None et statut = -1 ou -2

def imagesMultiples(plot):
    angles = np.linspace(c.iMax, c.iMin, c.nbIbalayage) # de max à min permet d'avoir toujours le rayon direct trouver par bissection dans la première case
    solutions = np.array([None, None])
    j = 0
    
    for k in range(len(angles) -1): # -1 car on a k+1 dans la boucle
        z0 = z(angles[k])
        z1 = z(angles[k+1])
        
        if z0 is None or z1 is None:
            continue
        if z0 * z1 < 0:
            racine, statut = r.bissection(z, angles[k], angles[k+1], c.racineTol)
            if statut == 0:
                solutions[j] = racine
                j += 1
    
    statut = 0
    if plot == True:
        parcoursI()
        for i in solutions:
            if i is None: 
                statut -= 1 
                continue
            if i > 0 : Type = 'direct' ; couleur = 'orange'
            elif i < 0 : Type = 'réfracté'; couleur = 'red'
            
            x, y = sim.trajetRayonEuler(c.Xinterval, [y0[0], i], c.dx, sim.profilTemperatureLin)
            plt.plot(x, y[0], color=couleur, linewidth = 3, label = f"rayon {Type} avec i0 = {round(i*1e3,6)} *10^-3 rad") # i arrondi à 6 décimales pour le plot
            
    if plot == True:
        plt.legend(loc='best', fontsize='16')
    return np.array([solutions[0], solutions[1], statut]) # NB : np.array transforme les None en nan !




# ----- Question 3.2 -----

def distAng (plot):
    statut = 0
    i0Particuliers = imagesMultiples(plot)
    angleArrivée = np.zeros( len(i0Particuliers) -1 )
    
    for i in range( len(i0Particuliers) -1):
        if i0Particuliers[i] is None:
            angleArrivée[i] = None
            statut -= 1
            continue                                    #break marche aussi car si une seule image, elle est dans la 1e case
        x, y = sim.trajetRayonEuler(c.Xinterval, [y0[0], i0Particuliers[i] ], c.dx, sim.profilTemperatureLin)
        angleArrivée[i] = y[1][-1]
    
    distAngu = abs( angleArrivée[0] - angleArrivée[1])
    
    zApparents = np.zeros( len(angleArrivée) )
    j = 0
    Label = "rayons perçu par l'observateur"
    for angle in angleArrivée :
        if angle is None: continue
        m = np.tan(angle)
        p = c.zf - m*c.Xinterval[1]                     # ordonnée à l'origine : z = pente*x + p, en xf on connait zf
        rayonReçu = m * np.array(c.Xinterval) + p       #calcul vectoriel par numpy
        zApparents[j] = p
        j += 1
        if plot == True:
            plt.plot(c.Xinterval, rayonReçu, color='black', linestyle='-.',marker='o', markersize=6, linewidth = 2, label=Label)
            Label = None                                # efface le label pour n'écrire la légende qu'une fois

    if plot == True:
        plt.legend(bbox_to_anchor=(0.05, 1), loc='upper left', fontsize='16') # bbox(x, y) définit la position (% de la taille du graphe)
                                                                              # loc est le pt de la box légende que l'on place à la position définie par bbox
    return np.array( [ [zApparents[0], zApparents[1], statut], [angleArrivée[0], angleArrivée[1], distAngu] ] )




# ----- Question 4 -----
def hauteurToIndice(h, nbLignes, hIm):
    if h >= 0:
        return int( np.round( nbLignes - (h/hIm * nbLignes) ) )
    elif h < 0:
        return int( np.round( nbLignes + ((-h)/hIm * nbLignes) ) )

    
def imageVoiture():
    hIm = c.hauteurImage # hateur de l'image en (m)
    imageArray = img.imread(c.imgFile)
    
    shape = np.shape(imageArray)
    print("taille de l'image : ", shape)
    nbLignes = shape[0]
    nouvelleImage = np.zeros( (nbLignes*2, shape[1], 3) , dtype=np.uint8)  # data type assure des valeures entière pour [r,g,b] 
                                                                           # impossible de convertir tableau en image si r,g,b sont réels
    for l in range(nbLignes):
        z0 = hIm/nbLignes * l
        y0[0] = z0
        print(y0)
        
        z1, z2 = distAng(False)[0, :2]
        print(z1,'\t', z2, '\n')
        
        if np.isnan(z1) or np.isnan(z2):
            continue
        
        i1 = hauteurToIndice(z1, nbLignes, hIm)
        nouvelleImage[i1] = imageArray[nbLignes - l -1]
        
        i2 = hauteurToIndice(z2, nbLignes, hIm)
        nouvelleImage[i2] = imageArray[nbLignes - l -1]
        
    derniere_ligne = 0                                  # trouve la dernière ligne qui n'est pas entièrement noire
    for i in range(nouvelleImage.shape[0]):
        if not np.all(nouvelleImage[i] == 0):
            derniere_ligne = i
    nouvelleImage = nouvelleImage[:derniere_ligne + 1]  # tronque après la dernière ligne non noire
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8), dpi=150)
    ax1.imshow(imageArray)
    ax1.set_title('Image originale', fontsize=18, pad=15)
    ax1.axis('off')

    ax2.imshow(nouvelleImage)
    ax2.set_title("Image perçue par l'observateur", fontsize=18, pad=15)
    ax2.axis('off')
    
    ax1.set_aspect('equal')  # force les deux images à la même hauteur d'affichage
    ax2.set_aspect('equal')
    plt.tight_layout()
    return 0
