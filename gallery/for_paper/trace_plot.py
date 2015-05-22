#!/usr/bin/env python
"""
	Example of trace plotting from a GeneClusterLibrary object.
"""

# Import required modules
import gene_cluster_library as gcl
import gene_cluster_analysis as gca
import gene_cluster_visualization as gcv

# Standard Python modules
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

# Load the Stata nif library data
nifs = gcl.GeneClusterLibrary()
nifs.load('../stata_trace/data/clean_nif_stata_library.txt')

# Load the traces for predicted and measured
phys_reads = gca.load_stata_strand_data('../stata_trace/data/phys_depths3.csv')

# Example plot of architecture with Tx traces
gs = gridspec.GridSpec(2, 1, height_ratios=[2,1])
fig = plt.figure(figsize=(9,4))
ax_arch = plt.subplot(gs[1])
ax_traces = plt.subplot(gs[0], sharex=ax_arch)

# Update the nif data to include formatting data
part_colors = {}
part_colors['nifU'] = (0.76,0.47,0.76)
part_colors['nifS'] = (0.37,0.78,0.78)
part_colors['nifV'] = (0.78,0.78,0.49)
part_colors['nifW'] = (0.94,0.74,0.4)
part_colors['nifZ'] = (0.91,0.6,0.58)
part_colors['nifM'] = (0.5,0.77,0.56)



part_colors['nifV'] = (0.42,0.24,0.60)
part_colors['nifS'] = (0.12,0.47,0.71)
part_colors['nifZ'] = (0.20,0.63,0.17)
part_colors['nifM'] = (0.89,0.10,0.11)

# Promoters
part_colors['P1'] = (223/255.0,73/255.0,61/255.0)
part_colors['P2'] = (245/255.0,158/255.0,152/255.0)
part_colors['P3'] = (245/255.0,158/255.0,152/255.0)
# RBSs
strong_rbs = (57/255.0,181/255.0,74/255.0)
weak_rbs = (126/255.0,223/255.0,139/255.0)
part_colors['Ru1'] = weak_rbs
part_colors['Ru2'] = strong_rbs
part_colors['Rs1'] = weak_rbs
part_colors['Rs2'] = strong_rbs
part_colors['Rv1'] = weak_rbs
part_colors['Rv2'] = strong_rbs
part_colors['Rw1'] = weak_rbs
part_colors['Rw2'] = strong_rbs
part_colors['Rz1'] = weak_rbs
part_colors['Rz2'] = strong_rbs
part_colors['Rm1'] = weak_rbs
part_colors['Rm2'] = strong_rbs
# Terminator
part_colors['T1'] = (0,0,0)

# Update the color attribute for the promoters and CDSs
for part in nifs.parts.keys():
	if part in part_colors.keys():
		nifs.parts[part]['color'] = part_colors[part]
	if part[0] == 'R':
		nifs.parts[part]['x_extent'] = 12
		nifs.parts[part]['y_extent'] = 2.3

# Plot the variant
gcv.plot_traces_with_arch(ax_arch, [ax_traces], nifs, '75', [phys_reads['75']], start_idx=8 , 
	                      end_idx=-7, linewidth=1.2, scaleadjust=1.3)

# Format plot and save to file
ax_traces.set_ylabel('Strand Specific Read Depth')
plt.tight_layout()
fig.savefig('figure_plot_trace.pdf', transparent=True)

# Clear the plotting cache
plt.close('all')

