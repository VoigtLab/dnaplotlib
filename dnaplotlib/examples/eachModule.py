'''rough script for rendering three glyphs in 3 modules
need to be moved outside the example directory 
at the same directory as render.py
'''

import render
import matplotlib.pyplot as plt

# default setting
strand1 = render.StrandRenderer()
strand2 = render.StrandRenderer()
strand3 = render.StrandRenderer()

renderer = render.GlyphRenderer()

module1 = render.ModuleRenderer()
module2 = render.ModuleRenderer()
module3 = render.ModuleRenderer()


fig = plt.figure(figsize=(5,5))
ax = fig.add_subplot(111)
# need to set axis first 
ax.set_xlim(-50.0, 50.0)
ax.set_ylim(-50.0, 50.0)

p1 = renderer.draw_glyph(ax, 'Promoter', (-20.0, 0), 5., 0)
strand1.add_glyphs([p1])
bb1 = strand1.draw_backbone_strand(ax, 0.0, 1.5)
module1.add_parts([p1, bb1])
module_frame1 = module1.draw_module_box2(ax)

cds2 = renderer.draw_glyph(ax, 'CDS', (0.0, -2), 5., 0)
strand2.add_glyphs([cds2])
bb2 = strand2.draw_backbone_strand(ax, 0., 1.5)
module2.add_parts([cds2, bb2])
module_frame2 = module2.draw_module_box2(ax)
print(module_frame2)

i3 = renderer.draw_glyph(ax, 'Insulator', (20.0, -5), 10., 0.)
strand3.add_glyphs([i3])
bb3 = strand3.draw_backbone_strand(ax, 0., 1.5)
module3.add_parts([i3, bb3])
module_frame3 = module3.draw_module_box2(ax)
print(module_frame3)

ax.set_axis_off()
plt.show()
