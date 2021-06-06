import matplotlib.pyplot as plt
import numpy as np
from matplotlib.lines import Line2D
from matplotlib.legend_handler import HandlerTuple

fig, ax = plt.subplots()


#fig.subplots_adjust(right=0.75)

#twin1 = ax.twinx()
#twin2 = ax.twinx()

# Offset the right spine of twin2.  The ticks and label have already been
# placed on the right by twinx above.
#twin2.spines.right.set_position(("axes", 1.2))

x = np.array(["Gesamt","Blockiert","Indirekt\nbockiert","Im\nXML-Abbild"])
colorBlind =  ['#377eb8', '#ff7f00', '#4daf4a', '#f781bf', '#a65628', '#984ea3', '#999999', '#e41a1c', '#dede00']
scenes = np.arange(len(x))
width = 0.25

# p1, = ax.plot(x, [4329,116,2243,1970], "d:",color=colorBlind[7], label="Anzahl der Knoten",markeredgecolor="black")
# ax.plot(x, [4329,116,2243,1970], "d:",color=colorBlind[7], label="Anzahl der Knoten",markeredgecolor="black")
# p2, = twin1.plot(x, [2.406,5.603,2.575,2.025], "o--",color=colorBlind[0], label="Nachfolgerknoten pro Knoten",markeredgecolor="black")
# p3, = twin1.plot(x, [2.42,31.672,1.036,2.274], "^--",color=colorBlind[0], label="Vorgängerknoten pro Knoten",markeredgecolor="black")
# p1 = ax.bar(scenes, [4329,116,2243,1970], width, color=colorBlind[7], label="Anzahl der Knoten")
p2 = ax.bar(scenes+0.25, [2.42,31.67,1.03,2.27], width ,color=colorBlind[5], label="Anzahl der\nVorgängerknoten")
p3 = ax.bar(scenes, [2.40,5.60,2.57,2.02], width ,color=colorBlind[0], label="Anzahl der\nNachfolgeknoten")
plt.ylim([0, 50])
ax.set_xlabel("Szenario")
ax.set_ylabel("Vorgänger-/Nachfolgeknoten pro Knoten")

ax2=ax.twinx()
# ax2.grid(True)

p1 = ax2.bar(scenes-0.25, [4329,116,2243,1970], width, color=colorBlind[7], label="Anzahl der\nUrsprungsknoten")
ax2.set_ylabel("Anzahl der betrachteten Ursprungsknoten",color=colorBlind[7])
ax2.tick_params(axis='y', labelcolor=colorBlind[7])
#twin1.set_ylim(-0.7, 35)
#ax2.set_ylim(0, 50000)

ax.grid()
ax.set_axisbelow(True)

ax.set_xticks(scenes)
ax.set_xticklabels(x)
#ax.legend()
h1, l1 = ax.get_legend_handles_labels()
h2, l2 = ax2.get_legend_handles_labels()
ax.legend(h1+h2, l1+l2)
plt.ylim([0, 5000])
ax2.bar_label(p1, padding=3)
ax.bar_label(p2, padding=3)
ax.bar_label(p3, padding=3)


plt.title('Auswirkungen der Blockierung von Knoten')
fig.tight_layout()

plt.show()
#plt.savefig("D:\\Downloads\\\OPC UA\\plots\\blockedNodes.pdf",bbox_inches='tight')