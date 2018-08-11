import matplotlib.pyplot as plt
import numpy as np
import json
import csv
from collections import OrderedDict
from operator import itemgetter
from matplotlib.widgets import Button
import re
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import math
import io
from collections import Counter
from os import path
from matplotlib.text import Annotation
from wordcloud import WordCloud

fig = plt.figure()

scatterplot = fig.add_subplot(2,2,2)
wordplot = fig.add_subplot(2,2,4)

with open('apple_store.json') as f1:
    data = json.load(f1)

fieldnames = ("id", "track_name", "size_bytes", "app_desc")
description_data = []
with open('description.csv', 'r') as csvfile:
    #python's standard dict is not guaranteeing any order,
    #but if you write into an OrderedDict, order of write operations will be kept in output.
    reader = csv.DictReader(csvfile, fieldnames)
    for row in reader:
        entry = {}
        for field in fieldnames:
            entry[field] = row[field]
        description_data.append(entry)

description_data.pop(0)
countAppDict = {}
appDict = {}

def getDescription(app):
    for app_w_description in description_data:
        if str(app_w_description['id']) == str(app['id']):
            app['description'] = app_w_description['app_desc']
            break
    return app

for app in data:
    app = getDescription(app)
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
    # button = Button(ax, "")

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

np.random.seed(19680801)
def draw_subplots(genre_data):
    #scatter plot
    x = []
    y = []
    area = []
    N = len(genre_data)
    colors = np.random.rand(N)

    for app in genre_data:
        def getRandomXinRange(user_rating):
            u = user_rating*500
            v = (np.random.randint(u,u+150))/500
            return v
        def getRandomYinRange(price):
            u = price*500
            v = (np.random.randint(u,u+150))/500
            return v
        x.append(getRandomXinRange(app['user_rating']))
        y.append(getRandomYinRange(app['price']))
        area.append(app['rating_count_tot']/1000)

    scatterplot.scatter(x, y, s=area, c=colors, alpha=0.5, picker=True)

    #word cloud
    d = path.dirname(__file__)

    open('description_genre.txt', 'w').close()
    f = open("description_genre.txt", "w")

    for app in genre_data:
        if 'description' in app:
            f.write(app['description'])

    text = io.open(path.join(d, 'description_genre.txt')).read()
    font_path = path.join(d, 'Symbola.ttf')
    word_cloud = WordCloud(font_path=font_path).generate(text)
    wordplot.imshow(word_cloud)
    wordplot.axis("off")

    plt.draw()

genre_data = appDict['Games']
draw_subplots(genre_data)
def onclick(event):
    for i in range(len(axes)):
        ax = axes[i]
        if event.inaxes == ax:
            scatterplot.cla()
            wordplot.cla()
            genre = countAppDict[i]
            print(genre[0])
            genre_data = appDict[genre[0]]
            draw_subplots(genre_data)
            break

def annotate(axis, text, x, y):
    text_annotation = Annotation(text, xy=(x, y), xycoords='data')
    axis.add_artist(text_annotation)

def onpick(event):
    # step 1: take the index of the dot which was picked
    ind = event.ind

    # step 2: save the actual coordinates of the click, so we can position the text label properly
    label_pos_x = event.mouseevent.xdata
    label_pos_y = event.mouseevent.ydata

    # just in case two dots are very close, this offset will help the labels not appear one on top of each other
    offset = 0

    # if the dots are to close one to another, a list of dots clicked is returned by the matplotlib library
    for i in ind:
        # step 3: take the label for the corresponding instance of the data
        app = genre_data[i]
        print(app)
        label = "App: " + app['track_name'] + "\n" + "Rating: " + str(app['user_rating']) + "\n" + "Rating count: " + str(app['rating_count_tot']) + "\n" + "Price: " + str(app['price'])

        # step 4: log it for debugging purposes
        print ("index", i, label)

        # step 5: create and add the text annotation to the scatterplot
        annotate(
            scatterplot,
            label,
            label_pos_x + offset,
            label_pos_y + offset
        )

        # step 6: force re-draw
        scatterplot.figure.canvas.draw_idle()

        # alter the offset just in case there are more than one dots affected by the click
        offset += 0.01

fig.canvas.mpl_connect('button_press_event', onclick)
fig.canvas.mpl_connect('pick_event', onpick)

plt.show()
plt.draw()
