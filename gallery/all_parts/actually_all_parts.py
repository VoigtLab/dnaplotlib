#import sys
import dnaplotlib as dpl
import matplotlib.pyplot as plt
#import matplotlib.transforms as mtransforms
#import matplotlib.patches as mpatch
#from matplotlib.patches import FancyBboxPatch
import numpy as np

dnaline = 3
dr = dpl.DNARenderer(scale = 5,linewidth=dnaline)
part_renderers = dr.SBOL_part_renderers()
parts = part_renderers.keys()
dontrender = ['StemTop']
fig1 = plt.figure(figsize=(14,14))
faxes = fig1.subplots(ncols=6,nrows=6)
raxes = np.ravel(faxes)
#print(raxes)
raxind = 0
for part in parts:
    if(part in dontrender):
        continue
    ax = raxes[raxind]
    raxind+=1
    #plt.Figure(figsize=(.1,.1))
    #ax = plt.gca()
    design = [{'type':part, 'name':'test', 'fwd':True,\
               'opts':{'label':part,'label_size':13,'label_y_offset':-8,'color':(.5,.5,.2)}},
             {'type':part, 'name':'testr', 'fwd':False,'opts':{'color':(.2,.5,.5)}}]
    start,end = dr.renderDNA(ax,design,part_renderers)
    ax.axis('off')
    xdist = end-start
    delta = xdist*.2
    start-=delta
    end+=delta
    newxdist = end-start
    ax.set_xlim([start,end])

    ax.set_ylim([-newxdist/2,newxdist/2])
plt.savefig("actually_all_parts.png")
