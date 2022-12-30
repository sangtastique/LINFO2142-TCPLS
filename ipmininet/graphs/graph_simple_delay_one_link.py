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

filename = "simple_link_different_delay_tour.txt"

measurements_path = os.path.join(os.path.dirname(os.path.realpath(os.path.dirname(__file__))), "measurements", filename)
data = pd.read_csv(measurements_path,sep=' ', skiprows=1)

val_max_delay = 200
data['goodput'] = data['goodput']/data['bw']
group = data.loc[data["delay"] <= val_max_delay].groupby('delay')

mean_goodput = group['goodput'].median()

to_box = group['goodput'].apply(np.hstack).to_numpy()

# group.boxplot( subplots=False, column="goodput")

# plt.xticks(np.array(data.groupby('max_bw').groups.keys()))

# plt.show()

# print(data.head())
# print(data.groupby('max_bw')['goodput'].mean())
# file_sizes = data["max_bw"].unique().to_numpy()
# means = np.zeros(len(file_sizes))

# print(np.mean([8.6649,6.0107,9.1454,9.3912,9.3680]))

# means = pd.DataFrame(file_sizes, columns=["max_bw","mean"])
# # means = np.array((len(file_sizes)))
# means.head()

# print(data.loc[data["max_bw"]==4])
# print(data["max_bw"].unique())

# exit()

fig = plt.figure(figsize=(8,4.5))
ax = fig.add_subplot(1,1,1)

# plt.ylabel(r"$\mathrm{Goodput} [Mbits/sec]$",fontsize=20)
# plt.xlabel(r"$\mathrm{Transfert size} [MBytes]$",fontsize=20)
plt.ylabel("Link utilization [/]",fontsize=16)
plt.xlabel("Link delay [ms]",fontsize=16)
plt.xticks(mean_goodput.index)
plt.xlim(3, val_max_delay + 3)
# plt.yticks(np.arange(1,11,1))
plt.grid(True, color='gray', alpha=0.2, linestyle='-', linewidth=0.3)


# x = np.linspace(5,val_max_bw,5)
# y = x
# max_link = plt.plot(x,y, color = 'r', linestyle = '--', linewidth=0.5, label="Max. link bandwidth")
max_link = plt.axhline(y = 1, color = 'grey', linestyle = '--', linewidth=0.5, label="Max. link bandwidth")

bp = plt.boxplot(to_box, positions=mean_goodput.index, widths=2, sym="+", medianprops=dict(linewidth=1.3, color="g"))

# plt.legend([max_link, bp['medians'][0]], ["Max. link bandwidth", "Medians"], fancybox=False, framealpha=0.5)
plt.legend([ bp['medians'][0]], [ "Medians"], fancybox=False, framealpha=0.5)
# plt.scatter(data["max_bw"],data["goodput"])
# plt.scatter(mean_goodput.index, mean_goodput.values)
# plt.plot(mean_goodput.index,mean_goodput.values, "-k")
# plt.tight_layout()
fig.tight_layout()
plt.show()

# top=0.987,
# bottom=0.128,
# left=0.109,
# right=0.991,
# hspace=0.2,
# wspace=0.2
