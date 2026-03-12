# ----- Fichier contenant l'ensemble des constantes et conditions particulières utilisées -----
import numpy as np

ns = 1.000272983820855      # constante de Gladstone
ps = 1e5                    # pression standard
Ts = 288.15                 # t° standard
Tsol = 30 + 273.15          # (K)
h = 0.5                     # hauteur limite entre t° constante et t° linéaire dans profilTemperature (m)
Th = 15 + 273.15            # (K)



# ----- conditions sur l'EDO -----

Xinterval = [0, 1000]       # bornes de l'intervalle de resolution  (m)
y0 = [1, 0 *np.pi/180]      # conditions initiales [z0, i0]         (m , rad)
dx = 0.1                    # pas pour la résolution par Euler      (m)
IVPtol = 1e-10              # tolérance (rtol et atol) pour IVP


# ----- Questions 2 & 3 -----
y0Tol = [1, -0.25 *np.pi/180]
dxTab = np.logspace(1, -3, 10) # tableau des différents dx à tester (attention logspace prend des puissances de 10 en argument)
nbRayons = 50               # nombre de rayons à tracer en Q2.5
zf = 1.5                    # hauteur de l'observateur                 (m)
iMin = -0.5 *np.pi/180      # angle min de l'interval de i pour Q2.5   (rad)
iMax = 0.1 *np.pi/180       # idem max                                 (rad)

nbIbalayage = 15            # nombre d'angles pour le balayage cherchant les bornes d'appel à bissection
racineTol = 1e-6            # tolérance sur la recherche de racines    (m)
