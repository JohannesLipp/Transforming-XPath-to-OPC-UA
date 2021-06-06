import matplotlib.pyplot as plt
from pylab import *
import numpy as np




colorBlind =  ['#377eb8', '#ff7f00', '#4daf4a', '#f781bf', '#a65628', '#984ea3', '#999999', '#e41a1c', '#dede00']

# following # i=84, i=86, ns=5;s=StaticData, i=2253, i=112
# OPC mit offlineList
xf = np.array([0,1,1256,1512,1539])
yf = np.array([1.174,1.249,1.232,1.363,1.592])
# OPC Zugriff auf Server
x2f = np.array([0,1,1256,1512,1539])
y2f = np.array([1.089,1.018,5.173,6.048,11.604])
# OPC Zugriff auf Server LocalCombined
x3f = np.array([0,1,1256,1512,1539])
y3f = np.array([1.023,1.030,2.786,3.015,3.470])
# #XQuery
x4f = np.array([0,1,1256,1512,1539]) # Anzahl der Knoten normiert
y4f = np.array([0.029,0.03,0.044,0.033,0.540])
# #onlineLocalAndererPC OPC Network
x5f = np.array([0,1,1256,1512,1539]) # Anzahl der Knoten normiert
y5f = np.array([0.971,1.198,14.601,19.333,33.008])
# #NetworkCombined
x6f = np.array([0,1,1256,1512,1539]) # Anzahl der Knoten normiert
y6f = np.array([1.068,1.091,7.429,9.282,8.817])

# #remote
x7f = np.array([0,1,1256,1512,1539]) # Anzahl der Knoten normiert
y7f = np.array([1.232,1.243,130.275,140.882,273.169])
# #remoteCombined
x8f = np.array([0,1,1256,1512,1539]) # Anzahl der Knoten normiert
y8f = np.array([0.995,0.967,55.189,73.281,68.447])

xlowlimit = -50
xuplimit = 2000
ylowlimit = -1.5
yuplimit = 45

fig, ax1 = plt.subplots()
plt.grid(True)


ax1.set_title('following')
ax1.set_xlabel('extrahierte Knoten')
ax1.set_ylabel('Laufzeit in Sekunden')
#ax1.tick_params(axis='y', labelcolor=colorBlind[0])

plt.xlim([xlowlimit, xuplimit])
plt.ylim([ylowlimit, yuplimit])

lns1 = ax1.plot(xf, yf, 'o:',color=colorBlind[0], markersize=6,label='UA offline',markeredgecolor="black")
lns3 = ax1.plot(x2f, y2f, 'o--',color=colorBlind[0], markersize=6,label='UA client',markeredgecolor="black",alpha=0.875)
lns4 = ax1.plot(x3f, y3f, 'o-.',color=colorBlind[0], markersize=6,label='UA client\nkombiniert',markeredgecolor="black",alpha=0.5)
lns5 = ax1.plot(x4f, y4f, 'd:',color=colorBlind[1], markersize=6,label='XQuery',markeredgecolor="black")
lns6 = ax1.plot(x5f, y5f, '^--',color=colorBlind[7], markersize=6,label='UA lokal',markeredgecolor="black")
lns7 = ax1.plot(x6f, y6f, '^-.',color=colorBlind[7], markersize=6,label='UA lokal\nkombiniert',markeredgecolor="black",alpha=0.5)




# zweite y-Achse
ax2 = ax1.twinx()
#lns2 = ax2.plot(durchlaeufe,times, '--',label='Laufzeit',color=colorBlind[5])
lns2 = ax2.plot(x7f, y7f, 'P--',color=colorBlind[5], markersize=6,label='UA remote',markeredgecolor="black")
lns8 = ax2.plot(x8f, y8f, 'P-.',color=colorBlind[5], markersize=6,label='UA remote\nkombiniert',markeredgecolor="black",alpha=0.5)
ax2.set_ylabel('UA remote Laufzeit in Sekunden ',color=colorBlind[5])
ax2.tick_params(axis='y', labelcolor=colorBlind[5])


leg = lns5 + lns1 + lns3+ lns4+ lns6+ lns7+ lns2 +lns8
labs = [l.get_label() for l in leg]
ax1.legend(leg, labs, loc=2,markerscale=0.9,fontsize="small",handlelength=6)


fig.tight_layout()  # otherwise the right y-label is slightly clipped
plt.show()
#plt.savefig("D:\\Downloads\\\OPC UA\\plots\\following.pdf",bbox_inches='tight')
# plt.savefig("D:\\Downloads\\\OPC UA\\plots\\following.png",bbox_inches='tight', dpi=300)
