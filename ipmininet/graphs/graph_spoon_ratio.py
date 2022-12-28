import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib import rc

rc('text', usetex=False)

# data = np.genfromtxt("../measurements/simple_tour_s1.txt",delimiter=' ', skip_header=2, dtype=float)
data = pd.read_csv("../measurements/spoon_double_ratio_tour_s1.txt",sep=' ', skiprows=1)
max_total_bw = 10


data.loc[data['ratio'] <= 0.5, 'utilization'] = data['goodput']/(max_total_bw * (1-data['ratio']))
data.loc[data['ratio'] > 0.5, 'utilization'] = data['goodput']/(max_total_bw * data['ratio'])
group = data.groupby('ratio')

mean_goodput = group['goodput'].median()

to_box = group['goodput'].apply(np.hstack).to_numpy()
to_box2 = group['utilization'].apply(np.hstack).to_numpy()

fig = plt.figure(figsize=(8,4.5))
ax = fig.add_subplot(1,1,1)

# plt.ylabel(r"$\mathrm{Goodput} [Mbits/sec]$",fontsize=20)
# plt.xlabel(r"$\mathrm{Transfert size} [MBytes]$",fontsize=20)
plt.ylabel("Goodput to best link\n bandwidth ratio [/]",fontsize=16)
plt.xlabel("Link bandwidth ratio [/]",fontsize=16)
# plt.xticks(mean_goodput.index)
# plt.xticks(np.arange(0,1.01,0.1), labels=['0/100', '10/90', '20/80', '30/70', '40/60', '50/50', '60/40', '70/30', '80/20', '90/10', '100/0'])
# ax.set_xticklabels(['0/100', '10/90', '20/80', '30/70', '40/60', '50/50', '60/40', '70/30', '80/20', '90/10', '100/0'])
plt.grid(True, color='gray', alpha=0.2, linestyle='-', linewidth=0.3)


max_link = plt.axhline(y = 1, color = 'grey', linestyle = '--', linewidth=0.5, label="Max. link bandwidth")

bp = plt.boxplot(to_box2, positions=mean_goodput.index, widths=0.05, sym="+", medianprops=dict(linewidth=1.3, color="g"))

plt.xticks(mean_goodput.index, labels=['0/100', '10/90', '20/80', '30/70', '40/60', '50/50', '60/40', '70/30', '80/20', '90/10', '100/0'], rotation=25)

# for i in mean_goodput.index:
#     minx = i-0.05
#     maxx = i+0.05
#     max_link = plt.axhline(y = max_total_bw*max(i, 1-i), xmin=minx, xmax=maxx, color = 'r', linestyle = '--', linewidth=0.5, label="Max. link bandwidth")

# plt.legend([max_link, bp['medians'][0]], ["Max. summed link bandwidth", "Medians"], fancybox=False)
plt.legend([bp['medians'][0]], [ "Medians"], fancybox=False)
plt.xlim(-0.1, 1.1)
fig.tight_layout()
plt.show()

#top=0.985,
# bottom=0.15,
# left=0.11,
# right=0.985,
# hspace=0.2,
# wspace=0.2