import numpy as np

#constantes
h =0.5                      # m
ns = 1.000272983820855
Ts = 303.15
Th = 288.15                 # K (15°C)
def profilTemperatureLin(z):        #tableau ressort T(z), dT/dz
    if z < 0:
        return 1, 0
    elif 0 <= z < h:
        return (Th - Ts)/h *z + Ts, (Th - Ts)/h # T(z) = -15/h=0.5 *z +30
    else:
        return Th, 0


def odefunction(x, y, profilTemperature):
    z = y[0]
    i = y[1]
    T, dTdz = profilTemperature(z)
    
    dy = np.zeros(2)
    dy[0] = np.tan(i)
    dy[1] = -(ns - 1)*Ts/T**2 * dTdz * 1/ (1+(ns -1)*Ts/T)
    return dy



def trajetRayonEuler(interval, y0, dx, profilTemperature):
    y = [ [y0[0]], [y0[1]] ]
    x = [interval[0]]
    
    while x[-1] <= interval[1]:
        yc = [y[0][-1], y[1][-1]]   #valeurs courantes de y:  [z, i]
        dy = odefunction(x[-1], yc, profilTemperature)
        
        znext = y[0][-1] + dx*dy[0]
        if znext <= 0:
            print('le rayon rentre dans le sol')
            break
        inext = y[1][-1] + dx*dy[1]
        y[0].append(znext) #ajout des nouvelles vals de z et i
        y[1].append(inext)
        x.append(x[-1]+dx) #ajout toute dernière val + le pas
    
    return [x, y]



from scipy.integrate import solve_ivp as ode45
def crash(t, y):
    return y[0]
crash.terminal = True

def  trajetRayonIVP(interval, y0, rtol, profilTemperature):
    
    sol = ode45(lambda x,y: odefunction(x, y, profilTemperature), interval, y0, rtol=rtol, events=crash)
    return [sol.t, sol.y]


#faire trajetrayon avec dx entre 10 et 1e-4
#comparer z (et i?) en x = 1000m entre eurel et ivp (faire différence pour calculer l'erreur)
#tracer graphe de l'erreur


import matplotlib.pyplot as plt
plt.figure(figsize=(15, 10))
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)

nb_angle = 50
angle = np.linspace(0.1*np.pi/180, -1*np.pi/180, nb_angle)    #avec angles en radians
interval = [0, 1000]
y0 = [1, 0]
dx = 1                 #///////////////////////////
for i in angle:
    y0[1] = i
    rslt = trajetRayonEuler(interval, y0, dx, profilTemperatureLin)
    plt.plot(rslt[0], rslt[1][0], linewidth = 2)