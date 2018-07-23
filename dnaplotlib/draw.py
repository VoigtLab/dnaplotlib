"""
draw dataype
: script for bringing datatype and render func together 
"""
import numpy as np 
import datatype as dt, render as rd 
import matplotlib.pyplot as plt, matplotlib.patches as p, matplotlib.path as mpath

# default rendering const
GLYPHSIZE = 6.
SPACER = 1.5 
RECURSE_DECREMENT = .5
XMIN, XMAX = -60., 60.
YMIN, YMAX = -60., 60.
WIDTH, HEIGHT = 50., 25. # for origin pos
WIDTHLIMIT, HEIGHTLIMIT = 45., 20. # limit for interaction
INTERACTION_SPACER = 1.5
INTERACTION_OFFSET_MIN, INTERACTION_OFFSET_MAX = 1, 4
INTERACTION_FILL_ZSCORE = 10.

# function that takes modules from design and return list of origins for the modules 
def get_origin_list(modules, module_level):
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

# helper function for get_module_frames
# takes the list of submodules and return frame for module containing all 
def __get_bigget_module_frame(framelist):
	width, height, origin = WIDTHLIMIT, HEIGHTLIMIT, [0., 0.]
	for frame in framelist:
		if frame.origin[0] < origin[0]:
			origin[0] = frame.origin[0] 
		if frame.origin[1] < origin[1]:
			origin[1] = frame.origin[1]
	return rd.Frame(width=width, height=height, origin=origin)

# recursive function that takes modules from design 
# and return list of frame for the modules 
def get_module_frames(modules, module_level, glyph_size=GLYPHSIZE, space=SPACER, has_submodule=False):
	frame_list = []
	origins = get_origin_list(modules, 0)

	for i, module in enumerate(modules):
		if module.part_list == None:
			frame_list += get_module_frames(module.children, 
				GLYPHSIZE - RECURSE_DECREMENT * 2,
				SPACER - RECURSE_DECREMENT, 
				True)
		else:
			# width: assume horizontal rendering in one circuit (refer to ppt)
			width = len(module.part_list.parts) * GLYPHSIZE + SPACER * (len(module.part_list.parts) - 1) + SPACER * 6
			# height: assume other parts all in one line 
			height = GLYPHSIZE + 3.5 * SPACER
			if len(module.other_parts) != 0.:
				height += GLYPHSIZE + SPACER
			frame_list.append(rd.Frame(width=width, height=height, origin=origins[i]))
	
	# add frame that contains every module 
	if has_submodule:
		frame_list.append(__get_bigget_module_frame(frame_list))

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
		part.frame = rd.Frame(width=GLYPHSIZE, height=GLYPHSIZE, origin=glyph_pos)
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

# private function for coordinate conversion
def __convert_coord_into_scalar_0_1(start, end, axis):
	axis_min, axis_max = axis
	dis = axis_max - axis_min 
	adjusted_start = abs(axis_min - start) / dis
	adjusted_end = adjusted_start + ((end - start) / dis)
	return adjusted_start, adjusted_end 

# helper function for draw_3/5part_interaction
# draw arrow body
def __draw_arrow_body(ax, coords, color):
	for i,coord in enumerate(coords):
		if i == (len(coords) - 1): break 
		curr_x, next_x = coord[0], coords[i + 1][0]
		curr_y, next_y = coord[1], coords[i + 1][1]
		cx, nx = __convert_coord_into_scalar_0_1(curr_x, next_x, ax.get_xlim())
		cy, ny = __convert_coord_into_scalar_0_1(curr_y, next_y, ax.get_ylim())
		
		if i % 2 == 0: # vertical
			ax.axvline(x=curr_x, ymin=cy, ymax=ny, c=color)
		else: # horizontal 
			ax.axhline(y=curr_y, xmin=cx, xmax=nx, c=color)

# helper function for draw interaction
# draw interaction arrow body when y diff < than height limit 
def draw_3part_interaction(ax, start_frame, end_frame, y_ofset, i_color):
	start_x = start_frame.origin[0] + start_frame.width / 2.
	start_y = start_frame.origin[1] + start_frame.height + INTERACTION_SPACER 
	end_x = end_frame.origin[0] + end_frame.width / 2.
	end_y = end_frame.origin[1] + end_frame.height + INTERACTION_SPACER
	c1x, c1y = start_x, start_y + y_ofset 
	c2x, c2y = end_x, c1y
	__draw_arrow_body(ax, [ [start_x, start_y], [c1x, c1y], [c2x, c2y], [end_x, end_y] ], i_color)
	return [c2y] # prevent this y coord for other interaction

# helper function for draw_5part_interaction
# determine c2/c3x for different frame interaction 
def _determine_5part_interaction_middle_x(startx, endx):
	xintrn_spacer = (WIDTH - WIDTHLIMIT) / 2.
	if startx < 0 and endx < 0:
		return -(WIDTH + xintrn_spacer)
	elif startx > 0 and endx > 0:
		return WIDTH + xintrn_spacer
	else:
		return -xintrn_spacer

# helper function for draw interaction
# draw interaction arrow body when y diff >= height limit 
def draw_5part_interaction(ax, start_frame, end_frame, y_1_ofset, y_2_ofset, i_color):
	start_x = start_frame.origin[0] + start_frame.width / 2.
	start_y = start_frame.origin[1] + start_frame.height + INTERACTION_SPACER 
	end_x = end_frame.origin[0] + end_frame.width / 2.
	end_y = end_frame.origin[1] + end_frame.height + INTERACTION_SPACER
	c1x, c1y = start_x, start_y + y_1_ofset 
	c2x, c2y = _determine_5part_interaction_middle_x(start_x, end_x), c1y
	c3x, c3y = _determine_5part_interaction_middle_x(start_x, end_x), end_y + y_2_ofset
	c4x, c4y = end_x, c3y
	__draw_arrow_body(ax, [ [start_x, start_y], [c1x, c1y], [c2x, c2y], [c3x, c3y], [c4x, c4y], [end_x, end_y] ], i_color)
	return [c2y, c3y] # prevent this y coord for other interaction 

# helper functions for draw_interaction_arrowhead
def draw_control_ah(ax, endframe, color):
	Path = mpath.Path
	start_x = endframe.origin[0] + endframe.width / 2.
	start_y = endframe.origin[1] + endframe.height + INTERACTION_SPACER
	edge = endframe.width / 5.

	path_data = [
		(Path.MOVETO, [start_x, start_y]),
		(Path.LINETO, [start_x - edge, start_y + edge]),
		(Path.LINETO, [start_x, start_y + (2 * edge)]),
		(Path.LINETO, [start_x + edge, start_y + edge]),
		(Path.LINETO, [start_x, start_y])
	]
	codes, verts = zip(*path_data)
	path = Path(verts, codes)
	patch = p.PathPatch(path, fill=True, edgecolor=color, facecolor='w', zorder=INTERACTION_FILL_ZSCORE)
	ax.add_patch(patch)

def draw_inhibition_ah(ax, endframe, color):
	x = endframe.origin[0] + endframe.width / 4.
	y = endframe.origin[1] + endframe.height + INTERACTION_SPACER 
	start_x, end_x = __convert_coord_into_scalar_0_1(x, x + endframe.width/2, ax.get_xlim())
	ax.axhline(y=y, xmin=start_x, xmax=end_x, c=color)

def draw_process_ah(ax, endframe, color):
	Path = mpath.Path
	start_x = endframe.origin[0] + endframe.width / 2.
	start_y = endframe.origin[1] + endframe.height + INTERACTION_SPACER
	edge = endframe.width / 5.

	path_data = [
		(Path.MOVETO, [start_x, start_y]),
		(Path.LINETO, [start_x - edge, start_y + edge]),
		(Path.LINETO, [start_x + edge, start_y + edge]),
		(Path.LINETO, [start_x, start_y])
	]
	codes, verts = zip(*path_data)
	path = Path(verts, codes)
	patch = p.PathPatch(path, fill=True, color=color)
	ax.add_patch(patch)

def draw_stimulation_ah(ax, endframe, color):
	Path = mpath.Path
	start_x = endframe.origin[0] + endframe.width / 2.
	start_y = endframe.origin[1] + endframe.height + INTERACTION_SPACER
	edge = endframe.width / 5.

	path_data = [
		(Path.MOVETO, [start_x, start_y]),
		(Path.LINETO, [start_x - edge, start_y + edge]),
		(Path.LINETO, [start_x + edge, start_y + edge]),
		(Path.LINETO, [start_x, start_y])
	]
	codes, verts = zip(*path_data)
	path = Path(verts, codes)
	patch = p.PathPatch(path, fill=True, edgecolor=color, facecolor='w', zorder=INTERACTION_FILL_ZSCORE)
	ax.add_patch(patch)

def draw_degradation_ah(ax, endframe, color):
	Path = mpath.Path
	# draw the same ah as process
	draw_process_ah(ax, endframe, color)
	# draw circle 
	r = endframe.width / 7
	start_x = endframe.origin[0] + endframe.width / 2.
	start_y = endframe.origin[1] + endframe.height 
	circle = p.Circle((start_x, start_y), r, ec=color, fc='w')
	ax.add_patch(circle)
	# draw circle bar 
	path_data = [
		(Path.MOVETO, [start_x + (r / np.sqrt(2)), start_y + (r / np.sqrt(2))]),
		(Path.LINETO, [start_x - (r / np.sqrt(2)), start_y - (r / np.sqrt(2))])
	]
	codes, verts = zip(*path_data)
	path = Path(verts, codes)
	patch = p.PathPatch(path, color=color)
	ax.add_patch(patch)

# helper function for draw_interaction 
# draw arrowhead and return interaction color 
def draw_interaction_arrowhead(interaction):
	if interaction.type == 'control':
		intercn_color = 'grey'
		draw_control_ah(ax, interaction.part_end.frame, intercn_color)
	elif interaction.type == 'degradation':
		intercn_color = 'brown'
		draw_degradation_ah(ax, interaction.part_end.frame, intercn_color)
	elif interaction.type == 'inhibition':
		intercn_color = 'red'
		draw_inhibition_ah(ax, interaction.part_end.frame, intercn_color)
	elif interaction.type == 'process':
		intercn_color = 'blue'
		draw_process_ah(ax, interaction.part_end.frame, intercn_color)
	elif interaction.type == 'stimulation':
		intercn_color = 'green'
		draw_stimulation_ah(ax, interaction.part_end.frame, intercn_color)
	return intercn_color

# function that draw one interaction 
# (offset can be user specified or randomly generated)
def draw_interaction(ax, intercn, ylist, user_specified_y_offset=None):
	# find valid y coord offset
	if user_specified_y_offset is not None:
		y_offset = user_specified_y_offset
	while user_specified_y_offset is None:
		y_offset = np.random.random_sample() + np.random.randint(INTERACTION_OFFSET_MIN, INTERACTION_OFFSET_MAX)
		start_y = intercn.part_start.frame.origin[1] + GLYPHSIZE
		from_y = intercn.part_end.frame.origin[1] + GLYPHSIZE
		if (start_y + y_offset) not in ylist and (from_y + y_offset) not in ylist:
			break

	# distinguish interaction to get arrowhead & color
	intercn_color = draw_interaction_arrowhead(intercn)
	
	# distinguish between 3 part / 5 part interaction  
	if abs(start_y - from_y) < HEIGHTLIMIT:
		ylist += draw_3part_interaction(ax, intercn.part_start.frame, intercn.part_end.frame, y_offset, intercn_color)
	else:
		ylist += draw_5part_interaction(ax, intercn.part_start.frame, intercn.part_end.frame, y_offset, y_offset, intercn_color)

	return ylist

# function that draw all interaction (without arrowhead)
def draw_all_interaction(ax, interactions):
	y_list = []
	for interaction in interactions:
		y_list = draw_interaction(ax, interaction, y_list)
		interaction.rendered_y = y_list

# get test design 
design = dt.create_test_design2()
design.print_design()
m_frames = get_module_frames(design.modules, 0)

# render test design
fig, ax = plt.subplots(1, figsize=(8,10))
ax.set_xlim(XMIN, XMAX)
ax.set_ylim(YMIN, YMAX)
ax.set_axis_off()

# render modules
for i, m_frame in enumerate(m_frames):
	actual_frame = draw_module(ax, design.modules[i], m_frame)

# automatically render interaction 
draw_all_interaction(ax, design.interactions)

plt.show()


