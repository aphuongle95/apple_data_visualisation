import matplotlib.pyplot as plt
import numpy as np
import json
from operator import itemgetter
from matplotlib.widgets import Button
from mpl_toolkits.axes_grid.inset_locator import inset_axes
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import math

fig = plt.figure()

# fig = plt.figure(figsize=(10, 8))

scatterplot = fig.add_subplot(2,2,2)
wordplot = fig.add_subplot(2,2,4)

with open('apple_store.json') as f:
    data = json.load(f)

countAppDict = {}
appDict = {}

for app in data:
    genre = app['prime_genre']
    if genre in countAppDict:
        count = countAppDict[genre]
        count = count + 1
        countAppDict[genre] = count
        apps = appDict[genre]
        apps.append(app)
        appDict[genre] = apps
    else:
        countAppDict[genre] = 1
        appDict[genre] = [app]


countAppDict = sorted(countAppDict.items(), key=itemgetter(1), reverse=True)
print(countAppDict)

num_genre = len(countAppDict)
grid_col = math.ceil(num_genre/2)
outer = gridspec.GridSpec(grid_col, 2, wspace=0, hspace=0)

range_num = []
for x in range(grid_col):
   range_num.append(x*2)

axes = []
for i in tuple(range_num):
    inner = gridspec.GridSpecFromSubplotSpec(2, 1,
                    subplot_spec=outer[i], wspace=0, hspace=0)
    for j in range(2):
        ax = plt.Subplot(fig, inner[j])
        # t = ax.text(0.5,0.5, 'outer=%d, inner=%d' % (i,j))
        # t.set_ha('center')
        ax.set_xticks([])
        ax.set_yticks([])
        axes.append(ax)
        fig.add_subplot(ax)

count = 0
# gap = 1/num_genre
for app in countAppDict:
    ax = axes[count]
    count = count + 1
    button = Button(ax, "")
    # def next(self, event):
    #     self.ind += 1
    #     i = self.ind % len(freqs)
    #     ydata = np.sin(2*np.pi*freqs[i]*t)
    #     l.set_ydata(ydata)
    #     plt.draw()
    # button.on_clicked(callback.next)

    ax.text(0.1, 0.9,
            app[0],
            horizontalalignment='left',
            verticalalignment='top',
            transform = ax.transAxes)

    ax.text(0.9, 0.9,
            str(app[1]),
            horizontalalignment='right',
            verticalalignment='top',
            transform = ax.transAxes)



# textplot.axis('off')
# textplot.axes.get_xaxis().set_visible(False)
# textplot.axes.get_yaxis().set_visible(False)

plt.show()
