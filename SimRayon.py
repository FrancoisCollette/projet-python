import numpy as np

#constantes
h =0.5                      # m
ns = 1.000272983820855
Tsol = 303.15
Th = 288.15                 # K (15°C)
def profilTemperatureLin(z):                            # ressort tableau T(z), dT/dz
    if z < 0:
        return Tsol, 0
    elif 0 <= z < h:
        return (Th - Tsol)/h *z + Tsol, (Th - Tsol)/h   # pente => (Th - Ts)/h 
    else:
        return Th, 0


def odefunction(x, y, profilTemperature):
    z = y[0]
    i = y[1]
    T, dTdz = profilTemperature(z)
    
    dy = np.zeros(2)
    dy[0] = np.tan(i)
    dy[1] = (((1 - ns)*Tsol/T**2) * dTdz) * (1/ (1+(ns -1)*Tsol/T))
    return dy



def trajetRayonEuler(interval, y0, dx, profilTemperature):
    x0, xf = interval
    
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
            print('le rayon rentre dans le sol')
            return [ x[: j+1], y[:, :j+1] ]         # une case de moins (car la case next n'est pas remplie)
        
        y[0, j +1] = znext
        y[1, j +1] = inext
    
    return [ x[: j+2] , y[:, :j+2] ]                # +2 car +1 borne supérieure ignorée et +1 pour prendre dernière case



from scipy.integrate import solve_ivp as ode45

def  trajetRayonIVP(interval, y0, rtol, profilTemperature):
    
    sol = ode45(lambda x,y: odefunction(x, y, profilTemperature), interval, y0, atol=rtol, rtol=rtol)
    return [sol.t, sol.y]