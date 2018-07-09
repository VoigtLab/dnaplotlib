'''rough script for rendering two glyphs onto dna backbone
'''


fig = plt.figure(figsize=(5,5))
ax = fig.add_subplot(111)
# need to set axis first 
ax.set_xlim(-50.0, 50.0)
ax.set_ylim(-50.0, 50.0)

#for glyph_type in renderer.glyphs_library.keys():
insulator = renderer.draw_glyph(ax, 'Insulator', (0.0, 0.0), 20)
promoter = renderer.draw_glyph(ax, 'Promoter', (-30.0, 0.0), 20.)

strand.addGlyphs([insulator, promoter]) #primary sequence 
strand.drawBackboneStrand(ax)

# annotation for sanity check 
ax.annotate('(-30.0, 0.0)', xy=[-30.0, 0.0], ha='center')
ax.annotate('(20.0, 0.0)', xy=[20.0, 0.0], ha='center')

ax.set_axis_off()
plt.show()