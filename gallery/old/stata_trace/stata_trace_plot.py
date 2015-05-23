#!/usr/bin/env python
"""
	Example of trace plotting from a GeneClusterLibrary object.
"""

import dnaplotlib as dpl
import gene_cluster_library as gcl
import gene_cluster_analysis as gca
import gene_cluster_visualization as gcv

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

# Load the Stata nif library data
nifs = gcl.GeneClusterLibrary()
nifs.load('./data/clean_nif_stata_library.txt')

# Example plot testing full variant rendering
fig = plt.figure(figsize=(8,4))
ax = fig.add_subplot(3,1,1)
gcv.plot_variant_arch(ax, nifs, '25', start_idx=1, end_idx=-2, linewidth=1.2)
ax = fig.add_subplot(3,1,2)
gcv.plot_variant_arch(ax, nifs, '10', start_idx=1, end_idx=-2, linewidth=1.2)
ax = fig.add_subplot(3,1,3)
gcv.plot_variant_arch(ax, nifs, '1', start_idx=1, end_idx=-2, linewidth=1.2)
plt.tight_layout()
fig.savefig('./variant_rendering.pdf', transparent=True)

# Example plot of the whole library
fig = plt.figure(figsize=(14,84))
gcv.plot_library_arch(fig, nifs, linewidth=1.2, scaleadjust=0.6)
plt.tight_layout()
fig.savefig('library_rendering.pdf', transparent=True)

# Load the traces for predicted and measured
phys_reads = gca.load_stata_strand_data('./data/phys_depths3.csv')

# Example plot of architecture with Tx traces
gs = gridspec.GridSpec(2, 1, height_ratios=[2,1])
fig = plt.figure(figsize=(14,4))
ax_arch = plt.subplot(gs[1])
ax_traces = plt.subplot(gs[0],sharex=ax_arch)
# Update the part attributes to influence the rendering


# Plot the variant
gcv.plot_traces_with_arch(ax_arch, [ax_traces], nifs, '75', [phys_reads['75']], start_idx=1, 
	                      end_idx=-2, linewidth=1.2, scaleadjust=0.7)
plt.tight_layout()
fig.savefig('arch_and_trace.pdf', transparent=True)

# Example plot of architecture with multiple Tx traces
gs = gridspec.GridSpec(3, 1, height_ratios=[2,2,1])
fig = plt.figure(figsize=(14,6))
ax_arch = plt.subplot(gs[2])
ax_traces = [plt.subplot(gs[0],sharex=ax_arch), plt.subplot(gs[1],sharex=ax_arch)]
gcv.plot_traces_with_arch(ax_arch, ax_traces, nifs, '75', [phys_reads['75'], phys_reads['80']], start_idx=1, 
	                      end_idx=-2, linewidth=1.2, scaleadjust=0.7)
plt.tight_layout()
fig.savefig('arch_and_multiple_traces.pdf', transparent=True)

# Clear the plotting cache
plt.close('all')

