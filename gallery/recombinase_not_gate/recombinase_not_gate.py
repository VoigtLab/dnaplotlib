#!/usr/bin/env python
"""
	Recombinase NOT-gate
"""

import math
import dnaplotlib as dpl
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

def sbol_recombinase1 (ax, type, num, start, end, prev_end, scale, linewidth, opts):
	""" SBOL recombinase site renderer - forward direction
	"""
	# Default parameters
	color = (0,0,0)
	color2 = (0,0,0)
	start_pad = 0.0
	end_pad = 0.0
	x_extent = 6.0
	y_extent = 6.0
	linestyle = '-'
	# Update default parameters if provided
	if opts != None:
		if 'start_pad' in opts.keys():
			start_pad = opts['start_pad']
		if 'end_pad' in opts.keys():
			end_pad = opts['end_pad']
		if 'x_extent' in opts.keys():
			x_extent = opts['x_extent']
		if 'y_extent' in opts.keys():
			y_extent = opts['y_extent']
		if 'linestyle' in opts.keys():
			linestyle = opts['linestyle']
		if 'linewidth' in opts.keys():
			linewidth = opts['linewidth']
		if 'scale' in opts.keys():
			scale = opts['scale']
		if 'color' in opts.keys():
			color = opts['color']
		if 'color2' in opts.keys():
			color2 = opts['color2']
	# Check direction add start padding
	final_end = end
	final_start = prev_end
	y_lower = -1 * y_extent/2
	y_upper = y_extent/2
	if start > end:
		start = prev_end+end_pad+x_extent+linewidth
		end = prev_end+end_pad
		final_end = start+start_pad
		color = color2
	else:
		start = prev_end+start_pad+linewidth
		end = start+x_extent
		final_end = end+end_pad
	# Draw the site
	p1 = Polygon([(start, y_lower), 
		          (start, y_upper),
		          (end,0)],
		          edgecolor=(0,0,0), facecolor=color, linewidth=linewidth, zorder=11, 
		          path_effects=[Stroke(joinstyle="miter")])		
	ax.add_patch(p1)
	# Add a label if needed
	if opts != None and 'label' in opts.keys():
		if final_start > final_end:
			write_label(ax, opts['label'], final_end+((final_start-final_end)/2.0), opts=opts)
		else:
			write_label(ax, opts['label'], final_start+((final_end-final_start)/2.0), opts=opts)
	# Return the final start and end positions to the DNA renderer
	if final_start > final_end:
		return prev_end, final_start
	else:
		return prev_end, final_end

def sbol_recombinase2 (ax, type, num, start, end, prev_end, scale, linewidth, opts):
	""" SBOL recombinase site renderer - reverse direction
	"""
	# Default parameters
	color = (0,0,0)
	color2 = (0,0,0)
	start_pad = 0.0
	end_pad = 0.0
	x_extent = 6.0
	y_extent = 6.0
	linestyle = '-'
	# Update default parameters if provided
	if opts != None:
		if 'start_pad' in opts.keys():
			start_pad = opts['start_pad']
		if 'end_pad' in opts.keys():
			end_pad = opts['end_pad']
		if 'x_extent' in opts.keys():
			x_extent = opts['x_extent']
		if 'y_extent' in opts.keys():
			y_extent = opts['y_extent']
		if 'linestyle' in opts.keys():
			linestyle = opts['linestyle']
		if 'linewidth' in opts.keys():
			linewidth = opts['linewidth']
		if 'scale' in opts.keys():
			scale = opts['scale']
		if 'color' in opts.keys():
			color = opts['color']
		if 'color2' in opts.keys():
			color2 = opts['color2']
		else:
			if 'color' in opts.keys():
				r2 = float(color[0]) / 2
				g2 = float(color[1]) / 2
				b2 = float(color[2]) / 2
				color2 = (r2,g2,b2)
	# Check direction add start padding
	final_end = end
	final_start = prev_end
	y_lower = -1 * y_extent/2
	y_upper = y_extent/2
	if start > end:
		start = prev_end+end_pad+x_extent+linewidth
		end = prev_end+end_pad
		final_end = start+start_pad
		temp = color
		color = color2
		color2 = temp
	else:
		start = prev_end+start_pad+linewidth
		end = start+x_extent
		final_end = end+end_pad
	# Draw the site
	p1 = Polygon([(start, y_lower), 
		         (start, y_upper),
		          (end,0)],
		          edgecolor=(0,0,0), facecolor=color, linewidth=linewidth, zorder=11, 
		          path_effects=[Stroke(joinstyle="miter")]) 
	midpoint = (end + start) / 2
	hypotenuse = math.sqrt( (y_extent/2)**2 + (x_extent)**2 )
	hypotenuse2 = hypotenuse / 2
	cosineA = (y_extent/2) / hypotenuse
	f = hypotenuse2 * cosineA
	p2 = Polygon([(midpoint, -1*f), 
		          (midpoint, f),
		          (end,0)],
		          edgecolor=(0,0,0), facecolor=color2, linewidth=linewidth, zorder=12, 
		          path_effects=[Stroke(joinstyle="miter")]) 	
	ax.add_patch(p1)
	ax.add_patch(p2)	
	# Add a label if needed
	if opts != None and 'label' in opts.keys():
		if final_start > final_end:
			write_label(ax, opts['label'], final_end+((final_start-final_end)/2.0), opts=opts)
		else:
			write_label(ax, opts['label'], final_start+((final_end-final_start)/2.0), opts=opts)
	# Return the final start and end positions to the DNA renderer
	if final_start > final_end:
		return prev_end, final_start
	else:
		return prev_end, final_end

def flip_arrow (ax, type, num, from_part, to_part, scale, linewidth, arc_height_index, opts):
	""" Regulation arcs for recombinase sites
	"""
	# Default parameters
	color = (0.0,0.0,0.0)
	arcHeightStart = 10
	arcHeightEnd = 10
	# Update default parameters if provided
	if opts != None:
		if 'linewidth' in opts.keys():
			linewidth = opts['linewidth']
		if 'color' in opts.keys():
			color = opts['color']
		if 'arc_height_start' in opts.keys():
			arcHeightStart = opts['arc_height_start']
		if 'arc_height_end' in opts.keys():
			arcHeightEnd = opts['arc_height_end']
	start = (from_part['start'] + from_part['end']) / 2
	end   = (to_part['start']   + to_part['end']) / 2
	# Check direction and draw arc
	if start > end:
		arcHeightStart = -arcHeightStart
		arcHeightEnd = -arcHeightEnd
	ax.annotate('', (end, arcHeightEnd), (start, arcHeightStart), ha="right", va="center", size=8, arrowprops=dict(arrowstyle='->',connectionstyle="arc3,rad=-.4",lw=linewidth, color=color))

# Color maps 
col_map = {}
col_map['red']     = (0.95, 0.30, 0.25)
col_map['green']   = (0.38, 0.82, 0.32)
col_map['blue']    = (0.38, 0.65, 0.87)
col_map['orange']  = (1.00, 0.75, 0.17)
col_map['purple']  = (0.55, 0.35, 0.64)

# Function to calculate darker colour
def dark (col, fac=2.0):
	return (col[0]/fac, col[1]/fac, col[2]/fac)

# Global line width
lw = 1.0

# Create the DNAplotlib renderer
dr = dpl.DNARenderer()

# Use default renderers and append our custom ones for recombinases
reg_renderers = dr.std_reg_renderers()
reg_renderers['Connection'] = flip_arrow
part_renderers = dr.SBOL_part_renderers()
part_renderers['RecombinaseSite'] = sbol_recombinase1
part_renderers['RecombinaseSite2'] = sbol_recombinase2

# Create the construct programmably to plot
sp = {'type':'EmptySpace', 'name':'S1', 'fwd':True, 'opts':{'x_extent':1}}
prom = {'type':'Promoter', 'name':'prom', 'fwd':True}
ins  = {'type':'Insulator', 'name':'ins', 'fwd':True}
ribo_r = {'type':'Ribozyme', 'name':'ribo', 'fwd':False}
rbs_r = {'type':'RBS', 'name':'rbs', 'fwd':False, 'opts':{'color':(0.0,0.0,0.0)}}
cds_r = {'type':'CDS', 'name':'cds', 'fwd':False, 'opts':{'color':(0.5,0.5,0.5), 'label':'GFP', 'label_x_offset':2, 'label_y_offset':0.5, 'label_rotation':180, 'label_style':'italic'}}
term = {'type':'Terminator', 'name':'term', 'fwd':True}
rec1f = {'type':'RecombinaseSite',  'name':'a1',  'fwd':True,   'opts':{'color':col_map['blue'], 'color2':dark(col_map['blue']), 'x_extent':16, 'y_extent':12, 'start_pad':3, 'end_pad':3}}
rec1r = {'type':'RecombinaseSite',  'name':'a1',  'fwd':False,  'opts':{'color':col_map['blue'], 'color2':dark(col_map['blue']), 'x_extent':16, 'y_extent':12, 'start_pad':3, 'end_pad':3}}
rec2f = {'type':'RecombinaseSite2',  'name':'a1f',  'fwd':True,   'opts':{'color':col_map['blue'], 'color2':dark(col_map['blue']), 'x_extent':16, 'y_extent':12, 'start_pad':3, 'end_pad':3}}
rec2r = {'type':'RecombinaseSite2',  'name':'a1f',  'fwd':False,  'opts':{'color':col_map['blue'], 'color2':dark(col_map['blue']), 'x_extent':16, 'y_extent':12, 'start_pad':3, 'end_pad':3}}
ribo_f = {'type':'Ribozyme', 'name':'ribo', 'fwd':True}
rbs_f = {'type':'RBS', 'name':'rbs', 'fwd':True, 'opts':{'color':(0.0,0.0,0.0)}}
cds_f = {'type':'CDS', 'name':'cds', 'fwd':True, 'opts':{'color':col_map['green'], 'label':'GFP', 'label_x_offset':-2, 'label_y_offset':-0.5, 'label_style':'italic'}}

design1 = [sp, prom, ins, rec1f, cds_r, rbs_r, ribo_r, rec1r, term, sp]
design2 = [sp, prom, ins, rec2f, ribo_f, rbs_f, cds_f, rec2r, term, sp]

arc1 = {'type':'Connection', 'from_part':rec1f, 'to_part':rec1r, 'opts':{'color':col_map['blue'],    'linewidth':lw, 'arc_height_start':10, 'arc_height_end':10}}
arc2 = {'type':'Connection', 'from_part':rec2r, 'to_part':rec2f, 'opts':{'color':col_map['blue'],    'linewidth':lw, 'arc_height_start':10, 'arc_height_end':10}}

reg1 = [arc1]
reg2 = [arc2]

# Create the figure
fig = plt.figure(figsize=(2.2,1.8))
gs = gridspec.GridSpec(3, 1)
ax_dna1 = plt.subplot(gs[0])
ax_dna2 = plt.subplot(gs[1])
ax_dna3 = plt.subplot(gs[2])

# Redender the DNA to axis
start, end = dr.renderDNA(ax_dna1, design1, part_renderers, regs=reg1, reg_renderers=reg_renderers)
ax_dna1.set_xlim([start, end])
ax_dna1.set_ylim([-18,18])
ax_dna1.set_aspect('equal')
ax_dna1.set_xticks([])
ax_dna1.set_yticks([])
ax_dna1.axis('off')
start, end = dr.renderDNA(ax_dna2, design2, part_renderers, regs=reg2, reg_renderers=reg_renderers)
ax_dna2.set_xlim([start, end])
ax_dna2.set_ylim([-18,18])
ax_dna2.set_aspect('equal')
ax_dna2.set_xticks([])
ax_dna2.set_yticks([])
ax_dna2.axis('off')
start, end = dr.renderDNA(ax_dna3, design1, part_renderers)
ax_dna3.set_xlim([start, end])
ax_dna3.set_ylim([-18,18])
ax_dna3.set_aspect('equal')
ax_dna3.set_xticks([])
ax_dna3.set_yticks([])
ax_dna3.axis('off')

# Update subplot spacing
plt.subplots_adjust(hspace=0.01, left=0.05, right=0.95, top=0.92, bottom=0.01)

# Save the figure
fig.savefig('recombinase_not_gate.pdf', transparent=True)
fig.savefig('recombinase_not_gate.png', dpi=300)

# Clear the plotting cache
plt.close('all')
