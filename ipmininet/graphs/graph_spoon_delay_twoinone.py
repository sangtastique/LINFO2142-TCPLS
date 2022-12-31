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
filename2 = "spoon_double_ratiodelay_topchange_tour.txt"

top_delay = 35
max_total_bw = 10

measurements_path = os.path.join(os.path.dirname(os.path.realpath(os.path.dirname(__file__))), "measurements", filename)
measurements2_path = os.path.join(os.path.dirname(os.path.realpath(os.path.dirname(__file__))), "measurements", filename2)
data = pd.read_csv(measurements_path, sep=' ', skiprows=1)
data2 = pd.read_csv(measurements2_path, sep=' ', skiprows=1)

data['goodput'] = data['goodput']/max_total_bw
data['ratio'] = (data['ratio'] * top_delay).astype('int')
group = data.groupby('ratio')

mean_goodput = group['goodput'].median()

to_box = group['goodput'].apply(np.hstack).to_numpy()

data2['goodput'] = data2['goodput']/max_total_bw
data2['ratio'] = (data2['ratio'] * top_delay).astype('int')
group2 = data2.groupby('ratio')

mean_goodput2 = group2['goodput'].median()

to_box2 = group2['goodput'].apply(np.hstack).to_numpy()

fig = plt.figure(figsize=(8,4.5))
ax = fig.add_subplot(1,1,1)

plt.ylabel("Combined utilization [/]",fontsize=16)
plt.xlabel("Link delay [ms]",fontsize=16)
plt.grid(True, color='gray', alpha=0.2, linestyle='-', linewidth=0.3)

max_2_link = plt.axhline(y = 1, color = 'grey', linestyle = '--', linewidth=0.5, label="Max. bandwidth (2 links)")
max_link = plt.axhline(y = 0.5, color = 'g', linestyle = '--', linewidth=0.5, label="Max. bandwidth (one link)")

bp = plt.boxplot(to_box, positions=mean_goodput.index -1.125, widths=1.75, sym="+", patch_artist=True, boxprops=dict(color="k", facecolor="white"), medianprops=dict(linewidth=1.3, color="r"))

bp2 = plt.boxplot(to_box2, positions=mean_goodput2.index + 1.125, widths=1.75, sym="+", patch_artist=True, boxprops=dict(color="k", facecolor=[0/255,92/255,173/255,0.5]), medianprops=dict(linewidth=1.3, color="orange"))

plt.xticks(ticks=mean_goodput.index, labels=mean_goodput.index)
plt.xlim(data["ratio"].min() - 3, data["ratio"].max() + 3)
ax.tick_params(labelsize=13)

plt.title("TCPLS' goodput link utilization vs. primary and secondary link delay\non spoon topology", fontsize=18)

plt.legend([bp['boxes'][0], bp2['boxes'][0], bp['medians'][0], bp2['medians'][0], max_2_link, max_link], [ "Primary path fixed","Secondary path fixed", "Medians for primary p.", "Medians for secondary p.", "Max. utilization of both paths", "Max. utilization of a single path"], ncol=3, fancybox=False, framealpha=0.8)

fig.tight_layout()
plt.subplots_adjust(top=0.878, bottom=0.132, left=0.079, right=0.996)
plt.show()