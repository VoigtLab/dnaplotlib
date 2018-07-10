'''Example of glyph rotation
'''

fig = plt.figure(figsize=(5,5))
ax = fig.add_subplot(111)
# need to set axis first 
ax.set_xlim(-50.0, 50.0)
ax.set_ylim(-50.0, 50.0)

#for glyph_type in renderer.glyphs_library.keys():
promoter = renderer.draw_glyph(ax, 'Promoter', (-30.0, 0.0), 10., 0)
promoter = renderer.draw_glyph(ax, 'Promoter', (0.0, 0.0), 10., np.pi/2.)
promoter = renderer.draw_glyph(ax, 'Promoter', (30.0, 0.0), 10., np.pi)

#annotation
ax.annotate('(-30.0, 0.0)', xy=[-30.0, 0.0], ha='center')
ax.annotate('(0.0, 0.0)', xy=[0.0, 0.0], ha='center')
ax.annotate('(30.0, 0.0)', xy=[30.0, 0.0], ha='center')
ax.set_axis_off()
plt.show()