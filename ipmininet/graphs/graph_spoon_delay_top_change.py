import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib import rc
import os

# Use LaTeX rendering (requires installing MiKTeX on windpws + ghostscript)
# Makes the rendering slower tho
plt.rc('text', usetex=True)
# Use LaTeX's default 'Computer Modern' font for labels as well
plt.rc('font', family='serif')

filename = "spoon_double_ratiodelay_tour.txt"

top_delay = 35
max_total_bw = 10

measurements_path = os.path.join(os.path.dirname(os.path.realpath(os.path.dirname(__file__))), "measurements", filename)
data = pd.read_csv(measurements_path, sep=' ', skiprows=1)

data['goodput'] = data['goodput']/max_total_bw
data['ratio'] = (data['ratio'] * top_delay).astype('int')
group = data.groupby('ratio')

mean_goodput = group['goodput'].median()

to_box = group['goodput'].apply(np.hstack).to_numpy()
# to_box2 = group['utilization'].apply(np.hstack).to_numpy()

fig = plt.figure(figsize=(8,4.5))
ax = fig.add_subplot(1,1,1)

# plt.ylabel(r"$\mathrm{Goodput} [Mbits/sec]$",fontsize=20)
# plt.xlabel(r"$\mathrm{Transfert size} [MBytes]$",fontsize=20)
plt.ylabel("Combined utilization [/]",fontsize=16)
plt.xlabel("Secondary link delay [ms]",fontsize=16)
# plt.xticks(mean_goodput.index)
# plt.xticks(np.arange(0,1.01,0.1), labels=['0/100', '10/90', '20/80', '30/70', '40/60', '50/50', '60/40', '70/30', '80/20', '90/10', '100/0'])
# ax.set_xticklabels(['0/100', '10/90', '20/80', '30/70', '40/60', '50/50', '60/40', '70/30', '80/20', '90/10', '100/0'])
plt.grid(True, color='gray', alpha=0.2, linestyle='-', linewidth=0.3)


max_link = plt.axhline(y = 1, color = 'grey', linestyle = '--', linewidth=0.5, label="Max. link bandwidth")

bp = plt.boxplot(to_box, positions=mean_goodput.index, widths=1, sym="+", medianprops=dict(linewidth=1.3, color="g"))

# plt.xticks(mean_goodput.index, labels=['0/100', '10/90', '20/80', '30/70', '40/60', '50/50', '60/40', '70/30', '80/20', '90/10', '100/0'], rotation=25)

# for i in mean_goodput.index:
#     minx = i-0.05
#     maxx = i+0.05
#     max_link = plt.axhline(y = max_total_bw*max(i, 1-i), xmin=minx, xmax=maxx, color = 'r', linestyle = '--', linewidth=0.5, label="Max. link bandwidth")

# plt.legend([max_link, bp['medians'][0]], ["Max. summed link bandwidth", "Medians"], fancybox=False)
plt.legend([bp['medians'][0]], [ "Medians"], fancybox=False)
plt.xlim(data["ratio"].min() - 3, data["ratio"].max() + 3)
fig.tight_layout()
plt.show()

#top=0.985,
# bottom=0.15,
# left=0.11,
# right=0.985,
# hspace=0.2,
# wspace=0.2