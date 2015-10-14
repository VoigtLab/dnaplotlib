#!/usr/bin/env python
"""
	File input
"""

import dnaplotlib as dpl
import matplotlib.pyplot as plt
from matplotlib import gridspec

__author__  = 'Thomas Gorochowski <tom@chofski.co.uk>, Voigt Lab, MIT'
__license__ = 'OSI OSL 3.0'
__version__ = '1.0'


# Load the design from a GFF file
design = dpl.load_design_from_gff('plasmid.gff', 'chrom1', region=[1700, 15880])

# Create the DNAplotlib renderer
dr = dpl.DNARenderer()
part_renderers = dr.SBOL_part_renderers()

# Create the figure
fig = plt.figure(figsize=(5.0,0.6))
gs = gridspec.GridSpec(1, 1)
ax_dna = plt.subplot(gs[0])

# Redender the DNA to axis
start, end = dr.renderDNA(ax_dna, design, part_renderers)
ax_dna.set_xlim([start, end])
ax_dna.set_ylim([-15,15])
ax_dna.set_aspect('equal')
ax_dna.axis('off')

# Update subplot spacing
plt.subplots_adjust(left=0.01, right=0.99, top=0.99, bottom=0.01)

# Save the figure
fig.savefig('input_gff.pdf', transparent=True)
fig.savefig('input_gff.png', dpi=300)

# Clear the plotting cache
plt.close('all')
