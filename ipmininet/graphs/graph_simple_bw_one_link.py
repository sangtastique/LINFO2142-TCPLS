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

filename = "simple_bw_tour.txt"
# filename = "simple_link_different_bw_tour_2.txt"

measurements_path = os.path.join(os.path.dirname(os.path.realpath(os.path.dirname(__file__))), "measurements", filename)
data = pd.read_csv(measurements_path,sep=' ', skiprows=1)

val_max_bw = 101
data['goodput'] = data['goodput']/data['max_bw']
group = data.loc[data["max_bw"] < val_max_bw].groupby('max_bw')

mean_goodput = group['goodput'].median()

to_box = group['goodput'].apply(np.hstack).to_numpy()

fig = plt.figure(figsize=(8,4.5))
ax = fig.add_subplot(1,1,1)

plt.ylabel("Link utilization [/]",fontsize=16)
plt.xlabel("Total available bandwidth [Mb/sec]",fontsize=16)
plt.xticks(mean_goodput.index)
plt.xlim(3, val_max_bw + 3)
plt.grid(True, color='gray', alpha=0.2, linestyle='-', linewidth=0.3)
ax.tick_params(labelsize=13)
plt.title("TCPLS' goodput link utilization vs. link bandwidth on simple topology", fontsize=18)

max_link = plt.axhline(y = 1, color = 'grey', linestyle = '--', linewidth=0.5, label="Max. link utilization")

bp = plt.boxplot(to_box, positions=mean_goodput.index, widths=2, sym="+", medianprops=dict(linewidth=1.3, color="r"))

plt.legend([ bp['medians'][0], max_link], [ "Medians", "Max. link utilization"], fancybox=False, framealpha=0.5)
fig.tight_layout()
plt.show()
