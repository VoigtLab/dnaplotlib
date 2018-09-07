'''
rough script for rendering two glyphs onto dna backbone
need to be moved outside the example directory 
at the same directory as render.py
'''

import matplotlib.pyplot as plt
import render



def main():
	print('executed')
	fig = plt.figure(figsize=(5,5))
	ax = fig.add_subplot(111)
	# need to set axis first 
	ax.set_xlim(-50.0, 50.0)
	ax.set_ylim(-50.0, 50.0)

	strand = render.StrandRenderer()
	renderer = render.GlyphRenderer()
	p1 = renderer.draw_glyph(ax, 'Promoter', (-20.0, 0.0), 5., 0)
	i3 = renderer.draw_glyph(ax, 'Insulator', (20.0, -2.5), 5., 0.)
	strand.add_glyphs([p1, i3])
	strand.draw_backbone_strand(ax, 0.0, 2)

	ax.set_axis_off()
	plt.show()


if __name__ == '__main__':
	print('what')
	main()


