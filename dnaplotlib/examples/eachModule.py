'''rough script for rendering three glyphs in 3 modules
need to be moved outside the example directory 
at the same directory as render.py
'''

from render import *
import matplotlib.pyplot as plt

# default setting
strand1 = StrandRenderer()
strand2 = StrandRenderer()
strand3 = StrandRenderer()

renderer = GlyphRenderer()

module1 = ModuleRenderer()
module2 = ModuleRenderer()
module3 = ModuleRenderer()


fig = plt.figure(figsize=(5,5))
ax = fig.add_subplot(111)
# need to set axis first 
ax.set_xlim(-50.0, 50.0)
ax.set_ylim(-50.0, 50.0)

p1 = renderer.draw_glyph(ax, 'Promoter', (-20.0, -40.0), 50., 0)
strand1.add_glyphs([p1])
bb1 = strand1.draw_backbone_strand(ax, 0.0)
module1.add_parts([p1, bb1])
module_frame1 = module1.draw_module_box(ax)

ori2 = renderer.draw_glyph(ax, 'ORI', (0.0, -2.5), 5., 0)
strand2.add_glyphs([ori2])
bb2 = strand2.draw_backbone_strand(ax, 0.)
module2.add_parts([ori2, bb2])
module_frame2 = module2.draw_module_box(ax)
print(module_frame2)

i3 = renderer.draw_glyph(ax, 'Insulator', (20.0, -2.5), 10., 0.)
strand3.add_glyphs([i3])
bb3 = strand3.draw_backbone_strand(ax, 0.)
module3.add_parts([i3, bb3])
module_frame3 = module3.draw_module_box(ax)
print(module_frame3)

ax.set_axis_off()
plt.show()
