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

filename = "simple_file_tour_concat.txt"

measurements_path = os.path.join(os.path.dirname(os.path.realpath(os.path.dirname(__file__))), "measurements", filename)
data = pd.read_csv(measurements_path, sep=' ', skiprows=1)

group = data.groupby('file_size[MB]')

mean_goodput = group['goodput'].median()

to_box = group['goodput'].apply(np.hstack).to_numpy()

# group.boxplot( subplots=False, column="goodput")

# plt.xticks(np.array(data.groupby('file_size[MB]').groups.keys()))

# plt.show()

# print(data.head())
# print(data.groupby('file_size[MB]')['goodput'].mean())
# file_sizes = data["file_size[MB]"].unique().to_numpy()
# means = np.zeros(len(file_sizes))

# print(np.mean([8.6649,6.0107,9.1454,9.3912,9.3680]))

# means = pd.DataFrame(file_sizes, columns=["file_size[MB]","mean"])
# # means = np.array((len(file_sizes)))
# means.head()

# print(data.loc[data["file_size[MB]"]==4])
# print(data["file_size[MB]"].unique())

# exit()

fig = plt.figure(figsize=(8,4.5))
ax = fig.add_subplot(1,1,1)

# plt.ylabel(r"$\mathrm{Goodput} [Mbits/sec]$",fontsize=20)
# plt.xlabel(r"$\mathrm{Transfert size} [MBytes]$",fontsize=20)
plt.ylabel("Goodput [Mb/sec]",fontsize=16)
plt.xlabel("Transfer size [MB]",fontsize=16)
plt.xticks(mean_goodput.index)
plt.yticks(np.arange(1,11,1))
plt.grid(True, color='gray', alpha=0.2, linestyle='-', linewidth=0.3)

max_link = plt.axhline(y = 10, color = 'r', linestyle = '--', linewidth=0.5, label="Max. link bandwidth")
bp = plt.boxplot(to_box, positions=mean_goodput.index, widths=0.35, sym="+", medianprops=dict(linewidth=1.3, color="g"))

plt.legend([max_link, bp['medians'][0]], ["Max. link bandwidth", "Medians"], fancybox=False)

# plt.scatter(data["file_size[MB]"],data["goodput"])
# plt.scatter(mean_goodput.index, mean_goodput.values)
# plt.plot(mean_goodput.index,mean_goodput.values, "-k")
fig.tight_layout()

plt.show()