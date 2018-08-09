import matplotlib.pyplot as plt
import numpy as np
import json
from operator import itemgetter

fig = plt.figure()

textplot = fig.add_subplot(1,2,1)
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
count = 0
gap = 1/num_genre
for app in countAppDict:
    count = count + 1
    textplot.text(0, 1-count*gap,
            app[0] + str(app[1]),
            horizontalalignment='left',
            verticalalignment='top',
            transform = textplot.transAxes)



# textplot.axis('off')
textplot.axes.get_xaxis().set_visible(False)
textplot.axes.get_yaxis().set_visible(False)

plt.show()
