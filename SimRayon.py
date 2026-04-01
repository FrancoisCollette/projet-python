import numpy as np
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
        T = (Th - Tsol)/h *z + Tsol
        dTdz = (Th - Tsol)/h 
        return [ T, dTdz ]  # pente => (Th - Ts)/h 
    elif z >= h:
        return [ Th, 0 ]


def profilTempLinTrilpeImg(z):
    if z < 0:
        return [Tsol, 0]
    elif z < h:
        T = (Th - Tsol)/h * z + Tsol
        dTdz = (Th - Tsol)/h
        return [T, dTdz]
    elif z < c.h2:
        return [Th, 0]
    elif z < c.h3:
        T = (c.Th3 - c.Th2)/(c.h3 - c.h2) * (z - c.h2) + c.Th2
        dTdz = (c.Th3 - c.Th2)/(c.h3 - c.h2)
        return [T, dTdz]
    else:
        return [c.Th3, 0]
'''
zs = np.linspace(0, 2, 100)
ts = np.zeros(100)
j = 0
for z in zs:
    ts[j] = profilTempLinTrilpeImg(z)[0]
    j += 1
print(ts)'''
    
def odefunction(x, y, profilTemperature):
    z = y[0]
    i = y[1]
    T, dTdz = profilTemperature(z)
    
    n = 1+(ns -1) *Ts/T
    dn = (1 - ns)*Ts*dTdz /T**2
    
    dy = np.zeros(2)
    dy[0] = np.tan(i)
    dy[1] = dn * (1/ n)
    return dy



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