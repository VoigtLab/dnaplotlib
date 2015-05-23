#!/usr/bin/env python
"""
	Example of a dnaplotlib figure being plotted on a standard matplotlib axis.
"""

import dnaplotlib as dpl
import matplotlib.pyplot as plt
import numpy as np

# Create the DNA renderer
dr = dpl.DNARenderer()

# Set the renders to draw elements
part_renderers = {'Promoter'  :dpl.sbol_promoter, 
                  'CDS'       :dpl.sbol_cds, 
                  'Terminator':dpl.sbol_terminator}

# Create the construct programmably to plot
part_promoter = {'type':'Promoter', 'name':'P1', 'fwd':True}
part_promoter_rev = {'type':'Promoter', 'name':'rP1', 'fwd':False}
part_cds1 = {'type':'CDS', 'name':'CDS1', 'fwd':True}
part_cds1_rev = {'type':'CDS', 'name':'CDS2', 'fwd':False}
part_terminator = {'type':'Terminator', 'name':'T1', 'fwd':True}
part_terminator_rev = {'type':'Terminator', 'name':'rT1', 'fwd':False}
# A design is merely a list of parts and their properties
design = [part_promoter, part_cds1, part_terminator, part_terminator_rev, part_cds1_rev, part_promoter_rev]

# Create the figure and first axis
fig = plt.figure(figsize=(4,6))
ax = fig.add_subplot(2,1,1)

# Redender the DNA to axis
start, end = dr.renderDNA(ax, design, part_renderers)
# Set bounds and display options for the axis
dna_len = end-start
ax.set_xlim([start, end])
ax.set_ylim([-15,15])
ax.set_aspect('equal')
ax.set_xticks([])
ax.set_yticks([])
ax.set_title('Example construct')

# Plot another graph
ax2 = fig.add_subplot(2,1,2)
x = np.arange(100)
y = np.sin(x)
ax2.plot(x,y)
ax2.set_title('Example graph')

# Save the figure
plt.tight_layout()
fig.savefig('dna_axis_plot.pdf', transparent=True)

# Clear the plotting cache
plt.close('all')

