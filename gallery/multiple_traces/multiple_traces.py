#!/usr/bin/env python
"""
	Example of trace plotting from a GeneClusterLibrary object.
"""

import dnaplotlib as dpl
import matplotlib.pyplot as plt
import csv
import numpy as np
import matplotlib.gridspec as gridspec

# Calculates a lighter color
def lighten_color (col, fac):
	r = col[0] + (fac*(1.0-col[0]))
	g = col[1] + (fac*(1.0-col[1]))
	b = col[2] + (fac*(1.0-col[2]))
	return (r,g,b)

# Color maps
col_map = {}
col_map['red']     = (0.95, 0.30, 0.25)
col_map['green']   = (0.38, 0.82, 0.32)
col_map['blue']    = (0.38, 0.65, 0.87)
col_map['orange']  = (1.00, 0.75, 0.17)
col_map['purple']  = (0.55, 0.35, 0.64)
col_map['yellow']  = (0.98, 0.97, 0.35)
col_map['grey']    = (0.70, 0.70, 0.70)
col_map['dark_grey'] = (0.60, 0.60, 0.60)
col_map['light_grey'] = (0.9, 0.9, 0.9)

opt_CDS1 = {'label':'nifV', 'label_style':'italic', 'label_y_offset':-5, 'color':col_map['light_grey']}
opt_CDS2 = {'label':'nifS', 'label_style':'italic', 'label_y_offset':-5, 'color':col_map['dark_grey']}
opt_CDS3 = {'label':'nifZ', 'label_style':'italic', 'label_y_offset':-5, 'color':col_map['light_grey']}
opt_CDS4 = {'label':'nifM', 'label_style':'italic', 'label_y_offset':-5, 'color':col_map['light_grey']}

# Design of the construct
P1 = {'type':'Promoter', 'name':'P1', 'start':0,    'end':23,   'fwd':True, 'opts':{'color':col_map['green']}}
P2 = {'type':'Promoter', 'name':'P2', 'start':2643, 'end':2666, 'fwd':True, 'opts':{'color':col_map['green']}}
P3 = {'type':'Promoter', 'name':'P3', 'start':3320, 'end':3297, 'fwd':False, 'opts':{'color':col_map['green']}}
P4 = {'type':'Promoter', 'name':'P4', 'start':4336, 'end':4313, 'fwd':False, 'opts':{'color':col_map['green']}}
RBS1 = {'type':'RBS', 'name':'RBS1', 'start':72,   'end':106,  'fwd':True, 'opts':{'color':col_map['blue']}}
RBS2 = {'type':'RBS', 'name':'RBS2', 'start':1353, 'end':1392, 'fwd':True, 'opts':{'color':col_map['blue']}}
RBS3 = {'type':'RBS', 'name':'RBS4', 'start':3248, 'end':3217, 'fwd':False, 'opts':{'color':col_map['blue']}}
RBS4 = {'type':'RBS', 'name':'RBS3', 'start':4209, 'end':4175, 'fwd':False, 'opts':{'color':col_map['blue']}}
CDS1 = {'type':'CDS', 'name':'CDS1', 'start':106,  'end':1249, 'fwd':True, 'opts':opt_CDS1}
CDS2 = {'type':'CDS', 'name':'CDS2', 'start':1392, 'end':2595, 'fwd':True, 'opts':opt_CDS2}
CDS3 = {'type':'CDS', 'name':'CDS3', 'start':3217, 'end':2770, 'fwd':False, 'opts':opt_CDS3}
CDS4 = {'type':'CDS', 'name':'CDS4', 'start':4175, 'end':3374, 'fwd':False, 'opts':opt_CDS4}
T1 = {'type':'Terminator', 'name':'T1', 'start':2595, 'end':2643, 'fwd':True, 'opts':{'color':col_map['red']}}

# A design is merely a list of parts and their properties
design = [P1, RBS1, CDS1, RBS2, CDS2, T1, P2, CDS3, RBS3, P3, CDS4, RBS4, P4]

def load_seq (filename_in):
	f_in = open(filename_in, 'rU')
	seq = f_in.readline().strip()
	f_in.close()
	return seq

def gc_window(seq, window_len):
	out = [0]*len(seq)
	for idx in range(len(seq)):
		start_idx = idx
		end_idx = start_idx+window_len
		if end_idx > len(seq):
			end_idx = len(seq)
		gc_count = seq[start_idx:end_idx].count('G')
		gc_count += seq[start_idx:end_idx].count('C')
		out[idx] = gc_count/float(window_len)
	return np.array(out)

def load_trace (filename_in):
	# data[0] is forward strand
	# data[1] is reverse strand
	data = [[],[]]
	trace_reader = csv.reader(open(filename_in, 'rU'), delimiter=',')
	data[0] = np.array([float(x) for x in next(trace_reader)])
	data[1] = np.array([float(x) for x in next(trace_reader)])
	return data

def plot_trace_2 (ax_trace, data, col, lab='', hightlight=[0,0]):
	trace_len = len(data[0])
	ax_trace.fill_between(range(trace_len),data[0],np.zeros(trace_len), color=lighten_color(col,0.5), edgecolor=lighten_color(col,0.5), linewidth=1, zorder=1)
	ax_trace.fill_between(range(trace_len),-data[1],np.zeros(trace_len), color=lighten_color(col,0.5), edgecolor=lighten_color(col,0.5), linewidth=1, zorder=1)
	
	# Hightlighted region
	r = np.arange(hightlight[0], hightlight[1])
	ax_trace.fill_between(r,data[0][hightlight[0]:hightlight[1]],np.zeros(len(r)), color=col, edgecolor=col, linewidth=1, zorder=1.5)
	ax_trace.fill_between(r,-data[1][hightlight[0]:hightlight[1]],np.zeros(len(r)), color=col, edgecolor=col, linewidth=1, zorder=1.5)
	
	ax_trace.plot(range(trace_len), np.zeros(trace_len), color=(0,0,0), linewidth=1, zorder=2)
	max_read_depth = max(data[0])
	max_read_depth_1 = max(data[1])
	if max_read_depth_1 > max_read_depth:
		max_read_depth = max_read_depth_1
	# Scale the y-axis of the traces appropriately
	max_read_depth *= 1.02
	ax_trace.set_ylim([-max_read_depth,max_read_depth])
	ax_trace.spines["right"].set_visible(False)
	ax_trace.spines["top"].set_visible(False)
	ax_trace.spines["bottom"].set_visible(False)
	ax_trace.tick_params(axis='both', direction='out')
	ax_trace.set_xticks([])
	#ax_trace.set_yticks([])
	ax_trace.get_yaxis().tick_left()
	ax_trace.tick_params('both', length=2, width=0.5, which='major')
	ax_trace.tick_params(axis='y', which='major', pad=2)
	ax_trace.tick_params(axis='y', labelsize=8)
	ax_trace.set_ylabel(lab, fontsize=8, labelpad=6)

def plot_trace_1 (ax_trace, data, col, scale=None, min_y=0, max_y=None, lab='', hightlight=[0,0]):
	trace_len = len(data)
	ax_trace.fill_between(range(trace_len),data,np.zeros(trace_len), color=lighten_color(col,0.5), edgecolor=lighten_color(col,0.5), linewidth=1, zorder=1)
	
	# Hightlighted region
	r = np.arange(hightlight[0], hightlight[1])
	ax_trace.fill_between(r,data[hightlight[0]:hightlight[1]],np.zeros(len(r)), color=col, edgecolor=col, linewidth=1, zorder=1.5)
	
	ax_trace.plot(range(trace_len), np.zeros(trace_len), color=(0,0,0), linewidth=1, zorder=2)
	max_read_depth = max(data) * 1.02
	if max_y == None:
		ax_trace.set_ylim([min_y,max_read_depth])
	else:
		ax_trace.set_ylim([min_y,max_y])
	ax_trace.spines["right"].set_visible(False)
	ax_trace.spines["top"].set_visible(False)
	#ax_trace.spines["bottom"].set_visible(False)
	ax_trace.tick_params(axis='both', direction='out')
	ax_trace.set_xticks([])
	#ax_trace.set_yticks([])
	ax_trace.get_yaxis().tick_left()
	ax_trace.tick_params('both', length=2, width=0.5, which='major')
	ax_trace.tick_params(axis='y', which='major', pad=2)
	ax_trace.tick_params(axis='y', labelsize=8)
	if scale != None:
		ax_trace.set_yscale(scale)
	ax_trace.set_ylabel(lab, fontsize=8, labelpad=1)

# Create the figure and all axes to draw to
fig = plt.figure(figsize=(3.2,2.7))
gs = gridspec.GridSpec(4, 1, height_ratios=[0.6,1.5,0.8,0.8])
ax_dna = plt.subplot(gs[0])
ax_trace1 = plt.subplot(gs[1], sharex=ax_dna)
ax_trace1.set_yticklabels(['', '50', '0', '50'])
ax_trace1.text(0.01, 0.86, 'sense', horizontalalignment='left', verticalalignment='center', transform=ax_trace1.transAxes, fontsize=8)
ax_trace1.text(0.01, 0.14, 'anti-sense', horizontalalignment='left', verticalalignment='center', transform=ax_trace1.transAxes, fontsize=8)

ax_trace2 = plt.subplot(gs[2], sharex=ax_dna)
ax_trace3 = plt.subplot(gs[3], sharex=ax_dna)

# Load the trace data
data_rnaseq = load_trace('data_rnaseq.csv')
#data_promoter = load_trace('./data/promoter_fwd_rev.csv')
data_rbs = load_trace('data_rbs.csv')
seq = load_seq('data_seq.txt')
data_gc = gc_window(seq, 50)

# Plot the traces
plot_trace_2(ax_trace1, data_rnaseq, col_map['orange'], lab='Read Depth', hightlight=[RBS2['start'], CDS2['end']])
plot_trace_1(ax_trace2, data_rbs[0]+data_rbs[1], col_map['blue'], scale='log', min_y=2000, lab='RBS Score', hightlight=[RBS2['start'], CDS2['end']])
plot_trace_1(ax_trace3, data_gc*100, col_map['purple'], max_y=100, lab='GC %', hightlight=[RBS2['start'], CDS2['end']])

# Redender the DNA
dr = dpl.DNARenderer(scale=4, linewidth=0.9)
start, end = dr.renderDNA(ax_dna, design, dr.trace_part_renderers())
# Set bounds and display options for the DNA axis
dna_len = end-start
ax_dna.set_xlim([start-20, end+20])
ax_dna.set_ylim([-8,8])
ax_dna.plot([start-20,end+20], [0,0], color=(0,0,0), linewidth=1.0, zorder=1)
ax_dna.axis('off')

# Make spacing between subplot less
plt.subplots_adjust(hspace=.08, left=.12, right=.99, top=0.99, bottom=0.02)
# Save the figure
fig.savefig('multiple_traces.pdf', transparent=True)
fig.savefig('multiple_traces.png', dpi=300)
# Clear the plotting cache
plt.close('all')

