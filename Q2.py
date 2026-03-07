
import numpy as np
import matplotlib.pyplot as plt
import RechercheRacine as r
import SimRayon as sim

solution = sim.trajetRayonIVP([0, 1000], [1, -0.1*np.pi/180], 1e-10, sim.profilTemperatureLin)
if (solution):
    print('IVP ok : ', solution)
    
solution2 = sim.trajetRayonEuler([0, 1000], [1, -0.1*np.pi/180], 0.1, sim.profilTemperatureLin)
if (solution2):
    print('euler ok : ', solution2)
    
plt.figure()
plt.plot(solution[0], solution[1][0])
plt.title("Trajet IVP")
plt.figure()
plt.plot(solution2[0], solution2[1][0])
plt.title("Trajet Euler")




def fct(x):
    return x**3 + x -1

print(r.secante(fct, 1, -0.2, 1e-6))

def cos(x):
    return np.cos(x)

print(r.secante(cos, -1, 2, 1e-6))



# variables initiales et solution à 1000m par ode45
dist = [0, 1000]
y0 = [1, -0.2*np.pi/180]
tolerance = 1e-10
solIVP = sim.trajetRayonIVP(dist, y0, tolerance, sim.profilTemperatureLin)
zIVP = solIVP[1][0][-1] #prendre toute dernière val de z dans y[]
print('solution par IVP : ', zIVP)
print('les erreurs en x= 1000m en fonction du pas sont :')

# tableau des pas et solutions à 1000m par Euler pour chacun
pas = [10, 5, 1, 0.5, 0.1, 5e-2, 1e-2, 5e-3, 1e-3]
erreurTab1 = np.zeros(len(pas))
i = 0
for dx in pas:
    solEuler = sim.trajetRayonEuler(dist, y0, dx, sim.profilTemperatureLin)
    zEuler = solEuler[1][0][-1]
    # erreur commise par Euler comme différence des 2 solutions trouvées
    erreur = abs(zEuler - zIVP)
    erreurTab1[i] = erreur
    i += 1
    print(erreur)


plt.figure(figsize=(15, 10))
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)
plt.title("Graphique des erreurs en 1000m", fontsize=20)
plt.xlabel('taille du pas (m) (échelle logarithmique)', fontsize=16)
plt.ylabel('erreur (m)', fontsize=16)

plt.plot(pas, erreurTab1, linewidth = 2, label='err en x=1000')
plt.xscale('log')
plt.xlim(10, 1e-3) #inverse axe x pour plus de lisibilité !! à adpater en fct du tavbleau des pas !!
plt.legend(loc='best', fontsize='16')

# le fait que l'erreur ne tombe pas en 0 même pour un pas très petit ne signifie pas que Euler est nul
# on a simplement atteint la limite de la plus petite précision que l'on peu avoir, avec euler et ivp,
# les 2 méthodes sont d'accord à 1e-2 près et 1cm pour 1000m c'est très bien!
# cela montre que Euler est très performant pour un pas bien choisi







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
dx = 1e-1                 # 1e- s'accompagne d'une erreur de ~3 cm choix équilibré précision/rapidité
for i in angle:
    y0[1] = i
    rslt = sim.trajetRayonEuler(interval, y0, dx, sim.profilTemperatureLin)
    plt.plot(rslt[0], rslt[1][0], linewidth = 2)