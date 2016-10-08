#!/usr/bin/env python
"""
	Rotated genetic design to generate a homology matrix for CRISPRi circuit
"""

import numpy as np
import string
import dnaplotlib as dpl
import matplotlib.pyplot as plt
import matplotlib
import pylab
import csv
import matplotlib.gridspec as gridspec
from matplotlib.transforms import Affine2D
import mpl_toolkits.axisartist.floating_axes as floating_axes
import mpl_toolkits.axisartist.grid_helper_curvelinear as gh
from mpl_toolkits.axes_grid.parasite_axes import SubplotHost, ParasiteAxesAuxTrans
from matplotlib import colors

__author__  = 'Thomas Gorochowski <tom@chofski.co.uk>, Voigt Lab, MIT'
__license__ = 'MIT'
__version__ = '1.0'

# Color maps (we use these throughout)
col_map = {}
col_map['red']     = (0.95, 0.30, 0.25)
col_map['green']   = (0.38, 0.82, 0.32)
col_map['blue']    = (0.38, 0.65, 0.87)
col_map['orange']  = (1.00, 0.75, 0.17)
col_map['purple']  = (0.55, 0.35, 0.64)
col_map['yellow']  = (0.98, 0.97, 0.35)
col_map['grey']    = (0.80, 0.80, 0.80)

# Options dictionary map (makes it easier to apply same styling)
opt_map = {}
opt_map['Promoter'] = {'color':col_map['green']}
opt_map['UserDefined'] = {'color':col_map['grey']}
opt_map['Terminator'] = {'color':col_map['red']}
opt_map['pTet'] = {'color':[0,0,0], 'label':'pTet', 'label_y_offset':-4, 'x_extent':50}
opt_map['pTac'] = {'color':[0,0,0], 'label':'pTac', 'label_y_offset':-4, 'x_extent':50}
opt_map['pA1'] = {'color':col_map['green'], 'label':'pA1', 'label_y_offset':-4, 'label_color':col_map['green'], 'x_extent':50}
opt_map['pA3'] = {'color':col_map['blue'], 'label':'pA3', 'label_y_offset':-4, 'label_color':col_map['blue'], 'x_extent':50}
opt_map['pA5'] = {'color':col_map['orange'], 'label':'pA5', 'label_y_offset':-4, 'label_color':col_map['orange'], 'x_extent':50}
opt_map['g1'] = {'color':col_map['green'], 'label':'g1', 'label_style':'italic', 'label_y_offset':4, 'label_color':col_map['green']}
opt_map['g2'] = {'color':(1,1,1), 'label':'g2', 'label_style':'italic', 'label_y_offset':4, 'label_color':(0,0,0)}
opt_map['g3'] = {'color':col_map['blue'], 'label':'g3', 'label_style':'italic', 'label_y_offset':4, 'label_color':col_map['blue']}
opt_map['g5'] = {'color':col_map['orange'], 'label':'g5', 'label_style':'italic', 'label_y_offset':4, 'label_color':col_map['orange']}

# Function to load the design of the circuit from a text file
def load_design (filename, opt_map):
	design = []
	parts = {}
	seq = ''
	cur_bp = 0
	reader = csv.reader(open(filename, 'rU'), delimiter=' ')
	for row in reader:
		if len(row) == 3:
			p_type = row[0]
			p_name = row[1]
			p_seq = row[2]
			p_opts = {}
			if p_name in opt_map.keys():
				p_opts = opt_map[p_name]
			elif p_type in opt_map.keys():
				p_opts = opt_map[p_type]
			new_part = {'type':p_type,
			            'name':p_name,
			            'start':cur_bp,
			            'end':cur_bp+len(p_seq),
			            'fwd':True,
			            'opts':p_opts}
			# Return all the parts by name
			if p_name not in parts.keys():
				parts[p_name] = [new_part]
			else:
				parts[p_name].append(new_part)
			design.append(new_part)
			seq += p_seq.upper()
			cur_bp = cur_bp+len(p_seq)
	return design, seq, parts

# Function to calculate the reverse complement of a sequence
def revcomp(seq, trans=string.maketrans("ACGT", "TGCA")):
	return "".join(reversed(seq.translate(trans)))

# Function to calculate number of shared bases between two sequences
def homology(seq1, seq2):
	same_count = 0
	for idx in range(len(seq1)):
		if idx < len(seq2):
			if seq1[idx] == seq2[idx]:
				same_count += 1
	return same_count

# Generate a homology matrix for a given sequence and window length
# (Homology is calculated against itself)
def homology_matrix2(seq, window_len=20):
	h_matrix = np.zeros((len(seq), len(seq)))
	for idx1 in range(len(seq)-window_len):
		# Extract the first seqeunce
		start_bp1 = idx1
		end_bp1 = idx1+window_len
		cur_seq1 = seq[start_bp1:end_bp1]

		for idx2 in range(len(seq)-window_len):
			# Extract the second sequence
			start_bp2 = idx2
			end_bp2 = idx2+window_len
			cur_seq2 = seq[start_bp2:end_bp2]

			# Calculate homology (include reverse complement)
			if cur_seq1 == cur_seq2 or cur_seq1 == revcomp(cur_seq2):
				h_matrix[start_bp1:end_bp1,start_bp2:end_bp2] = 1
	return h_matrix

# Load the design
design, seq, parts = load_design('data_design.txt', opt_map)

# Create regulation
arc1 = {'type':'Repression', 'from_part':parts['g5'][0], 'to_part':parts['pA5'][0], 'opts':{'color':col_map['orange'], 'linewidth':1.0, 'arrowhead_length':8, 'arc_height_start':8, 'arc_height_const':9, 'arc_height_spacing':1.1, 'arc_height_end':7.5}}
arc2 = {'type':'Repression', 'from_part':parts['g1'][0], 'to_part':parts['pA1'][0], 'opts':{'color':col_map['green'], 'linewidth':1.0, 'arrowhead_length':8, 'arc_height_start':8, 'arc_height_const':9, 'arc_height_spacing':1.1, 'arc_height_end':7.5}}
arc3 = {'type':'Repression', 'from_part':parts['g3'][0], 'to_part':parts['pA3'][0], 'opts':{'color':col_map['blue'], 'linewidth':1.0, 'arrowhead_length':8, 'arc_height_start':8, 'arc_height_const':9, 'arc_height_spacing':1.1, 'arc_height_end':7.5}}
arc4 = {'type':'Repression', 'from_part':parts['g3'][1], 'to_part':parts['pA3'][0], 'opts':{'color':col_map['blue'], 'linewidth':1.0, 'arrowhead_length':8, 'arc_height_start':8, 'arc_height_const':9, 'arc_height_spacing':1.1, 'arc_height_end':7.5}}

regs = [arc1, arc2, arc3, arc4]

# Calculate homology
h_matrix_60 = homology_matrix2(seq, window_len=60)
h_matrix_30 = homology_matrix2(seq, window_len=30)
h_matrix_15 = homology_matrix2(seq, window_len=15)

# Collate homology results so that different levels of homology are coloured differently
h_matrix = np.zeros((len(seq), len(seq)))
for idx1 in range(len(seq)):
	for idx2 in range(len(seq)):
		if h_matrix_60[idx1,idx2] == 1:
			h_matrix[idx1,idx2] = 60
		elif h_matrix_30[idx1,idx2] == 1:
			h_matrix[idx1,idx2] = 25
		elif h_matrix_15[idx1,idx2] == 1:
			h_matrix[idx1,idx2] = 10

# Create the figure and all axes to draw to
fig = plt.figure(figsize=(3.2,3.4))
gs = gridspec.GridSpec(2, 2, width_ratios=[1,9], height_ratios=[1.6,9])
ax_dna_x = plt.subplot(gs[1])

# Redender the DNA
dr = dpl.DNARenderer(scale=1, linewidth=0.9)
start, end = dr.renderDNA(ax_dna_x, design, dr.trace_part_renderers(), 
	                      regs=regs, reg_renderers=dr.std_reg_renderers())

# Set bounds and display options for the DNA axis
dna_len = end-start
ax_dna_x.set_xlim([start, end])
ax_dna_x.set_ylim([-6,13])
ax_dna_x.plot([start-20,end+20], [0,0], color=(0,0,0), linewidth=1.0, zorder=1)
ax_dna_x.axis('off')

# Setup the rotated axis
def setup_rot_axes(fig, rect):
	tr = Affine2D().rotate_deg(90.0)
	grid_helper = gh.GridHelperCurveLinear(tr)
	ax1 = SubplotHost(fig, rect, grid_helper=grid_helper)
	fig.add_subplot(ax1)
	ax2 = ParasiteAxesAuxTrans(ax1, tr, "equal")
	ax1.set_ylim([end, start])
	ax1.set_xlim([-8, 4])
	ax2 = ax1.get_aux_axes(tr)
	ax1.set_aspect('auto')
	ax1.axis['top', 'right', 'left', 'bottom'].set_visible(False)
	return ax1, ax2

# Generate the rotated axis.
ax_dna_y_main, ax_dna_y = setup_rot_axes(fig, gs[2])

# Before rendering rotated circuit remove all labels (simplify plot)
for el in design:
	if 'label' in el['opts'].keys():
		el['opts']['label'] = ''

# Render the rotated design normally (rotation done by matplotlib)
start, end = dr.renderDNA(ax_dna_y, design, dr.trace_part_renderers())

# Plot the homology matrix (make sure aspect the same)
ax_data = plt.subplot(gs[3], sharex=ax_dna_x)
ax_data.matshow(h_matrix, cmap=pylab.cm.gray_r)
ax_data.set_aspect('auto')
ax_data.set_xticks([])
ax_data.set_yticks([])
ax_data.set_ylim([end, start])
ax_data.set_xlim([start, end])

# Sort out subplot spacing
plt.subplots_adjust(hspace=.04, wspace=.04, left=.01, right=.99, top=0.99, bottom=0.01)

# Save the figure
fig.savefig('rotated_design.pdf', transparent=True)
fig.savefig('rotated_design.png', dpi=300)

# Clear the plotting cache
plt.close('all')
