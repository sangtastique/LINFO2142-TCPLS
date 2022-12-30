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

filename = "spoon_double_ratiodelay_topchange_tour.txt"

top_delay = 35
max_total_bw = 10

measurements_path = os.path.join(os.path.dirname(os.path.realpath(os.path.dirname(__file__))), "measurements", filename)
data = pd.read_csv(measurements_path, sep=' ', skiprows=1)

data['goodput'] = data['goodput']/max_total_bw
data['ratio'] = (data['ratio'] * top_delay).astype('int')
group = data.groupby('ratio')

mean_goodput = group['goodput'].median()

to_box = group['goodput'].apply(np.hstack).to_numpy()

fig = plt.figure(figsize=(8,4.5))
ax = fig.add_subplot(1,1,1)

plt.ylabel("Combined utilization [/]",fontsize=16)
plt.xlabel("Primary link delay [ms]",fontsize=16)
plt.grid(True, color='gray', alpha=0.2, linestyle='-', linewidth=0.3)

plt.xlim(data["ratio"].min() - 3, data["ratio"].max() + 3)
ax.tick_params(labelsize=13)

max_2_link = plt.axhline(y = 1, color = 'grey', linestyle = '--', linewidth=0.5, label="Max. bandwidth (2 links)")
max_link = plt.axhline(y = 0.5, color = 'g', linestyle = '--', linewidth=0.5, label="Max. bandwidth (one link)")

bp = plt.boxplot(to_box, positions=mean_goodput.index, widths=1, sym="+", medianprops=dict(linewidth=1.3, color="r"))

plt.title("TCPLS' goodput link utilization vs. first advertised link delay", fontsize=18)

plt.legend([bp['medians'][0], max_2_link, max_link], [ "Medians", "Max. utilization of both links", "Max. utilization of a single link"], fancybox=False, framealpha=0.5)

fig.tight_layout()
plt.show()