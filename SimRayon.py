import numpy as np
import math
import constantes as c
#constantes
h = c.h
ns = c.ns
Ts = c.Ts
Tsol = c.Tsol
Th = c.Th


def profilTemperatureLin(z): # ressort tableau T(z), dT/dz
    if z < 0:
        return [Tsol, 0]
    elif 0 <= z < h:
        dTdz = (Th - Tsol)/h
        T = dTdz *z + Tsol
        return [ T, dTdz ]  # pente => (Th - Ts)/h 
    elif z >= h:
        return [ Th, 0 ]


# ----- pour bonus -----
def profilTripleImg(z):
    h2 = 1.9                      # limite 2e gradient de température     (m)
    h3 = 3.0                      # limite supérieure du 2e gradient      (m)
    Th2 = Th                      # gradient symétrique au 1er
    Th3 = Tsol
    if z < 0:
        return [Tsol, 0]
    elif z < h:
        T = (Th - Tsol)/h * z + Tsol
        dTdz = (Th - Tsol)/h
        return [T, dTdz]
    elif z < h2:
        return [Th, 0]
    elif z < h3:
        dTdz = (Th3 - Th2)/(h3 - h2)
        T = dTdz * (z - h2) + Th2
        return [T, dTdz]
    else:
        return [Th3, 0]
    

def profilMirageSupp(z):

    TsolSupp = 5 + 273.15         # tsol mirage suppérieur : froid au sol (K)
    ThSupp = 35 + 273.15          # chaud dans l'air loin du sol          (K)
    hSupp = 5                     # limite avant t=cst fixée à 5m         (m)
    if z < 0:
        return [TsolSupp, 0]
    elif z < hSupp:
        dTdz = (ThSupp - TsolSupp)/hSupp
        T = dTdz *z + TsolSupp
        return [ T, dTdz ]
    elif z >= h:
        return [ ThSupp, 0 ]
    

def profilComplex(z):
    T0 = 20 + 273.15      # Température moyenne     (K)
    A = 20                # Amplitude               (K)
    L = 0.5               # Épaisseur d'une couche  (m)

    T = T0 + A * np.sin(2 * np.pi * z / L)
    dTdz = A * (2 * np.pi / L) * np.cos(2 * np.pi * z / L)
    return [T, dTdz]


# ----- ----- ----- -----
   

    
def odefunction(x, y, profilTemperature):
    z = y[0]
    i = y[1]
    T, dTdz = profilTemperature(z)
    
    n = 1+(ns -1) *Ts/T
    dn = (1 - ns)*Ts*dTdz /T**2
    
    return [math.tan(i), dn / n]



def trajetRayonEuler(interval, y0, dx, profilTemperature):
    x0, xf = interval
    if x0 == xf:
        print("attention l'interval est mal choisit : x0 = xf")
        return [x0, y0]

    x = np.arange(x0, xf +dx, dx)
    y = np.zeros( (2 ,len(x)) )
    x[0] = x0
    y[:, 0] = y0
    
    for j in range(len(x) -1 ):
        yc = y[:, j]                                # valeurs courantes de y:  [z, i]
        dy = odefunction(x[j], yc, profilTemperature)
        
        znext = y[0, j] + dx*dy[0]
        inext = y[1, j] + dx*dy[1]
        if znext <= 0:
            return [ x[: j+1], y[:, :j+1] ]         # une case de moins (car la case next n'est pas remplie)
        
        y[0, j +1] = znext
        y[1, j +1] = inext
    
    return [ x[: j+2] , y[:, :j+2] ]                # +2 car +1 borne supérieure ignorée et +1 pour prendre dernière case



from scipy.integrate import solve_ivp as ode45
def crash(t, y):
        return y[0]     # = z, s'annule quand le rayon touche le sol

crash.terminal = True   # stoppe l'intégration quand z=0
crash.direction = -1    # stoppe seulement quand z descend vers 0

def  trajetRayonIVP(interval, y0, tol, profilTemperature):
    
    sol = ode45(lambda x,y: odefunction(x, y, profilTemperature), interval, y0, atol=tol, rtol=tol, events=crash)
    return [sol.t, sol.y]