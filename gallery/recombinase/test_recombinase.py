#!/usr/bin/env python
"""
	Short description goes here.
"""

import dnaplotlib as dpl
import matplotlib.pyplot as plt

__author__  = 'First Lastname <email>, Voigt Lab, MIT'
__license__ = 'OSI Non-Profit OSL 3.0'
__version__ = '1.0'

# Color maps (let's make sure we use similar colors)
col_map = {}
col_map['red']     = (0.95, 0.30, 0.25)
col_map['green']   = (0.38, 0.82, 0.32)
col_map['blue']    = (0.38, 0.65, 0.87)
col_map['orange']  = (1.00, 0.75, 0.17)
col_map['purple']  = (0.55, 0.35, 0.64)
col_map['yellow']  = (0.98, 0.97, 0.35)

# Create the DNAplotlib renderer
dr = dpl.DNARenderer()

# Create the construct programmably to plot
sp = {'type':'EmptySpace', 'name':'S1', 'fwd':True}

a1  = {'type':'RecombinaseSite',  'name':'a1', 'fwd':True,   'opts':{'color':col_map['red'], 'x_extent':16, 'y_extent':12}}
a2  = {'type':'RecombinaseSite',  'name':'a2', 'fwd':False,  'opts':{'color':col_map['red'], 'x_extent':16, 'y_extent':12}}
a1f = {'type':'RecombinaseSite2', 'name':'a1', 'fwd':True,   'opts':{'color':col_map['red'], 'x_extent':16, 'y_extent':12}}
a2f = {'type':'RecombinaseSite2', 'name':'a2', 'fwd':False,  'opts':{'color':col_map['red'], 'x_extent':16, 'y_extent':12}}

b1  = {'type':'RecombinaseSite',  'name':'d1', 'fwd':True,  'opts':{'color':col_map['green'], 'x_extent':16, 'y_extent':12}}
b2  = {'type':'RecombinaseSite',  'name':'d2', 'fwd':False, 'opts':{'color':col_map['green'], 'x_extent':16, 'y_extent':12}}
b1f = {'type':'RecombinaseSite2', 'name':'d1', 'fwd':True,  'opts':{'color':col_map['green'], 'x_extent':16, 'y_extent':12}}
b2f = {'type':'RecombinaseSite2', 'name':'d2', 'fwd':False, 'opts':{'color':col_map['green'], 'x_extent':16, 'y_extent':12}}

c1  = {'type':'RecombinaseSite',  'name':'e1', 'fwd':True,  'opts':{'color':col_map['blue'], 'x_extent':16, 'y_extent':12}}
c2  = {'type':'RecombinaseSite',  'name':'e2', 'fwd':False, 'opts':{'color':col_map['blue'], 'x_extent':16, 'y_extent':12}}
c1f = {'type':'RecombinaseSite2', 'name':'e1', 'fwd':True,  'opts':{'color':col_map['blue'], 'x_extent':16, 'y_extent':12}}
c2f = {'type':'RecombinaseSite2', 'name':'e2', 'fwd':False, 'opts':{'color':col_map['blue'], 'x_extent':16, 'y_extent':12}}

d1  = {'type':'RecombinaseSite',  'name':'f1', 'fwd':True,  'opts':{'color':col_map['purple'], 'x_extent':16, 'y_extent':12}}
d2  = {'type':'RecombinaseSite',  'name':'f2', 'fwd':False, 'opts':{'color':col_map['purple'], 'x_extent':16, 'y_extent':12}}
d1f = {'type':'RecombinaseSite2', 'name':'f1', 'fwd':True,  'opts':{'color':col_map['purple'], 'x_extent':16, 'y_extent':12}}
d2f = {'type':'RecombinaseSite2', 'name':'f2', 'fwd':False, 'opts':{'color':col_map['purple'], 'x_extent':16, 'y_extent':12}}

e1  = {'type':'RecombinaseSite',  'name':'h1', 'fwd':True,  'opts':{'color':col_map['orange'], 'x_extent':16, 'y_extent':12}}
e2  = {'type':'RecombinaseSite',  'name':'h2', 'fwd':False, 'opts':{'color':col_map['orange'], 'x_extent':16, 'y_extent':12}}
e1f = {'type':'RecombinaseSite2', 'name':'h1', 'fwd':True,  'opts':{'color':col_map['orange'], 'x_extent':16, 'y_extent':12}}
e2f = {'type':'RecombinaseSite2', 'name':'h2', 'fwd':False, 'opts':{'color':col_map['orange'], 'x_extent':16, 'y_extent':12}}


x1 = {'type':'RecombinaseSite', 'name':'x1', 'fwd':True,  'opts':{'color':(0.3,0.3,0.3), 'x_extent':16, 'y_extent':12}}
x2 = {'type':'RecombinaseSite', 'name':'x2', 'fwd':False, 'opts':{'color':(0.3,0.3,0.3), 'x_extent':16, 'y_extent':12}}



# A design is merely a list of parts and their properties
design1 = [sp,  a1,sp,a2,    b1,sp,b2,    c1,sp,c2,    d1,sp,d2,    e1,sp,e2,    sp]
design2 = [sp,  a1f,sp,a2f,  b1,sp,b2,    c1,sp,c2,    d1,sp,d2,    e1,sp,e2,    sp]
design3 = [sp,  a1,sp,a2,    b1f,sp,b2f,  c1,sp,c2,    d1f,sp,d2f,  e1,sp,e2,    sp]
design4 = [sp,  a1f,sp,a2f,  b1,sp,b2,    c1f,sp,c2f,  d1,sp,d2,    e1f,sp,e2f,  sp]


# Either 1 or 2 column width
#fig = plt.figure(figsize=(3.2,0.8))
fig = plt.figure(figsize=(6.9,4.5))

#ax = fig.add_subplot(1,1,1)

ax_dna1 = plt.axes([0.0, 0.75, 1, 0.2])
ax_dna2 = plt.axes([0.0, 0.55, 1, 0.2])
ax_dna3 = plt.axes([0.0, 0.35, 1, 0.2])
ax_dna4 = plt.axes([0.0, 0.15, 1, 0.2])

# Redender the DNA to axis
start, end = dr.renderDNA(ax_dna1, design1, dr.SBOL_part_renderers())
start, end = dr.renderDNA(ax_dna2, design2, dr.SBOL_part_renderers())
start, end = dr.renderDNA(ax_dna3, design3, dr.SBOL_part_renderers())
start, end = dr.renderDNA(ax_dna4, design4, dr.SBOL_part_renderers())

# Set bounds and display options for the axis
dna_len = end-start
ax_dna1.set_xlim([start, end])
ax_dna1.set_ylim([-25,25])
ax_dna1.set_aspect('equal')
ax_dna1.set_xticks([])
ax_dna1.set_yticks([])
ax_dna1.axis('off')
ax_dna2.set_xlim([start, end])
ax_dna2.set_ylim([-25,25])
ax_dna2.set_aspect('equal')
ax_dna2.set_xticks([])
ax_dna2.set_yticks([])
ax_dna2.axis('off')
ax_dna3.set_xlim([start, end])
ax_dna3.set_ylim([-25,25])
ax_dna3.set_aspect('equal')
ax_dna3.set_xticks([])
ax_dna3.set_yticks([])
ax_dna3.axis('off')
ax_dna4.set_xlim([start, end])
ax_dna4.set_ylim([-25,25])
ax_dna4.set_aspect('equal')
ax_dna4.set_xticks([])
ax_dna4.set_yticks([])
ax_dna4.axis('off')

# Save the figure
fig.savefig('output.pdf', transparent=True)
# Clear the plotting cache
plt.close('all')
