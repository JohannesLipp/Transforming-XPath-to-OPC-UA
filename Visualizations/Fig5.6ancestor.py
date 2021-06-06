
import matplotlib.pyplot as plt
from pylab import *
import numpy as np




colorBlind =  ['#377eb8', '#ff7f00', '#4daf4a', '#f781bf', '#a65628', '#984ea3', '#999999', '#e41a1c', '#dede00']

# ancestor # i=84, i=86, ns=5;s=StaticData, i=2253, i=112
# OPC mit offlineList
xa = np.array([0,1,2,2,292])
ya = np.array([1.117,1.103,1.137,1.143,1.213])
# OPC Zugriff auf Server
x2a = np.array([0,1,2,2,292])
y2a = np.array([1.087,1.060,1.030,1.065,5.273])
# OPC Zugriff auf Server LocalCombined
x3a = np.array([0,1,2,2,292])
y3a = np.array([1.111,1.013,1.000,0.927,1.526])
# #XQuery
x4a = np.array([0,1,2,2,292]) # Anzahl der Knoten normiert
y4a = np.array([0.029,0.028,0.029,0.029,0.045])
# #onlineLocalAndererPC OPC Network
x5a = np.array([0,1,2,2,292]) # Anzahl der Knoten normiert
y5a = np.array([1.030,1.016,1.125,1.018,12.789])
# #NetworkCombined
x6a = np.array([0,1,2,2,292]) # Anzahl der Knoten normiert
y6a = np.array([1.033,1.159,0.982,1.010,2.832])

# remote online
x7a = np.array([0,1,2,2,292]) # Anzahl der Knoten normiert
y7a = np.array([1.212,1.133,1.424,1.064,103.518])
# remote combined
x8a = np.array([0,1,2,2,292]) # Anzahl der Knoten normiert
y8a = np.array([0.989,0.974,1.035,1.179,16.972])

xlowlimit = -50
xuplimit = 2000
ylowlimit = -1.5
yuplimit = 45







fig, ax1 = plt.subplots()
plt.grid(True)

ax1.set_title('ancestor')
ax1.set_xlabel('extrahierte Knoten')
ax1.set_ylabel('Laufzeit in Sekunden')
#ax1.tick_params(axis='y', labelcolor=colorBlind[0])

plt.xlim([xlowlimit, xuplimit])
plt.ylim([ylowlimit, yuplimit])

lns1 = ax1.plot(xa, ya, 'o:',color=colorBlind[0], markersize=6,label='UA offline',markeredgecolor="black")
lns3 = ax1.plot(x2a, y2a, 'o--',color=colorBlind[0], markersize=6,label='UA client',markeredgecolor="black",alpha=0.875)
lns4 = ax1.plot(x3a, y3a, 'o-.',color=colorBlind[0], markersize=6,label='UA client\nkombiniert',markeredgecolor="black",alpha=0.5)
lns5 = ax1.plot(x4a, y4a, 'd:',color=colorBlind[1], markersize=6,label='XQuery',markeredgecolor="black")
lns6 = ax1.plot(x5a, y5a, '^--',color=colorBlind[7], markersize=6,label='UA lokal',markeredgecolor="black")
lns7 = ax1.plot(x6a, y6a, '^-.',color=colorBlind[7], markersize=6,label='UA lokal\nkombiniert',markeredgecolor="black",alpha=0.5)




# zweite y-Achse
ax2 = ax1.twinx()
#lns2 = ax2.plot(durchlaeufe,times, '--',label='Laufzeit',color=colorBlind[5])
lns2 = ax2.plot(x7a, y7a, 'P--',color=colorBlind[5], markersize=6,label='UA remote',markeredgecolor="black")
lns8 = ax2.plot(x8a, y8a, 'P-.',color=colorBlind[5], markersize=6,label='UA remote\nkombiniert',markeredgecolor="black",alpha=0.5)
ax2.set_ylabel('UA remote Laufzeit in Sekunden ',color=colorBlind[5])
ax2.tick_params(axis='y', labelcolor=colorBlind[5])
#scale_x = 1000000


leg = lns1 + lns3+ lns4+ lns5+ lns6+ lns7+ lns2 +lns8
labs = [l.get_label() for l in leg]
ax1.legend(leg, labs, loc=1,markerscale=0.9,fontsize="small",handlelength=6)

# plt.title('Pfadberechnung ohne blockierte Knoten')

fig.tight_layout()  # otherwise the right y-label is slightly clipped
plt.show()
#plt.savefig("D:\\Downloads\\\OPC UA\\plots\\ancestor.pdf",bbox_inches='tight')
# plt.savefig("D:\\Downloads\\\OPC UA\\plots\\ancestor.png",bbox_inches='tight', dpi=300)

