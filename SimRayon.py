import numpy as np

#constantes
h =0.5                      # m
ns = 1.000272983820855
Ts = 303.15
Th = 288.15                 # K (15°C)
def profilTemperatureLin(z):        # ressort tableau T(z), dT/dz
    if z < 0:
        return 1, 0
    elif 0 <= z < h:
        return (Th - Ts)/h *z + Ts, (Th - Ts)/h # pente => (Th - Ts)/h 
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
        yc = [y[0][-1], y[1][-1]]   # valeurs courantes de y:  [z, i]
        dy = odefunction(x[-1], yc, profilTemperature)
        
        znext = y[0][-1] + dx*dy[0]
        if znext <= 0:
            print('le rayon rentre dans le sol')
            break
        inext = y[1][-1] + dx*dy[1]
        y[0].append(znext) # ajout des nouvelles vals de z et i
        y[1].append(inext)
        x.append(x[-1]+dx) # ajout toute dernière val + le pas
    
    return [x, y]



from scipy.integrate import solve_ivp as ode45
def crash(t, y):
    return y[0]
crash.terminal = True

def  trajetRayonIVP(interval, y0, rtol, profilTemperature):
    
    sol = ode45(lambda x,y: odefunction(x, y, profilTemperature), interval, y0, rtol=rtol, events=crash)
    return [sol.t, sol.y]



import matplotlib.pyplot as plt
plt.figure(figsize=(15, 10))
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)
plt.title('Graphique des erreurs en fonction du pas', fontsize=20)
plt.xlabel('taille du pas (m) (échelle logarithmique)', fontsize=16)
plt.ylabel('erreur (m)', fontsize=16)

#faire trajetrayon avec dx entre 10 et 1e-4
#comparer z (et i?) en x = 1000m entre euler et ivp (faire différence pour calculer l'erreur)
#tracer graphe de l'erreur
dist = [0, 1000]
y0 = [1, -0.2*np.pi/180]
rtol = 1e-10
solIVP = trajetRayonIVP(dist, y0, rtol, profilTemperatureLin)
zIVP = solIVP[1][0][-1]
print('solution par IVP : ', zIVP)
print('les erreurs en fonction du pas sont :')

pas = [10, 5, 1, 0.5, 0.1, 5e-2, 1e-2, 1e-3, 1e-4]
erreurTab = []
for dx in pas:
    solEuler = trajetRayonEuler(dist, y0, dx, profilTemperatureLin)
    zEuler = solEuler[1][0][-1]
    erreur = abs(zEuler - zIVP)
    erreurTab.append(erreur)
    print(erreur)

plt.plot(pas, erreurTab, linewidth = 2)
plt.xscale('log')
plt.xlim(10, 1e-4)



plt.figure(figsize=(15, 10))
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)
plt.title('Graphique de différents rayons en fonction de i0', fontsize=20)
plt.xlabel('distance de la source (m)', fontsize=16)
plt.ylabel('hauteur z du rayon (m)', fontsize=16)

nb_angle = 50
angle = np.linspace(0.1*np.pi/180, -1*np.pi/180, nb_angle)    #avec angles en radians
interval = [0, 1000]
y0 = [1, 0]
dx = 1e-2                 #///////////////////////////  1e-2 s'accompagne d'une erreur de ~1 cm
for i in angle:
    y0[1] = i
    rslt = trajetRayonEuler(interval, y0, dx, profilTemperatureLin)
    plt.plot(rslt[0], rslt[1][0], linewidth = 2)
    
