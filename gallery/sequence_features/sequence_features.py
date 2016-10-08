#!/usr/bin/env python
"""
	Visualize sequence features
"""

import dnaplotlib as dpl
import matplotlib.pyplot as plt
from matplotlib import gridspec

# Required for drawing shapes
from matplotlib.patches import Polygon
from matplotlib.lines import Line2D
from matplotlib.patheffects import Stroke
import matplotlib.patches as patches

__author__  = 'Thomas Gorochowski <tom@chofski.co.uk>, Voigt Lab, MIT'
__license__ = 'MIT'
__version__ = '1.0'

##############################################################################
# HELPER FUNCTIONS
# Could be integrated into DNAplotlib in the future. You can create renderer
# functions for each type of annoation and these are then easily used by
# DNAplotlib. I created a very simple one for what we discussed - these can
# be customised further by the opts dictionary in the later section to capture
# metadata such as strength, etc.
##############################################################################

# Function for writing a sequence to axis
def draw_sequence (ax, start_pos, y_offset, seq):
	# For each letter position in center of range
	for c_idx, c in enumerate(seq):
		ax.annotate(c,(start_pos+c_idx+0.5, y_offset), ha='center', va='bottom', fontsize=8)

# Custom renderer for promoter -35 to -10 site (this is used by DNAplotlib to render the sites in a design)
def promoter_region (ax, type, num, start, end, prev_end, scale, linewidth, opts):
	# Default parameters - these can be added to, but we usually use this style (probably should simplify in future)
	y_offset = 0.0
	color_35 = (0.5,0.5,0.5)
	color_10 = (0.5,0.5,0.5)
	color_connector = (0,0,0)
	linewidth_connector = 2.0
	len_35 = 4
	len_10 = 2
	y_extent = 4.0
	# Update default parameters if provided
	if opts != None:
		if 'y_extent' in opts.keys():
			y_extent = opts['y_extent']
		if 'y_offset' in opts.keys():
			y_offset = opts['y_offset']
		if 'linewidth' in opts.keys():
			linewidth = opts['linewidth']
		if 'color_35' in opts.keys():
			color_35 = opts['color_35']
		if 'color_10' in opts.keys():
			color_10 = opts['color_10']
		if 'color_connector' in opts.keys():
			color_connector = opts['color_connector']
		if 'linewidth_connector' in opts.keys():
			linewidth_connector = opts['linewidth_connector']
		if 'len_35' in opts.keys():
			len_35 = opts['len_35']
		if 'len_10' in opts.keys():
			len_10 = opts['len_10']
	# Check direction (we don't use at moment)
	fwd = True
	if start > end:
		fwd = False
	# Draw the -35 site (from start to start + length of -35 site)
	p35 = Polygon([(start, y_offset), 
		           (start, y_offset+y_extent),
		           (start+len_35,y_offset+y_extent),
		           (start+len_35,y_offset)],
		            edgecolor=(0,0,0), facecolor=color_35, linewidth=linewidth, zorder=11, 
		            path_effects=[Stroke(joinstyle="miter")])		
	ax.add_patch(p35)
	# Draw the -10 site (from end-length of -10 site to end)
	p10 = Polygon([(end-len_10, y_offset), 
		           (end-len_10, y_offset+y_extent),
		           (end,y_offset+y_extent),
		           (end,y_offset)],
		            edgecolor=(0,0,0), facecolor=color_10, linewidth=linewidth, zorder=11, 
		            path_effects=[Stroke(joinstyle="miter")])		
	ax.add_patch(p10)
	l1 = Line2D([start+len_35, end-len_10],
                [y_offset+(y_extent/2.0), y_offset+(y_extent/2.0)], linewidth=linewidth_connector, 
                color=color_connector, zorder=10)
	ax.add_line(l1)

	# Add a label if needed
	if opts != None and 'label' in opts.keys():
		if final_start > final_end:
			dpl.write_label(ax, opts['label'], final_end+((final_start-final_end)/2.0), opts=opts)
		else:
			dpl.write_label(ax, opts['label'], final_start+((final_end-final_start)/2.0), opts=opts)
	# Return the final start and end positions to the DNA renderer
	return start, end

##############################################################################
# CREATES THE FIGURE
##############################################################################

# Create the figure
fig = plt.figure(figsize=(3.0,1.5))
gs = gridspec.GridSpec(1, 1)
ax_dna = plt.subplot(gs[0])

# This is the main sequence
seq1 = 'AATTCCGAGCGCGAGCTTTGCGAGTGA'
draw_sequence(ax_dna, 0, 0, seq1)

# Another sequence to show you can overlay them if needed with an offset
seq2 = 'TTGCGAGTGA'
draw_sequence(ax_dna, 8, 5, seq2)

# Create the DNAplotlib renderer and map of part types to renderering functions
dr = dpl.DNARenderer()
part_renderers = {'PromoterRegion': promoter_region}

# Create the sites to draw
r1 = {'type':'PromoterRegion', 'name':'region1', 'start': 2, 'end': 13, 'fwd':True, 'opts':{'y_offset':10, 'len_35':1, 'len_10':1, 'color_35':(0,0.5,0.2), 'color_10':(0.9,0.2,0.7)}}
r2 = {'type':'PromoterRegion', 'name':'region2', 'start': 15, 'end': 22, 'fwd':True, 'opts':{'y_offset':20, 'color_connector':(1,0,0), 'linewidth_connector':4.0}}
r3 = {'type':'PromoterRegion', 'name':'region3', 'start': 5, 'end': 24, 'fwd':True, 'opts':{'y_offset':30}}

# We don't use a design, so just annotate an axis
dr.annotate(ax_dna, part_renderers, r1)
dr.annotate(ax_dna, part_renderers, r2)
dr.annotate(ax_dna, part_renderers, r3)

# Set up bounds of the axis
ax_dna.set_xlim([-0.5, len(seq1)+0.5])
ax_dna.set_ylim([0,40])
ax_dna.set_xticks([])
ax_dna.set_yticks([])
ax_dna.axis('off')

# Update subplot spacing
plt.subplots_adjust(left=0.01, right=0.99, top=0.99, bottom=0.01)

# Save the figure
fig.savefig('sequence_features.pdf', transparent=True)
fig.savefig('sequence_features.png', dpi=300)

# Clear the plotting cache
plt.close('all')
