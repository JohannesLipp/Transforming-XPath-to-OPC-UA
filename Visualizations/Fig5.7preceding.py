import matplotlib.pyplot as plt
from pylab import *
import numpy as np

colorBlind =  ['#377eb8', '#ff7f00', '#4daf4a', '#f781bf', '#a65628', '#984ea3', '#999999', '#e41a1c', '#dede00']

# Preceding # i=84, i=2253, ns=5;s=StaticData, i=86, i=112
# OPC mit offlineList
x = np.array([0,0,569,779,1905])
y = np.array([1.092,1.148,1.179,1.292,1.665])
# OPC Zugriff auf Server
x2 = np.array([0,0,569,779,1905])
y2 = np.array([1.075,0.934,3.110,3.804,12.963])
# OPC Zugriff auf Server LocalCombined
x3 = np.array([0,0,569,779,1905])
y3 = np.array([0.907,1.001,1.836,2.089,3.706])
# #XQuery
x4 = np.array([0,0,569,779,1905]) # Anzahl der Knoten normiert
y4 = np.array([0.029,0.033,0.044,0.045,0.710])
# #onlineLocalAndererPC OPC Network
x5 = np.array([0,0,569,779,1905]) # Anzahl der Knoten normiert
y5 = np.array([1.129,1.061,7.315,10.953,40.724])
# #NetworkCombined
x6 = np.array([0,0,569,779,1905]) # Anzahl der Knoten normiert
y6 = np.array([0.997,0.900,3.870,4.676,11.395])

# #remote
x7 = np.array([0,0,569,779,1905]) # Anzahl der Knoten normiert
y7 = np.array([1.137,1.594,58.992,78.377,316.305])
# #remoteCombined
x8 = np.array([0,0,569,779,1905]) # Anzahl der Knoten normiert
y8 = np.array([0.949,0.896,28.419,39.409,94.157])
# i=84, i=2253, ns=5;s=StaticData, i=86, i=112

xlowlimit = -50
xuplimit = 2000
ylowlimit = -1.5
yuplimit = 45

fig, ax1 = plt.subplots()
plt.grid(True)


ax1.set_title('preceding')
ax1.set_xlabel('extrahierte Knoten')
ax1.set_ylabel('Laufzeit in Sekunden')
#ax1.tick_params(axis='y', labelcolor=colorBlind[0])

plt.xlim([xlowlimit, xuplimit])
plt.ylim([ylowlimit, yuplimit])

lns1 = ax1.plot(x, y, 'o:',color=colorBlind[0], markersize=6,label='UA offline',markeredgecolor="black")
lns3 = ax1.plot(x2, y2, 'o--',color=colorBlind[0], markersize=6,label='UA client',markeredgecolor="black",alpha=0.875)
lns4 = ax1.plot(x3, y3, 'o-.',color=colorBlind[0], markersize=6,label='UA client\nkombiniert',markeredgecolor="black",alpha=0.5)
lns5 = ax1.plot(x4, y4, 'd:',color=colorBlind[1], markersize=6,label='XQuery',markeredgecolor="black")
lns6 = ax1.plot(x5, y5, '^--',color=colorBlind[7], markersize=6,label='UA lokal',markeredgecolor="black")
lns7 = ax1.plot(x6, y6, '^-.',color=colorBlind[7], markersize=6,label='UA lokal\nkombiniert',markeredgecolor="black",alpha=0.5)



# zweite y-Achse
ax2 = ax1.twinx()
#lns2 = ax2.plot(durchlaeufe,times, '--',label='Laufzeit',color=colorBlind[5])
lns2 = ax2.plot(x7, y7, 'P--',color=colorBlind[5], markersize=6,label='UA remote',markeredgecolor="black")
lns8 = ax2.plot(x8, y8, 'P-.',color=colorBlind[5], markersize=6,label='UA remote\nkombiniert',markeredgecolor="black",alpha=0.5)
ax2.set_ylabel('UA remote Laufzeit in Sekunden ',color=colorBlind[5])
ax2.tick_params(axis='y', labelcolor=colorBlind[5])

leg = lns5 + lns1 + lns3+ lns4+ lns6+ lns7+ lns2 +lns8
labs = [l.get_label() for l in leg]
ax1.legend(leg, labs, loc=2,markerscale=0.9,fontsize="small",handlelength=6)






fig.tight_layout()  # otherwise the right y-label is slightly clipped
plt.show()
#plt.savefig("D:\\Downloads\\\OPC UA\\plots\\preceding.pdf",bbox_inches='tight')
# plt.savefig("D:\\Downloads\\\OPC UA\\plots\\preceding.png",bbox_inches='tight', dpi=300)
