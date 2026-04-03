import numpy as np
import time
import matplotlib.pyplot as plt
import RechercheRacine as r
import SimRayon as sim
import matplotlib.image as img
import constantes as c


# ---------- Question 2.4 ----------

# définit la valeur correcte comme z en xf par IVP
# cacule z en xf par Euler pour chaque dx ainsi que le temps de calcul nécessaire à Euler
# erreur commise comme différence des 2 solutions (IVP et Euler) trouvées
# plot un graphique de l'erreur et du temps de calcul en fonction du pas

def tolerance():
    solIVP = sim.trajetRayonIVP(c.Xinterval, c.y0Tol, c.IVPtol, sim.profilTemperatureLin)
    zIVP = solIVP[1][0][-1]             #prendre toute dernière val de z dans y[]
    print('solution par IVP : ', zIVP)
    print('les erreurs en x= 1000m en fonction du pas sont :')
    
    errTab = np.zeros( len(c.dxTab) )
    tempsTab = np.zeros( len(c.dxTab) )
    i = 0
    for pas in c.dxTab:
        t0 = time.perf_counter()        # donne l'heure précise pour calculer le temps pris pas Euler
        solEuler = sim.trajetRayonEuler(c.Xinterval, c.y0Tol, pas, sim.profilTemperatureLin)
        tf = time.perf_counter()
        
        zEuler = solEuler[1][0][-1]
        erreur = abs(zEuler - zIVP)
        errTab[i] = erreur
        tempsTab[i] = tf - t0
        i += 1
        print(erreur)
    
    plt.figure(figsize=(15, 10))
    plt.loglog(c.dxTab, errTab, 'ob-', linewidth=2, label='erreur')
    plt.xlabel('taille du pas (m)', fontsize=24)
    plt.ylabel('erreur (m)', fontsize=24,)
    plt.xlim(np.max(c.dxTab), np.min(c.dxTab)) # retourne l'axe pour avoir grand pas à gauche et petits à droite
    plt.tick_params(labelsize = 20)
    plt.savefig('erreur.pdf', bbox_inches='tight')
    
    plt.figure(figsize=(15,10))
    plt.xlabel('taille du pas (m)', fontsize=24)
    plt.loglog(c.dxTab, tempsTab, 'og-', linewidth=2, label='temps')
    plt.ylabel('temps de calcul (s)', fontsize=24)
    plt.xlim(np.max(c.dxTab), np.min(c.dxTab))
    plt.tick_params(labelsize = 20)
    plt.savefig('temps.pdf', bbox_inches='tight')

    '''
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
    fig.legend(loc='lower left',fontsize=16)'''
    return 0



# ---------- Question 2.5 ----------

# plot la trajectoire z(x) du rayon pour différents i initiaux entre iMin et iMax
# si le rayon rentre dans le sol, il est plot en rouge, en vert sinon
# nbAngles étant le nombre d'angles et donc de rayons différents considérés

def parcoursI(profilTemp = sim.profilTemperatureLin):
    angle = np.linspace(c.iMin, c.iMax, c.nbRayons)
    
    plt.figure(figsize=(15, 10))
    plt.xlabel('distance depuis la source (m)', fontsize=24)
    plt.ylabel('hauteur du rayon (m)', fontsize=24)
    plt.tick_params(labelsize = 20)
    for i in angle:
        c.y0[1] = i
        x, y = sim.trajetRayonEuler(c.Xinterval, c.y0, c.dx, profilTemp)
        if x[-1] < 1000 :
            plt.plot(x, y[0], color = 'red', linewidth = 1)
            
        else : plt.plot(x, y[0], color = 'green', linewidth = 1)
    plt.grid()
    plt.savefig('balayage_angles.pdf', bbox_inches='tight')
    return 0


# ---------- Quetion 3.1 ----------

# fonction retournant la hauter z du rayon en xf (corrigé de -zf) en fct de i0
# si le rayon est absorbé par le sol, retourne None

def z(i0, profilTemp = sim.profilTemperatureLin):
    y0Local = np.array([c.y0[0], i0])  # prend z0 courant mais sans modifier c.y0
    
    x, y = sim.trajetRayonEuler(c.Xinterval, y0Local, c.dx, profilTemp)
    if x[-1] < c.Xinterval[1] :
        return None
    return y[0, -1] - c.zf


# fonction visant à déterminer les i0 tel que z(xf) = zf ; retourne les i0 trouvés et une variables de statut
# balaye les images produites par quelques angles pour trouver 2 angles produisant une image de part et d'autre de zf
# utilise ces 2 angles comme conditions initiales pour la recherche de racines
# si argument plot = True alors trace le graphe des particuliers rayons trouver et de quelques autres avec parcoursI()
# les rayons absorbés par le sol (z retourne None) entrainent directement l'iteration suivante de la boucle
# si un seul ou pas de rayons atteint zf alors la fonction retourne des None et statut = -1 ou -2

def imagesMultiples(plot=False, profilTemp = sim.profilTemperatureLin):
    angles = np.linspace(c.iMax, c.iMin, c.nbIbalayage) # de max à min permet d'avoir toujours le rayon direct trouver par bissection dans la première case
    solutions = np.array([None, None])
    j = 0
    
    for k in range(len(angles) -1): # -1 car on a k+1 dans la boucle
        z0 = z(angles[k], profilTemp)
        z1 = z(angles[k+1], profilTemp)
        
        if z0 is None or z1 is None:
            continue
        if z0 * z1 < 0:
            racine, statut = r.bissection(z, angles[k], angles[k+1], c.racineTol)
            if statut == 0:
                solutions[j] = racine
                j += 1
    
    statut = 0
    if plot == True:
        #parcoursI(profilTemp)
        plt.figure(figsize=(15, 10))
        for i in solutions:
            if i is None: 
                statut -= 1 
                continue
            if i > 0 : Type = 'direct' ; couleur = 'lightblue'
            elif i < 0 : Type = 'réfracté'; couleur = 'blue'
            
            x, y = sim.trajetRayonEuler(c.Xinterval, [c.y0[0], i], c.dx, profilTemp)
            plt.plot(x, y[0], color=couleur, linewidth = 2, label = f"rayon {Type}")
            
    if plot == True:
        plt.xlabel('distance depuis la source (m)', fontsize=24)
        plt.ylabel('hauteur du rayon (m)', fontsize=24)
        plt.tick_params(labelsize = 20)
        plt.legend(loc='best', fontsize='24')
        plt.grid()
        plt.savefig('images_multpiles.pdf', bbox_inches='tight')
    return np.array([solutions[0], solutions[1], statut]) # NB : np.array transforme les None en nan !




# ----- Question 3.2 -----

# fonction appelant imagesMultiples() pour connaitre les i0 tel que z(xf) = zf
# apelle trajetRayonEuler() avec ces i0 pour déterminer i en xf et calculer la distance angulaire entre les 2 rayons reçus
# trace la droite représentant le rayon perçu par l'observateur de pente = tan(i)
# et détermine la hauteur en x = 0 du rayon tel que vu par l'observateur
# ressort un tableau 2x3 contenant [ hauteur1 , hauteur2, statut] , [i1, i2, distance angulaire]

def distAng (plot, profilTemp = sim.profilTemperatureLin):
    statut = 0
    i0Particuliers = imagesMultiples(plot, profilTemp)
    angleArrivée = np.zeros( len(i0Particuliers) -1 )
    
    for i in range( len(i0Particuliers) -1):
        if i0Particuliers[i] is None:
            angleArrivée[i] = None
            statut -= 1
            continue                                    #break marche aussi car si une seule image, elle est dans la 1e case
        x, y = sim.trajetRayonEuler(c.Xinterval, [c.y0[0], i0Particuliers[i] ], c.dx, profilTemp)
        angleArrivée[i] = y[1][-1]
    
    distAngu = abs( angleArrivée[0] - angleArrivée[1])
    
    zApparents = np.zeros( len(angleArrivée) )
    j = 0
    Label = "images perçues par l'observateur"
    for angle in angleArrivée :
        if angle is None: continue
        m = np.tan(angle)
        p = c.zf - m*c.Xinterval[1]                     # ordonnée à l'origine : z = pente*x + p, en xf on connait zf
        rayonReçu = m * np.array(c.Xinterval) + p       #calcul vectoriel par numpy
        zApparents[j] = p
        j += 1
        if plot == True:
            plt.plot(c.Xinterval, rayonReçu, color='black', linestyle='--',marker='o', markersize=4, linewidth = 2, label=Label)
            Label = None                                # efface le label pour n'écrire la légende qu'une fois

    if plot == True:
        plt.legend(loc='lower right', fontsize='24')
        plt.tick_params(labelsize = 20)
        plt.savefig('projections_rayons_perçus.pdf', bbox_inches='tight')
                                                                             
    return np.array( [ [zApparents[0], zApparents[1], statut], [angleArrivée[0], angleArrivée[1], distAngu] ] )




# ----- Question 4 -----

# Fonction prennant un profil de température comme argument otpionnel, la valeur par défault est sim.profilTemperatureLin
# Crée un tableau de taille lignesNouvelleImage x largeur initiale de l'image avec lignesNouvelleImage définie dans le module Constantes
# Pour chaque ligne appelle Euler à l'envers (xf -> 0m) pour déterminé 
# la hauteur initiale du rayon et copier les pixels de l'image dans le nouveau tableau
# Termine par afficher l'image vue par l'observateur ainsi qu'un graphe 
# de la hauteur perçue par l'observateur en fonction de la hauteur réelle de la source
def imageBacktracing(profilTemp = sim.profilTemperatureLin):
    hIm = c.hauteurImage
    hImObs = c.bornesImageObs
    imageArray = img.imread(c.imgFile)
    shape = np.shape(imageArray)
    nbLignes = shape[0]
    nouvelleImageLong = c.lignesNouvelleImage
    nouvelleImage = np.zeros((nouvelleImageLong, shape[1], 3), dtype=np.uint8)
    xf = c.Xinterval[1]

    z_sources_direct, z_apps_direct, z_sources_refracte, z_apps_refracte = [], [], [], []
    print('Calcul en cours, cela peut prendre un instant...')
    z_apps_balayage = np.linspace(hImObs[0], hImObs[1], nouvelleImageLong) # tab des hauteurs apparentes pour l'observateur entre hImObs[0] et [1]
    l =0
    for l, z_app in enumerate(z_apps_balayage):

        angle_arrivee = np.arctan((c.zf - z_app) / xf)
        
        y0_inverse = np.array([c.zf, angle_arrivee])          # intègre le rayon à l'envers depuis (xf, zf) vers x=0
        x, y = sim.trajetRayonEuler([xf, 0], y0_inverse, -c.dx, profilTemp)

        if x[-1] > 0:             # rayon absorbé avant d'atteindre x=0
            continue
        z_source = y[0, -1]       # hauteur à x=0 => ligne sur la voiture
        if z_source < 0 or z_source > hIm:
            continue
            
        if abs(angle_arrivee - y[1, -1]) <= 1e-6:  # compare les angles pour savoir si réfracté 
            z_sources_direct.append(z_source)      # car hors du gradiant, le rayon va en ligne droite
            z_apps_direct.append(z_app)
        else:
            z_sources_refracte.append(z_source)
            z_apps_refracte.append(z_app)

        ligne_source = int(np.round( nbLignes - (z_source/hIm * nbLignes) )) # convertit z_source en ligne dans l'image originale
        nouvelleImage[l] = imageArray[ligne_source]

    
    plt.imshow(nouvelleImage, extent=[0, 3, -6, 6])
    print("suppression des extrémités non visibles de l'image ...")
    j=0
    while( np.all(nouvelleImage[0] == 0) ):         # tronque bande noire de dessus, démarre du haut et supprime chaque bande trouvée jusqu'a ce qu'il y ait de la couleur
        nouvelleImage = nouvelleImage[1 :]
        j +=1
    zmax = z_apps_balayage[j]                       # z_app de la première ligne non noire
      
    derniere_ligne = 0                              # tronque bande noire du dessous, on supprime la fin du tab à pt de la 1er ligne noire
    for i in range(np.shape(nouvelleImage)[0]):
        if not np.all(nouvelleImage[i] == 0):
            derniere_ligne = i
    nouvelleImage = nouvelleImage[:derniere_ligne + 1]
    zmin = z_apps_balayage[j + derniere_ligne]      # z_app de la dernière ligne non noire
    
    print('100% - terminé! \n')
    print("L'image s'étant de", zmax, 'm à', zmin,'m')
    plt.figure()
    plt.imshow(imageArray, extent=[0, 3, 0, hIm], aspect='auto')
    plt.xlabel("largeur (m)", fontsize=14)
    plt.ylabel("altitude (m)", fontsize=14)
    plt.savefig('image_originaleBis.pdf', dpi=600, bbox_inches='tight' )

    plt.figure()
    plt.imshow(nouvelleImage, extent=[0, 3, zmin, zmax])
    graduations = np.arange(np.ceil(zmin * 2) / 2, np.floor(zmax * 2) / 2 + 0.5, 0.5)
    graduations = np.concatenate([[zmin], graduations, [zmax]])
    graduations = np.unique(np.round(graduations, 3))
    plt.yticks(graduations)
    plt.xlabel("largeur (m)", fontsize=14)
    plt.ylabel("altitude (m)", fontsize=14)
    plt.savefig('image_modifiéeBis.pdf', dpi=600, bbox_inches='tight')
    
    plt.figure(figsize=(10, 15))
    plt.plot(z_sources_direct,   z_apps_direct,   'b', linewidth=2, label='rayons directs')
    plt.plot(z_sources_refracte, z_apps_refracte, 'r', linewidth=2, label='rayons réfractés')
    plt.xlabel('position réelle de la source (m)', fontsize=24)
    plt.ylabel("position perçue par l'observateur (m)", fontsize=24)
    plt.tick_params(labelsize = 20)
    plt.legend(loc='best', fontsize=24)
    plt.grid(True)
    plt.savefig('graphePositionsVerticalesBis.pdf', dpi=300)
    return 0


# ---- Question bonus -----

# fonction d'aide à la visualisation du phénomène
def T(profilTemp = sim.profilTemperatureLin):
    ztab = np.linspace(0, c.bornesImageObs[0], 100)
    Ttab = np.zeros(100)
    j = 0
    for z in ztab:
        Ttab[j] = profilTemp(z)[0]
        j +=1
    plt.figure(figsize=(20, 5))
    plt.plot(ztab, Ttab, linewidth=2)
    plt.xlabel("altitude (m)", fontsize=24)
    plt.ylabel("température (K)", fontsize=24)
    plt.tick_params(labelsize = 20)
