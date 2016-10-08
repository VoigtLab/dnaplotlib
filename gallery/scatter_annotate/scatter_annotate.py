#!/usr/bin/env python
"""
	Annotation of standard scatter plot with genetic constructs
"""

import numpy as np
import matplotlib.pyplot as plt
import dnaplotlib as dpl
import csv

__author__  = 'Thomas Gorochowski <tom@chofski.co.uk>, Voigt Lab, MIT'
__license__ = 'MIT'
__version__ = '1.0'

# Read some data points for the scatter plot
filename_in ='data_points.txt'
data_reader = csv.reader(open(filename_in, 'rU'), delimiter=' ')
x = []
y = []
for row in data_reader:
	y.append( float(row[1]) )
	x.append( float(row[2]) )

# Generate the scatter plot
fig = plt.figure(figsize=(2.8,2.32))
ax = plt.subplot(1, 1, 1)
ax.set_yscale('log')
ax.set_xlim([0.85,1.05])
ax.set_ylim([1,500])
ax.set_xticks([0.85, 0.9, 0.95, 1.0, 1.05])
ax.tick_params(axis='y', labelsize=8)
ax.tick_params(axis='x', labelsize=8)
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
ax.yaxis.set_ticks_position('left')
ax.xaxis.set_ticks_position('bottom')
plt.xlabel('Parameter 1', fontsize=8, labelpad=0)
plt.ylabel('Parameter 2', fontsize=8, labelpad=0)
ax.tick_params(axis='y', which='major', pad=1)
plt.scatter(x, y, c='none', s=6, edgecolor=(0.5,0.5,0.5), lw = 0.8) #(0.38, 0.65, 0.87)

# Add arrows to the constructs
plt.annotate(
	'', 
	xy = (0.8785, 323.5), xytext = (25, 5),
	textcoords = 'offset points', ha = 'right', va = 'bottom',
	bbox = dict(boxstyle = 'round,pad=0.5', fc = 'yellow', alpha = 0.5),
	arrowprops = dict(arrowstyle = '->', linewidth=1.0, connectionstyle = 'arc3,rad=0'))
plt.annotate(
	'', 
	xy = (0.977, 34), xytext = (20, 14),
	textcoords = 'offset points', ha = 'right', va = 'bottom',
	bbox = dict(boxstyle = 'round,pad=0.5', fc = 'yellow', alpha = 0.5),
	arrowprops = dict(arrowstyle = '->', linewidth=1.0, connectionstyle = 'arc3,rad=0'))
plt.annotate(
	'', 
	xy = (0.982, 3.3), xytext = (22, 10),
	textcoords = 'offset points', ha = 'right', va = 'bottom',
	bbox = dict(boxstyle = 'round,pad=0.5', fc = 'yellow', alpha = 0.5),
	arrowprops = dict(arrowstyle = '->', linewidth=1.0, connectionstyle = 'arc3,rad=0'))

# Color maps (let's make sure we use similar colors)
col_map = {}
col_map['black']   = (0.00, 0.00, 0.00)
col_map['white']   = (1.00, 1.00, 1.00)
col_map['red']     = (0.95, 0.30, 0.25)
col_map['green']   = (0.38, 0.82, 0.32)
col_map['blue']    = (0.38, 0.65, 0.87)
col_map['orange']  = (1.00, 0.75, 0.17)
col_map['purple']  = (0.55, 0.35, 0.64)
col_map['yellow']  = (0.98, 0.97, 0.35)

# Global line width
lw = 1.0

# Define design 1
p1_1 = {'type':'Promoter', 'name':'pA', 'fwd':True, 'opts':{'linewidth':lw, 'color':col_map['black']}}
rbs_1_1 = {'type':'RBS', 'name':'rbs_f', 'fwd':True, 'opts':{'linewidth':lw, 'color':col_map['black'], 'start_pad':-6, 'x_extent':6}}
gA_1 = {'type':'CDS', 'name':'gA',  'fwd':True, 'opts':{'linewidth':lw, 'color':col_map['red'], 'edgecolor':col_map['red'], 'x_extent':24, 'label':'A', 'label_style':'italic', 'label_color':(1,1,1), 'label_x_offset':-3, 'label_y_offset':-1}}
rbs_1_2 = {'type':'RBS', 'name':'rbs_r', 'fwd':True, 'opts':{'linewidth':lw, 'color':col_map['black'], 'start_pad':2, 'x_extent':6}}
gB_1  = {'type':'CDS', 'name':'gB',  'fwd':True, 'opts':{'linewidth':lw, 'color':col_map['blue'], 'edgecolor':col_map['blue'], 'x_extent':24, 'label':'B', 'label_style':'italic', 'label_color':(1,1,1), 'label_x_offset':-3, 'label_y_offset':-1}}
t1_1 = {'type':'Terminator', 'name':'t0', 'fwd':True, 'opts':{'linewidth':lw, 'color':col_map['black'], 'start_pad':-1}}
design1 = [p1_1, rbs_1_1, gA_1, rbs_1_2, gB_1, t1_1]

# Define design 2
t1_2 = {'type':'Terminator', 'name':'t0', 'fwd':False, 'opts':{'linewidth':lw, 'color':col_map['black'], 'start_pad':-1}}
gA_2 = {'type':'CDS', 'name':'gA',  'fwd':False, 'opts':{'linewidth':lw, 'color':col_map['red'], 'edgecolor':col_map['red'], 'x_extent':24, 'label':'A', 'label_style':'italic', 'label_color':(1,1,1), 'label_x_offset':2, 'label_y_offset':-1}}
rbs_1_2 = {'type':'RBS', 'name':'rbs_f', 'fwd':False, 'opts':{'linewidth':lw, 'color':col_map['black'], 'start_pad':-6, 'x_extent':6}}
p1_2 = {'type':'Promoter', 'name':'pA', 'fwd':False, 'opts':{'linewidth':lw, 'color':col_map['black']}}
p2_2 = {'type':'Promoter', 'name':'pA', 'fwd':True, 'opts':{'linewidth':lw, 'color':col_map['black']}}
rbs_2_2 = {'type':'RBS', 'name':'rbs_r', 'fwd':True, 'opts':{'linewidth':lw, 'color':col_map['black'], 'start_pad':-6, 'x_extent':6}}
gB_2  = {'type':'CDS', 'name':'gB',  'fwd':True, 'opts':{'linewidth':lw, 'color':col_map['blue'], 'edgecolor':col_map['blue'], 'x_extent':24, 'label':'B', 'label_style':'italic', 'label_color':(1,1,1), 'label_x_offset':-3, 'label_y_offset':-1}}
t2_2 = {'type':'Terminator', 'name':'t0', 'fwd':True, 'opts':{'linewidth':lw, 'color':col_map['black'], 'start_pad':-1}}
design2 = [t1_2, gA_2, rbs_1_2, p1_2, p2_2, rbs_2_2, gB_2, t2_2]

# Define design 3
p1_3 = {'type':'Promoter', 'name':'pA', 'fwd':True, 'opts':{'linewidth':lw, 'color':col_map['black']}}
rbs_1_3 = {'type':'RBS', 'name':'rbs_r', 'fwd':True, 'opts':{'linewidth':lw, 'color':col_map['black'], 'start_pad':-6, 'x_extent':6}}
gA_3  = {'type':'CDS', 'name':'gB',  'fwd':True, 'opts':{'linewidth':lw, 'color':col_map['red'], 'edgecolor':col_map['red'], 'x_extent':24, 'label':'A', 'label_style':'italic', 'label_color':(1,1,1), 'label_x_offset':-3, 'label_y_offset':-1}}
t1_3 = {'type':'Terminator', 'name':'t0', 'fwd':True, 'opts':{'linewidth':lw, 'color':col_map['black'], 'start_pad':-1}}
t2_3 = {'type':'Terminator', 'name':'t0', 'fwd':False, 'opts':{'linewidth':lw, 'color':col_map['black'], 'start_pad':-1}}
gB_3 = {'type':'CDS', 'name':'gA',  'fwd':False, 'opts':{'linewidth':lw, 'color':col_map['blue'], 'edgecolor':col_map['blue'], 'x_extent':24, 'label':'B', 'label_style':'italic', 'label_color':(1,1,1), 'label_x_offset':0, 'label_y_offset':-1}}
rbs_2_3 = {'type':'RBS', 'name':'rbs_f', 'fwd':False, 'opts':{'linewidth':lw, 'color':col_map['black'], 'start_pad':-6, 'x_extent':6}}
p2_3 = {'type':'Promoter', 'name':'pA', 'fwd':False, 'opts':{'linewidth':lw, 'color':col_map['black']}}
design3 = [p1_3, rbs_1_3, gA_3, t1_3, t2_3, gB_3, rbs_2_3, p2_3]

# Set up the axes for the genetic constructs
ax_dna1 = plt.axes([0.35, 0.83, 0.35, 0.12])
ax_dna2 = plt.axes([0.61, 0.65, 0.4, 0.12])
ax_dna3 = plt.axes([0.58,  0.32, 0.4, 0.12])

# Create the DNAplotlib renderer
dr = dpl.DNARenderer()

# Redender the DNA to axis
start, end = dr.renderDNA(ax_dna1, design1, dr.SBOL_part_renderers())
ax_dna1.set_xlim([start, end])
ax_dna1.set_ylim([-15,15])
ax_dna1.set_aspect('equal')
ax_dna1.set_xticks([])
ax_dna1.set_yticks([])
ax_dna1.axis('off')
start, end = dr.renderDNA(ax_dna2, design2, dr.SBOL_part_renderers())
ax_dna2.set_xlim([start, end])
ax_dna2.set_ylim([-15,15])
ax_dna2.set_aspect('equal')
ax_dna2.set_xticks([])
ax_dna2.set_yticks([])
ax_dna2.axis('off')
start, end = dr.renderDNA(ax_dna3, design3, dr.SBOL_part_renderers())
ax_dna3.set_xlim([start, end])
ax_dna3.set_ylim([-15,15])
ax_dna3.set_aspect('equal')
ax_dna3.set_xticks([])
ax_dna3.set_yticks([])
ax_dna3.axis('off')

# Sort out subplot spacing
plt.subplots_adjust(hspace=0.01, left=0.13, right=0.95, top=0.93, bottom=0.13)

# Save the figure
fig.savefig('scatter_annotate.pdf', transparent=True)
fig.savefig('scatter_annotate.png', dpi=300)

# Clear the plotting cache
plt.close('all')

