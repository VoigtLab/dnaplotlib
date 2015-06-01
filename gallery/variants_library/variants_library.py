#!/usr/bin/env python
"""
    Plots a set of designs and related performance informations. This
    has been adapted from the "plot_SBOL_designs.py" app, showing how
    existing scripts can easily be extended to include new functionality.
"""

import sys
import getopt
import csv
import dnaplotlib as dpl
import matplotlib.pyplot as plt
from argparse import ArgumentParser
import os.path
import matplotlib.gridspec as gridspec
import numpy as np

__author__  = 'Thomas E. Gorochowski <tom@chofski.co.uk>, Voigt Lab, MIT'
__license__ = 'OSI Non-Profit OSL 3.0'
__version__ = '1.0'

# Function that converts string to float (if possible)
def make_float_if_needed (s):
	try:
		float(s)
		return float(s)
	except ValueError:
		return s

# Function to load the parameters data file
def load_plot_parameters (filename):
	plot_params = {}
	param_reader = csv.reader(open(filename, 'rU'), delimiter=',')
	# Ignore header
	header = next(param_reader)
	# Process all parameters
	for row in param_reader:
		if len(row) >= 2:
			if row[1] != '':
				plot_params[row[0]] = make_float_if_needed(row[1])
	return plot_params

# Function to load the part information data file
def load_part_information (filename):
	part_info = {}
	parts_reader = csv.reader(open(filename, 'rU'), delimiter=',')
	header = next(parts_reader)
	header_map = {}
	for i in range(len(header)):
		header_map[header[i]] = i
	attrib_keys = [k for k in header_map.keys() if k not in ['part_name', 'type']]
	for row in parts_reader:
		# Make the attributes map
		part_attribs_map = {}
		for k in attrib_keys:
			if row[header_map[k]] != '':
				if k == 'color' or k == 'label_color':
					part_attribs_map[k] = [float(x) for x in row[header_map[k]].split(';')]
				else:
					part_attribs_map[k] = make_float_if_needed(row[header_map[k]])
		part_name = row[header_map['part_name']]
		part_type = row[header_map['type']]
		part_info[part_name] = [part_name, part_type, part_attribs_map]
	return part_info

# Function to load the performance data file
def load_perf_information (filename):
	perf_info = {}
	perf_reader = csv.reader(open(filename, 'rU'), delimiter=',')
	header = next(perf_reader)
	header_map = {}
	for i in range(len(header)):
		header_map[header[i]] = i
	attrib_keys = [k for k in header_map.keys() if k != 'Variant']
	for row in perf_reader:
		# Make the attributes map
		perf_attribs_map = {}
		for k in attrib_keys:
			if row[header_map[k]] != '':
				perf_attribs_map[k] = make_float_if_needed(row[header_map[k]])
		variant = row[header_map['Variant']]
		perf_info[variant] = perf_attribs_map
	return perf_info

# Function to load the DNA designs data file
def load_dna_designs (filename, part_info):
	dna_design_order = []
	dna_designs = {}
	design_reader = csv.reader(open(filename, 'rU'), delimiter=',')
	# Ignore header
	header = next(design_reader)
	# Process all parameters
	for row in design_reader:
		if len(row[0]) != '':
			part_list = []
			for i in range(1,len(row)):
				# Handle reverse parts
				fwd = True
				part_name = row[i]
				if len(part_name) != 0:
					if part_name[0] == 'r':
						part_name = part_name[1:]
						fwd = False
					# Store the design
					part_design = {}
					cur_part_info = part_info[part_name]
					part_design['type'] = cur_part_info[1]
					part_design['name'] = part_name
					part_design['fwd']  = fwd 
					if fwd == True:
						part_design['start'] = i
						part_design['end'] = i+1
					else:
						part_design['end'] = i
						part_design['start'] = i+1
					part_design['opts'] = cur_part_info[2]
					part_list.append(part_design)
			dna_designs[row[0]] = part_list
			dna_design_order.append(row[0])
	return dna_designs, dna_design_order

# Function to all of the values for a given attribute from a dictionary
def extract_dict_attribs (d, dict_keys, attrib_key):
	out = []
	for d_key in dict_keys:
		out.append(d[d_key][attrib_key])
	return out

# Function to plot the designs and performance information
def plot_dna (dna_designs, dna_design_order, out_filename, plot_params, perf_data):
	# Default parameters for the plotting
	if 'axis_y' not in plot_params.keys():
		plot_params['axis_y'] = 35
	left_pad = 0.0
	right_pad = 0.0
	scale = 1.0
	linewidth = 1.0
	fig_y = 5.0
	fig_x = 5.0
	# Update parameters if needed
	if 'backbone_pad_left' in plot_params.keys():
		left_pad = plot_params['backbone_pad_left']
	if 'backbone_pad_right' in plot_params.keys():
		right_pad = plot_params['backbone_pad_right']
	if 'scale' in plot_params.keys():
		scale = plot_params['scale']
	if 'linewidth' in plot_params.keys():
		linewidth = plot_params['linewidth']
	if 'fig_y' in plot_params.keys():
		fig_y = plot_params['fig_y']
	if 'fig_x' in plot_params.keys():
		fig_x = plot_params['fig_x']
	dr = dpl.DNARenderer(scale=scale, linewidth=linewidth,
		                 backbone_pad_left=left_pad, 
		                 backbone_pad_right=right_pad)

	# We default to the SBOL part renderers
	part_renderers = dr.SBOL_part_renderers()

    # Create the figure
	fig = plt.figure(figsize=(3.6,6.2))

	# Cycle through the designs an plot on individual axes
	design_list = sorted(dna_designs.keys())
	num_of_designs = len(design_list)
	ax_list = []
	max_dna_len = 0.0
	gs = gridspec.GridSpec(num_of_designs,2, width_ratios=[1,12])

	# Plot the genetic designs
	for i in range(len(dna_design_order)):
		# Create axis for the design and plot
		design =  dna_designs[dna_design_order[i]]
		ax = plt.subplot(gs[i, 1])
		if 'show_title' in plot_params.keys() and plot_params['show_title'] == 'Y':
			ax.set_title(design_list[i], fontsize=8)
		start, end = dr.renderDNA(ax, design, part_renderers)
		dna_len = end-start
		if max_dna_len < dna_len:
			max_dna_len = dna_len
		ax_list.append(ax)
	for ax in ax_list:
		ax.set_xticks([])
		ax.set_yticks([])
		# Set bounds
		ax.set_xlim([(-0.01*max_dna_len)-left_pad,
			        max_dna_len+(0.01*max_dna_len)+right_pad])
		ax.set_ylim([-14,14])
		ax.set_aspect('equal')
		ax.set_axis_off()

	# Plot the performance data (bar charts)
	perf_vals = extract_dict_attribs(perf_data, dna_design_order, 'Activity')
	perf_sd_vals = extract_dict_attribs(perf_data, dna_design_order, 'Activity_SD')
	ax_perf = plt.subplot(gs[:, 0])
	bar_height = 0.3
	ax_perf.plot([1],[1])
	ax_perf.spines['top'].set_visible(False)
	ax_perf.spines['bottom'].set_visible(False)
	ax_perf.spines['right'].set_visible(False)
	ax_perf.invert_yaxis()
	ax_perf.set_xticks([])
	ax_perf.yaxis.tick_left()
	ax_perf.yaxis.set_ticks_position('left')
	ax_perf.tick_params(axis='y', direction='out')
	ax_perf.tick_params('y', length=3, width=0.8, which='major', pad=2, labelsize=8)
	pos1 = np.arange(len(perf_vals))
	ax_perf.barh(pos1, perf_vals, height=bar_height, color=(0.6,0.6,0.6), edgecolor=(0.6,0.6,0.6))
	ax_perf.errorbar(perf_vals, pos1+(bar_height/2.0), fmt='none', xerr=perf_sd_vals, ecolor=(0,0,0), capthick=1)
	ax_perf.set_yticks(pos1+(bar_height/2.0))
	ax_perf.set_yticklabels(dna_design_order)
	ax_perf.set_ylim([max(pos1)+0.65, -0.35])
	ax_perf.set_xlim([0, 1062606*1.05])

	# Save the figure
	plt.subplots_adjust(hspace=0.001, wspace=0.05, top=0.99, bottom=0.01, left=0.06, right=0.99)
	fig.savefig(out_filename, transparent=True, dpi=300)
	
	# Clear the plotting cache
	plt.close('all')

def main():	
	# Load the data
	plot_params = load_plot_parameters('plot_parameters.csv')
	part_info = load_part_information('part_information.csv')
	dna_designs, dna_design_order = load_dna_designs ('dna_designs.csv', part_info)
	perf_data =load_perf_information('performance.csv')
	# Plot the libraries
	plot_dna(dna_designs, dna_design_order, 'variants_library.pdf', plot_params, perf_data)
	plot_dna(dna_designs, dna_design_order, 'variants_library.png', plot_params, perf_data)

if __name__ == "__main__":
 	main()
 	
