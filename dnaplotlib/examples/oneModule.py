'''
rough script for rendering three glyphs onto one module
need to be moved outside the example directory 
at the same directory as render.py
'''

import render
import matplotlib.pyplot as plt

# default setting
strand = render.StrandRenderer()
renderer = render.GlyphRenderer()
module = render.ModuleRenderer()

print(renderer.glyphs_library)
print('------------')
print(renderer.glyph_soterm_map)

fig = plt.figure(figsize=(5,5))
ax = fig.add_subplot(111)
# need to set axis first 
ax.set_xlim(-50.0, 50.0)
ax.set_ylim(-50.0, 50.0)

p1 = renderer.draw_glyph(ax, 'Promoter', (-20.0, 0.0), 10., 0)
ori2 = renderer.draw_glyph(ax, 'OriginOfReplication', (0.0, -5.), 10., 0)
i3 = renderer.draw_glyph(ax, 'Insulator', (20.0, -5.), 10., 0.)
strand.add_glyphs([p1, ori2, i3])
bb = strand.draw_backbone_strand(ax, 0., 1.5)
module.add_parts([p1, ori2, i3, bb])
module_frame = module.draw_module_box(ax, render.Frame(width=70, height=30, origin=(-30, -10)))

ax.set_axis_off()
plt.show()