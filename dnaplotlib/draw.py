"""
draw dataype
: script for bringing datatype and render func together 
"""

import datatype as dt 
import render as rd 
import matplotlib.pyplot as plt, numpy as np 

# default const
GLYPHSIZE = 6.
XMIN, XMAX = -51., 50.
YMIN, YMAX = -51., 50.
WIDTH, HEIGHT = 50., 25.
SPACER = 1.5

# function that takes modules from design and return list of origins for the modules 
def get_origin_list(modules):
	# initialize origin params
	origins = []
	modules_left = len(modules)
	dynamic_x, dynamic_y = -WIDTH/2, 0.
	if modules_left > 1: dynamic_x = -WIDTH
	if modules_left > 4: dynamic_y = HEIGHT

	# iterate origin calculation
	for i in range(len(modules)):
		origins.append((dynamic_x, dynamic_y))
		modules_left -= 1
		if modules_left != 0:
			# just shift to left
			if dynamic_x < 0.: dynamic_x += WIDTH
			# shift right and down 
			else:
				if modules_left == 1: dynamic_x = -WIDTH/2
				else: dynamic_x = -WIDTH 
				dynamic_y -= HEIGHT

	return origins

# function that takes modules from design and return list of frame for the modules 
def get_module_frames(modules):
	frame_list = []
	origins = get_origin_list(modules)

	for i, module in enumerate(modules):
		# width: assume horizontal rendering in one circuit (refer to ppt)
		width = len(module.part_list.parts) * GLYPHSIZE 
		+ SPACER * (len(module.part_list.parts) - 1) 
		+ SPACER * 6
		# height: assume other parts all in one line 
		height = GLYPHSIZE + 3.5 * SPACER
		if len(module.other_parts) != 0.:
			height += GLYPHSIZE + SPACER
		frame_list.append(rd.Frame(width=width, height=height, origin=origins[i]))

	return frame_list

# function that draw module
def draw_module(ax, module, module_frame, haveBackbone=True):
	glyph_pos = [module_frame.origin[0] + 3 * SPACER, 
		module_frame.origin[1] + 1.5 * SPACER]
	renderer = rd.GlyphRenderer()
	strand_rd = rd.StrandRenderer()
	module_rd = rd.ModuleRenderer()
	module.part_list.position = glyph_pos 

	# draw each glyphs in module part list
	for part in module.part_list.parts:
		part.position = glyph_pos
		child = renderer.draw_glyph(ax, part.type, glyph_pos, GLYPHSIZE, 0.)
		strand_rd.add_glyphs(child)
		module_rd.add_parts(child)
		glyph_pos = [glyph_pos[0] + GLYPHSIZE + SPACER, glyph_pos[1]]
	
	# draw backbone 
	if haveBackbone:
		bb = strand_rd.draw_backbone_strand(ax, glyph_pos[1], SPACER)
		module_rd.add_parts(bb)
		module.part_list.position = bb['frame'].origin	
	module_box = module_rd.draw_module_box(ax, SPACER, SPACER)
	return module_box


# get test design 
design = dt.create_test_design2()
m_frames = get_module_frames(design.modules)

# render test design
fig, ax = plt.subplots(1, figsize=(8,10))
ax.set_xlim(XMIN, XMAX)
ax.set_ylim(YMIN, YMAX)
ax.set_axis_off()

for i, m_frame in enumerate(m_frames):
	actual_frame = draw_module(ax, design.modules[i], m_frame)

#draw_interaction(design.interactions[0])

plt.show()

