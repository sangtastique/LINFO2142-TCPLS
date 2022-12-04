import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib import rc

rc('text', usetex=False)

# data = np.genfromtxt("../measurements/simple_tour_s1.txt",delimiter=' ', skip_header=2, dtype=float)
data = pd.read_csv("../measurements/simple_file_tour_concat.txt",sep=' ', skiprows=1)

mean_goodput = data.groupby('file_size[MB]')['goodput'].median()

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

plt.ylabel(r"$\mathrm{Goodput} [Mbits/sec]$",fontsize=20)

plt.xlabel(r"$\mathrm{Transfert size} [MBytes]$",fontsize=20)
plt.xticks(mean_goodput.index)

plt.scatter(data["file_size[MB]"],data["goodput"])
plt.scatter(mean_goodput.index, mean_goodput.values)
plt.plot(mean_goodput.index,mean_goodput.values, "-k")
# plt.tight_layout()
plt.show()