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

filename = "simple_link_different_bw_tour.txt"
# filename = "simple_link_different_bw_tour_2.txt"
filename_tcp = "simple_link_different_bw_tcp_tour.txt"

val_max_bw = 101

measurements_path = os.path.join(os.path.dirname(os.path.realpath(os.path.dirname(__file__))), "measurements", filename)
data = pd.read_csv(measurements_path,sep=' ', skiprows=1)

data['goodput'] = data['goodput']/data['max_bw']
group = data.loc[data["max_bw"] < val_max_bw].groupby('max_bw')

mean_goodput = group['goodput'].median()

to_box = group['goodput'].apply(np.hstack).to_numpy()

measurements_path_tcp = os.path.join(os.path.dirname(os.path.realpath(os.path.dirname(__file__))), "measurements", filename_tcp)
data_tcp = pd.read_csv(measurements_path_tcp, sep=' ', skiprows=1)

data_tcp['goodput'] = data_tcp['goodput']/data['max_bw']
group_tcp = data_tcp.loc[data_tcp["max_bw"] < val_max_bw].groupby('max_bw')

mean_goodput_tcp = group_tcp['goodput'].median()

to_box_tcp = group_tcp['goodput'].apply(np.hstack).to_numpy()


fig = plt.figure(figsize=(8,4.5))
ax = fig.add_subplot(1,1,1)

plt.ylabel("Link utilization [/]",fontsize=16)
plt.xlabel("Total available bandwidth [Mb/sec]",fontsize=16)

plt.grid(True, color='gray', alpha=0.2, linestyle='-', linewidth=0.3)
ax.tick_params(labelsize=13)
plt.title("Goodput link utilization vs. link bandwidth on simple topology", fontsize=18)

max_link = plt.axhline(y = 1, color = 'grey', linestyle = '--', linewidth=0.5, label="Max. link utilization")

bp = plt.boxplot(to_box, positions=mean_goodput.index - 0.8, widths=1, sym="+", patch_artist=True, flierprops={'marker': '+', 'markersize': 5}, boxprops=dict(color="k", facecolor="white"),medianprops=dict(linewidth=1.3, color="r"))

bp_tcp = plt.boxplot(to_box_tcp, positions=mean_goodput.index + 0.8, widths=1, sym="x", patch_artist=True, flierprops={'marker': 'x', 'markersize': 4.5}, boxprops=dict(color="k", facecolor=[27/255,166/255,29/255,0.5]), medianprops=dict(linewidth=1.3, color="orange"))

plt.xticks(mean_goodput.index, mean_goodput.index)
plt.xlim(3, val_max_bw + 2)
plt.legend([bp['boxes'][0], bp_tcp['boxes'][0], bp['medians'][0], max_link], [ r"TCPLS (\small\texttt{rapido})", r"TCP (\small\texttt{iperf3})", "Medians", "Max. link utilization"], ncol=2, fancybox=False, framealpha=0.5)
fig.tight_layout()
plt.subplots_adjust(top=0.925, bottom=0.132, left=0.079, right=0.991)
plt.show()

