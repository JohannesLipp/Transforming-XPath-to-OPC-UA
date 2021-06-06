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

x = np.array(["IKV XQuery","IKV offline","IKV kombiniert","IKV online"])
colorBlind =  ['#377eb8', '#ff7f00', '#4daf4a', '#f781bf', '#a65628', '#984ea3', '#999999', '#e41a1c', '#dede00']
scenes = np.arange(len(x))
width = 0.25

p3 = ax.bar(scenes, [0.053, 0.506, 18.643, 47.744], width ,color=colorBlind[2], label="Durchschnittliche Laufzeit\ndes Ausdrucks")
plt.ylim([0, 53])
ax.set_xlabel("Szenario")
ax.set_ylabel("Laufzeit in Sekunden")


ax.grid()
ax.set_axisbelow(True)

ax.set_xticks(scenes)
ax.set_xticklabels(x)

ax.legend(loc='best')

ax.bar_label(p3, padding=3,fontsize=12)


plt.title('Laufzeit des IKV-Ausdrucks')
fig.tight_layout()

plt.show()
#plt.savefig("D:\\Downloads\\\OPC UA\\plots\\IKVAusdruck.pdf",bbox_inches='tight')
#plt.savefig("D:\\Downloads\\\OPC UA\\plots\\IKVAusdruck.png",bbox_inches='tight', dpi=300)