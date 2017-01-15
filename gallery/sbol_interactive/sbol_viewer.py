#!/usr/bin/env python
"""
	Recombinase NOT-gate
"""

PROMOTER = "http://purl.obolibrary.org/obo/SO_0000167"
RBS = "http://purl.obolibrary.org/obo/SO_0000552"
CDS = "http://purl.obolibrary.org/obo/SO_0000316"
TERMINATOR = "http://purl.obolibrary.org/obo/SO_0000139"

import sbol
import assembly

import math
import dnaplotlib as dpl
import dnaplotlib.sbol as dpl_sbol
import matplotlib.pyplot as plt
from matplotlib import gridspec
from matplotlib.patches import Polygon, Ellipse, Wedge, Circle, PathPatch
from matplotlib.path import Path
from matplotlib.lines import Line2D
from matplotlib.patheffects import Stroke
import matplotlib.patches as patches

__author__  = 'Bryan Der <bder@mit.edu>, Voigt Lab, MIT\n\
               Thomas Gorochowski <tom@chofski.co.uk>, Voigt Lab, MIT'
__license__ = 'MIT'
__version__ = '1.0'

# Test pySBOL interface
doc = sbol.Document()
doc.read('ExampleAlignment.xml')
target = doc.components['http://sys-bio.org/Design']
module = [ None ] * 3
module[0] = doc.components['http://sys-bio.org/DC1']
module[1] = doc.components['http://sys-bio.org/DC2']
module[2] = doc.components['http://sys-bio.org/DC3']

# Create the DNAplotlib renderer
dr = dpl_sbol.SBOLRenderer()

design = []
for dc in module:
    SO_term = dc.type.split('/')[-1]
    part = {}
    if SO_term in list(dr.SO_terms().keys()):
        part['type'] = dr.SO_terms()[SO_term]
    part['name'] = dc.name
    part['fwd'] = True
    design.append(part)

# Instantiate rendered
part_renderers = dr.SBOL_part_renderers()

# Create the figure
fig = plt.figure()
ax = plt.gca()
start, end = dr.renderSBOL(ax, target, part_renderers)

# for i_part, part in enumerate(design):
#
#     start, end = (part['start'], part['end'])
#     identity = assembly.calculate_identity(module[i_part])
#     dpl.write_label(ax, "%.2f" %identity, (start+end)/2, { 'label_size' : 18, 'label_y_offset': 12 })
#     #ax.text(center, -10, "%.2f" %identity, horizontalalignment = 'center', fontsize = 12)
from matplotlib.patches import Rectangle
ax.set_xlim([start, end])
ax.set_ylim([-18,18])
ax.set_aspect('equal')
ax.set_xticks([])
ax.set_yticks([])
ax.axis('off')
#plt.ion()
#ax.add_patch(Rectangle((start, .5), 1, 1, facecolor="grey"))
#plt.show()

design = []
subcomponents = []
for ann in module[0].annotations:
    dc = ann.subcomponent
    subcomponents.append(dc)
    SO_term = dc.type.split('/')[-1]
    part = {}
    if SO_term in list(dr.SO_terms().keys()):
        part['type'] = dr.SO_terms()[SO_term]
    part['name'] = dc.display_id
    part['fwd'] = True
    design.append(part)

"""
# Create the figure
fig = plt.figure()
ax = plt.gca()
start, end = dr.renderDNA(ax, design, part_renderers)
for i_part, part in enumerate(design):
    name = part['name']
    center = (part['start'] + part['end']) / 2
    ax.text(center, -10, name, horizontalalignment = 'center', fontsize = 12)
    coverage = assembly.calculate_coverage(subcomponents[i_part])
    ax.text(center, -15, "%.2f" %coverage, horizontalalignment = 'center', fontsize = 12)
    identity = assembly.calculate_identity(subcomponents[i_part])
    ax.text(center, -16.5, "%.2f" %identity, horizontalalignment = 'center', fontsize = 12)
    ambiguity = assembly.calculate_ambiguity(subcomponents[i_part])
    ax.text(center, -18, "%.2f" %ambiguity, horizontalalignment = 'center', fontsize = 12)


ax.set_xlim([start, end])
ax.set_ylim([-18,18])
ax.set_aspect('equal')
ax.set_xticks([])
ax.set_yticks([])
ax.axis('off')
"""

plt.show()
# Clear the plotting cache
#plt.close('all')
