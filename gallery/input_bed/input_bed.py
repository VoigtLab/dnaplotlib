#!/usr/bin/env python
"""
	File input
"""

import dnaplotlib as dpl
import matplotlib.pyplot as plt
from matplotlib import gridspec
import numpy as np

__author__  = 'Thomas Gorochowski <tom@chofski.co.uk>, Voigt Lab, MIT'
__license__ = 'MIT'
__version__ = '1.0'

# Load the design from a GFF file
cur_region = [1700, 15880]
design = dpl.load_design_from_gff('plasmid.gff', 'chrom1', region=cur_region)
profile_fwd = dpl.load_profile_from_bed('plasmid_fwd_profile.txt', 'chrom1', [0, 22953])
profile_rev = dpl.load_profile_from_bed('plasmid_rev_profile.txt', 'chrom1', [0, 22953])

# Create the DNAplotlib renderer
dr = dpl.DNARenderer(scale=10.0)
part_renderers = dr.trace_part_renderers()

# Create the figure
fig = plt.figure(figsize=(3.5,2.0))
gs = gridspec.GridSpec(2, 1, height_ratios=[1, 0.2])
ax_dna = plt.subplot(gs[1])

# Redender the DNA to axis
start, end = dr.renderDNA(ax_dna, design, part_renderers)
ax_dna.set_xlim(cur_region)
ax_dna.set_ylim([-5,8])
ax_dna.axis('off')

ax_profile = plt.subplot(gs[0])
ax_profile.fill_between(range(cur_region[0],cur_region[1]), profile_fwd[cur_region[0]:cur_region[1]], np.zeros(cur_region[1]-cur_region[0]), color=(0.5,0.5,0.5), edgecolor=(0.5,0.5,0.5), linewidth=1, zorder=1.5)
ax_profile.fill_between(range(cur_region[0],cur_region[1]), np.array(profile_rev[cur_region[0]:cur_region[1]])*-1.0, np.zeros(cur_region[1]-cur_region[0]), color=(1,0,0), edgecolor=(1,0,0), linewidth=1, zorder=1.5)
ax_profile.plot(cur_region, [0,0], color=(0,0,0), zorder=10)
ax_profile.set_xlim(cur_region)
ax_profile.axis('off')

# Update subplot spacing
plt.subplots_adjust(hspace=0.001, left=0.01, right=0.99, top=0.99, bottom=0.01)

# Save the figure
fig.savefig('input_bed.pdf', transparent=True)
fig.savefig('input_bed.png', dpi=300)

# Clear the plotting cache
plt.close('all')
