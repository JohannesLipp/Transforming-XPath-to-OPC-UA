import matplotlib.pyplot as plt
from pylab import *
import numpy as np




colorBlind =  ['#377eb8', '#ff7f00', '#4daf4a', '#f781bf', '#a65628', '#984ea3', '#999999', '#e41a1c', '#dede00']

# descendant # i=112, ns=5;s=StaticData, i=2253, i=86, i=84
# OPC mit offlineList
# xd = np.array([0,208,549,1205,1969])
# yd = np.array([1.385,1.375,1.065,1.122,1.167])
# # OPC Zugriff auf Server
# x2d = np.array([0,208,549,1205,1969])
# y2d = np.array([7.141,5.193,1.080,3.004,1.859])
# # OPC Zugriff auf Server LocalCombined
# x3d = np.array([0,208,549,1205,1969])
# y3d = np.array([3.562,2.720,0.994,1.864,1.291])
# # #XQuery
# x4d = np.array([0,208,549,1205,1969]) # Anzahl der Knoten normiert
# y4d = np.array([0.041,0.036,0.029,0.032,0.029])
# # #onlineLocalAndererPC OPC Network
# x5d = np.array([0,208,549,1205,1969]) # Anzahl der Knoten normiert
# y5d = np.array([22.949,14.595,1.004,7.329,4.139])
# # #NetworkCombined
# x6d = np.array([0,208,549,1205,1969]) # Anzahl der Knoten normiert
# y6d = np.array([10.583,7.159,1.037,3.929,1.812])
# # #remote
# x7d = np.array([0,208,549,1205,1969]) # Anzahl der Knoten normiert
# y7d = np.array([184.31,117.728,1.031,53.838,20.367])
# # #remoteCombined
# x8d = np.array([0,208,549,1205,1969]) # Anzahl der Knoten normiert
# y8d = np.array([103.756,63.958,0.894,30.91,12.09])
# OPC mit offlineList
xd = np.array([0,208,549,1205,1969])
yd = np.array([1.065,1.167,1.122,1.375,1.385])
# OPC Zugriff auf Server
x2d = np.array([0,208,549,1205,1969])
y2d = np.array([1.080,1.859,3.004,5.193,7.141])
# OPC Zugriff auf Server LocalCombined
x3d = np.array([0,208,549,1205,1969])
y3d = np.array([0.994,1.291,1.864,2.720,3.562])
# #XQuery
x4d = np.array([0,208,549,1205,1969]) # Anzahl der Knoten normiert
y4d = np.array([0.029,0.029,0.032,0.036,0.041])
# #onlineLocalAndererPC OPC Network
x5d = np.array([0,208,549,1205,1969]) # Anzahl der Knoten normiert
y5d = np.array([1.004,4.139,7.329,14.595,22.949])
# #NetworkCombined
x6d = np.array([0,208,549,1205,1969]) # Anzahl der Knoten normiert
y6d = np.array([1.037,1.812,3.929,7.159,10.583])
# #remote
x7d = np.array([0,208,549,1205,1969]) # Anzahl der Knoten normiert
y7d = np.array([1.031,20.367,53.838,117.728,184.31])
# #remoteCombined
x8d = np.array([0,208,549,1205,1969]) # Anzahl der Knoten normiert
y8d = np.array([0.894,12.09,30.91,63.958,103.756])


xlowlimit = -50
xuplimit = 2000
ylowlimit = -1.5
yuplimit = 45

fig, ax1 = plt.subplots()
plt.grid(True)


ax1.set_title('descendant')
ax1.set_xlabel('extrahierte Knoten')
ax1.set_ylabel('Laufzeit in Sekunden')
#ax1.tick_params(axis='y', labelcolor=colorBlind[0])

plt.xlim([xlowlimit, xuplimit])
plt.ylim([ylowlimit, yuplimit])

lns1 = ax1.plot(xd, yd, 'o:',color=colorBlind[0], markersize=6,label='UA offline',markeredgecolor="black")
lns3 = ax1.plot(x2d, y2d, 'o--',color=colorBlind[0], markersize=6,label='UA client',markeredgecolor="black",alpha=0.875)
lns4 = ax1.plot(x3d, y3d, 'o-.',color=colorBlind[0], markersize=6,label='UA client\nkombiniert',markeredgecolor="black",alpha=0.5)
lns5 = ax1.plot(x4d, y4d, 'd:',color=colorBlind[1], markersize=6,label='XQuery',markeredgecolor="black")
lns6 = ax1.plot(x5d, y5d, '^--',color=colorBlind[7], markersize=6,label='UA lokal',markeredgecolor="black")
lns7 = ax1.plot(x6d, y6d, '^-.',color=colorBlind[7], markersize=6,label='UA lokal\nkombiniert',markeredgecolor="black",alpha=0.5)




# zweite y-Achse
ax2 = ax1.twinx()
#lns2 = ax2.plot(durchlaeufe,times, '--',label='Laufzeit',color=colorBlind[5])
lns2 = ax2.plot(x7d, y7d, 'P--',color=colorBlind[5], markersize=6,label='UA remote',markeredgecolor="black")
lns8 = ax2.plot(x8d, y8d, 'P-.',color=colorBlind[5], markersize=6,label='UA remote\nkombiniert',markeredgecolor="black",alpha=0.5)
ax2.set_ylabel('UA remote Laufzeit in Sekunden ',color=colorBlind[5])
ax2.tick_params(axis='y', labelcolor=colorBlind[5])


leg = lns5 + lns1 + lns3+ lns4+ lns6+ lns7+ lns2 +lns8
labs = [l.get_label() for l in leg]
ax1.legend(leg, labs, loc=2,markerscale=0.9,fontsize="small",handlelength=6)


fig.tight_layout()  # otherwise the right y-label is slightly clipped
plt.show()
#plt.savefig("D:\\Downloads\\\OPC UA\\plots\\descendant.pdf",bbox_inches='tight')
# plt.savefig("D:\\Downloads\\\OPC UA\\plots\\descendant.png",bbox_inches='tight', dpi=300)
