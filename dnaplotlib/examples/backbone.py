'''rough script for rendering two glyphs onto dna backbone
'''


fig = plt.figure(figsize=(5,5))
ax = fig.add_subplot(111)
# need to set axis first 
ax.set_xlim(-50.0, 50.0)
ax.set_ylim(-50.0, 50.0)

#for glyph_type in renderer.glyphs_library.keys():
p1 = renderer.draw_glyph(ax, 'Promoter', (-20.0, 0.0), 5., 0)
ori2 = renderer.draw_glyph(ax, 'ORI', (0.0, -2.5), 5., 0)
i3 = renderer.draw_glyph(ax, 'Insulator', (20.0, -2.5), 5., 0.)
strand.add_glyphs([p1, ori2, i3])
strand.draw_backbone_strand(ax, 0.0)

ax.set_axis_off()
plt.show()