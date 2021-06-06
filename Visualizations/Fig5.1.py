import matplotlib.pyplot as plt
import numpy as np


from matplotlib.lines import Line2D
from matplotlib.legend_handler import HandlerTuple


colorBlind =  ['#377eb8', '#ff7f00', '#4daf4a', '#f781bf', '#a65628', '#984ea3', '#999999', '#e41a1c', '#dede00']


fig, ax1 = plt.subplots()

x2 = np.array(["UA client","UA lokal","UA remote"])
# y3 = np.array([0.0028, 0.0059, 0.0763])
# # lns3 = ax1.plot(x2, y3, 'd--',label='Schnellste',color=colorBlind[0],markeredgecolor="black")
# # ax1.plot(x2, y3, 'd--',label='Schnellste',color=colorBlind[0],markeredgecolor="black")
# ax1.errorbar(x2, y3, yerr=[[0,1,2],[1,2,3]], fmt='o', ecolor='g', capthick=2)

# y4 = np.array([0.2218, 0.6279, 0.5115])
# # lns4 = ax1.plot(x2, y4, '^--',label='Langsamste',color=colorBlind[0],markeredgecolor="black")
# # ax1.plot(x2, y4, '^--',label='Langsamste',color=colorBlind[0],markeredgecolor="black")
# ax1.errorbar(x2, y4, yerr=[[0,1,2],[1,2,3]], fmt='o', ecolor='g', capthick=2)


y2 = np.array([0.0052, 0.0177, 0.13419])
mins=[0.0028, 0.0059, 0.0763]
maxs=[0.2218, 0.6279, 0.5115]
plt.grid(True)
# lns1 = ax1.plot(x2, y2, 'o--',label='Durchschnitt',color=colorBlind[0],markeredgecolor="black")
# ax1.plot(x2, y2, 'o--',label='Durchschnitt',color=colorBlind[0],markeredgecolor="black")
ax1.errorbar(x2, y2, yerr=[[y2[0]-mins[0],y2[1]-mins[1],y2[2]-mins[2]],[maxs[0]-y2[0],maxs[1]-y2[1],maxs[2]-y2[2]]], fmt='o', ecolor=colorBlind[0], capthick=2, capsize=3,markeredgecolor="black",label='Durchschnittliche\nLaufzeit pro Datensatz')

ax1.set_xlabel('Szenario')
ax1.set_ylabel('Extraktionsdauer pro Datensatz in Sekunden',color=colorBlind[0])

ax1.tick_params(axis='y', labelcolor=colorBlind[0])
#ax1.legend(loc=0)
ax1.set_ylim([-.015, 0.7])

ax2 = ax1.twinx()

ax2.set_ylim([-15, 700])
y2nodes= np.array([22.9, 77.1, 581.5])
#lns2 = ax2.plot(x2, y2nodes, 'o--',label='Gesamt',color=colorBlind[7],markeredgecolor="black")
ax2.plot(x2, y2nodes, 'd--',label='Laufzeit gesamt',color=colorBlind[7],markeredgecolor="black")
# ax2.errorbar(x2, y2nodes, yerr=[[0,1,2],[1,2,3]], fmt='o', ecolor='g', capthick=2)
ax2.set_ylabel('Extraktionsdauer in Sekunden',color=colorBlind[7])
ax2.tick_params(axis='y', labelcolor=colorBlind[7])




h1, l1 = ax1.get_legend_handles_labels()
h2, l2 = ax2.get_legend_handles_labels()
ax1.legend(h1+h2, l1+l2, loc=2)

plt.title('Extraktionsdauer des Informationsmodells')

fig.tight_layout()  # otherwise the right y-label is slightly clipped


plt.show()
#plt.savefig("D:\\Downloads\\\OPC UA\\plots\\extraction2.pdf",bbox_inches='tight')