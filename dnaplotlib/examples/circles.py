'''rough script for rendering three ORI
need to be moved outside the example directory 
at the same directory as render.py
'''

import render
import matplotlib.pyplot as plt, numpy as np

fig = plt.figure(figsize=(5,5))
ax = fig.add_subplot(111)
# need to set axis first 
ax.set_xlim(-50.0, 50.0)
ax.set_ylim(-50.0, 50.0)

renderer = render.GlyphRenderer()

#insulator = renderer.draw_glyph(ax, 'Insulator', (0.0, 0.0), 33., 0)
ori1 = renderer.draw_glyph(ax, 'OriginOfReplication', (-30.0, 0.0), 8., 0)
ori2 = renderer.draw_glyph(ax, 'OriginOfReplication', (-10.0, 20.0), 23., np.pi)
ori3 = renderer.draw_glyph(ax, 'OriginOfReplication', (10.0, 0.0), 11., np.pi/3.)
ax.annotate('(-30.0, 0.0)', xy=[-30.0, 0.0], ha='center')
ax.plot(-30, 0, c='r', marker='o')
ax.annotate('(-10.0, 20.0)', xy=[-10.0, 20.0], ha='center')
ax.annotate('(10.0, 0.0)', xy=[10.0, 0.0], ha='center')


ax.set_axis_off()
plt.show()