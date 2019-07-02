'''script for drawing all sypported part glyphs
need to be moved outside the example directory 
at the same directory as render.py
'''

import render
import matplotlib.pyplot as plt


fig, ax = plt.subplots(1, figsize=(10,10))
# need to set axis first 
ax.set_xlim(-50.0, 50.0)
ax.set_ylim(-50.0, 50.0)

renderer = render.GlyphRenderer()

promoter = renderer.draw_glyph(ax, 'Promoter', (-40., 0.), 5., 0.)
insulator = renderer.draw_glyph(ax, 'Insulator', (-33., 0.), 5., 0.)
ax.plot(-33,0,marker='o', c='r')
ax.plot(-33,5.,marker='o', c='r')
ax.plot(-28,0,marker='o', c='r')
aptamer = renderer.draw_glyph(ax, 'Aptamer', (-26., 0.), 5., 0.)
ori = renderer.draw_glyph(ax, 'OriginOfReplication', (-19., 0.), 5., 0)
res = renderer.draw_glyph(ax, 'RibosomeEntrySite', (-12., 0.), 5., 0.)
cds = renderer.draw_glyph(ax, 'CDS', (-5., 0.), 5., 0.)
terminator = renderer.draw_glyph(ax, 'Terminator', (2., 0.), 5., 0.)
macromolecule = renderer.draw_glyph(ax, 'Macromolecule', (10., 0.), 5., 0.)
protein = renderer.draw_glyph(ax, 'Unspecified', (-21., 10.), 5., 0.)

ax.set_axis_off()
plt.show()
