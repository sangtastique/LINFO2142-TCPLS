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

filename = "spoon_double_ratio_tour_s1.txt"

measurements_path = os.path.join(os.path.dirname(os.path.realpath(os.path.dirname(__file__))), "measurements", filename)
data = pd.read_csv(measurements_path, sep=' ', skiprows=1)

max_total_bw = 10

# To make older version of graph :
# data.loc[data['ratio'] <= 0.5, 'utilization'] = data['goodput']/(max_total_bw * (1-data['ratio']))
# data.loc[data['ratio'] > 0.5, 'utilization'] = data['goodput']/(max_total_bw * data['ratio'])
# New version uses :
data['utilization'] = data['goodput']/max_total_bw
group = data.groupby('ratio')

mean_goodput = group['goodput'].median()

to_box = group['goodput'].apply(np.hstack).to_numpy()
to_box2 = group['utilization'].apply(np.hstack).to_numpy()

fig = plt.figure(figsize=(8,4.5))
ax = fig.add_subplot(1,1,1)

plt.ylabel("Combined utilization [/]",fontsize=16)
plt.xlabel(r"Link bandwidth allocation between both paths [primary \%/ secondary \%]",fontsize=16)

plt.grid(True, color='gray', alpha=0.2, linestyle='-', linewidth=0.3)

max_link = plt.axhline(y = 1, color = 'grey', linestyle = '--', linewidth=0.5, label="Max. link bandwidth")

bp = plt.boxplot(to_box2, positions=mean_goodput.index, widths=0.05, sym="+", medianprops=dict(linewidth=1.3, color="r"))

scatt = plt.scatter(mean_goodput.index, np.maximum(mean_goodput.index.to_numpy(),1 - mean_goodput.index.to_numpy()), marker="^", color="g")

plt.xlim(-0.05, 1.05)
ax.tick_params(labelsize=13)
plt.xticks(mean_goodput.index, labels=['0/100', '10/90', '20/80', '30/70', '40/60', '50/50', '60/40', '70/30', '80/20', '90/10', '100/0'], rotation=25)

plt.title("TCPLS' goodput combined link utilization vs. bandwidth allocation\nover both paths on spoon topology", fontsize=18)

plt.legend([bp['medians'][0], max_link, scatt], [ "Medians", "Max. utilization", "Max. single path utilization"], fancybox=False, framealpha=0.5)

fig.tight_layout()
plt.subplots_adjust(top=0.873, bottom=0.174, left=0.079, right=0.996)
plt.show()