#!/usr/bin/env python
"""
	Example of trace plotting.
"""

import dnaplotlib as dpl
import matplotlib.pyplot as plt
import numpy as np

# Create the DNA renderer
dr = dpl.DNARenderer(scale=2000.0/1500.0) # Recomend scaling bp by 1500.0 to get similar glyph sizes

# Set the renders to draw elements
part_renderers = dr.trace_part_renderers()

# Create the construct programmably to plot
part_promoter = {'type':'Promoter', 'name':'P1', 'fwd':True, 'start':10, 'end':76}
part_rbs = {'type':'RBS', 'name':'RBS1', 'fwd':True, 'start':80, 'end':105}
part_cds = {'type':'CDS', 'name':'CDS2', 'fwd':True, 'start':106, 'end':804}
part_terminator = {'type':'Terminator', 'name':'T1', 'fwd':True, 'start':805, 'end':821}

part_promoter_rev = {'type':'Promoter', 'name':'P1', 'fwd':False, 'start':2000, 'end':1950}
part_rbs_rev = {'type':'RBS', 'name':'RBS1', 'fwd':False, 'start':1933, 'end':1900}
part_cds_rev = {'type':'CDS', 'name':'CDS2', 'fwd':False, 'start':1901, 'end':860}
part_terminator_rev = {'type':'Terminator', 'name':'T1', 'fwd':False, 'start':859, 'end':845}
# A design is merely a list of parts and their properties
design = [part_promoter, part_rbs, part_cds, part_terminator, part_terminator_rev, 
          part_cds_rev, part_rbs_rev, part_promoter_rev]

# Create the figure and first axis
fig = plt.figure(figsize=(6,6))
ax = fig.add_subplot(2,1,1)

# Redender the DNA to axis
start, end = dr.renderDNA(ax, design, part_renderers)
# Set bounds and display options for the axis
dna_len = end-start
ax.set_xlim([-10, 2020])
ax.set_ylim([-25,25])
ax.set_xticks([])
ax.set_yticks([])
ax.set_title('Example construct')

# Plot another graph
ax2 = fig.add_subplot(2,1,2)
x = np.arange(2020)
y = np.sin(x/10)
ax2.plot(x,y)
ax2.set_title('Example graph')
ax2.set_xlim([-10, 2020])
ax2.set_ylim([-1.5,1.5])

# Save the figure
plt.tight_layout()
fig.savefig('trace_data_plot.pdf', transparent=True)

# Clear the plotting cache
plt.close('all')

