import numpy as np

#constantes
h =0.5                      # m
ns = 1.000272983820855
Ts = 15                     # °C
def profilTemperatureLin(z):
    if z < 0:
        return -1, -1               #tableau ressort T(z), dT/dz
    elif 0 < z < h:
        return -15/h *z + 30, -15/h # T(z) = -15/h=0.5 *z +30
    else:
        return 15, 0

def odefunction(x, y, profilTemperature):
    z = y[0]
    T, dTdz = profilTemperature(z)
    
    dy = np.zero(2)
    dy[0] = np.tan(y[1])
    dy[1] = (ns - 1)*Ts*np.ln(T) * profilTemperature(dTdz) * 1/ 1+(ns -1)*Ts/T
    return dy



