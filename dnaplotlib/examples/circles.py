'''rough script for rendering three ORI
'''

fig = plt.figure(figsize=(5,5))
ax = fig.add_subplot(111)
# need to set axis first 
ax.set_xlim(-50.0, 50.0)
ax.set_ylim(-50.0, 50.0)

#insulator = renderer.draw_glyph(ax, 'Insulator', (0.0, 0.0), 33., 0)
ori1 = renderer.draw_glyph(ax, 'ORI', (-30.0, 0.0), 5., 0)
ori2 = renderer.draw_glyph(ax, 'ORI', (-10.0, 20.0), 22., np.pi)
ori3 = renderer.draw_glyph(ax, 'ORI', (10.0, 0.0), 8., np.pi/3.)
ax.annotate('(-30.0, 0.0)', xy=[-30.0, 0.0], ha='center')
ax.annotate('(-10.0, 20.0)', xy=[-10.0, 20.0], ha='center')
ax.annotate('(10.0, 0.0)', xy=[10.0, 0.0], ha='center')


ax.set_axis_off()
plt.show()