"""
draw dataype
: script for bringing datatype and render func together 
"""
import sys, numpy as np 
import datatype as dt, render as rd 
import matplotlib.pyplot as plt, matplotlib.patches as p, matplotlib.path as mpath

# default rendering const
MAX_MODULE = 8
GLYPHSIZE = 6.
SPACER = 1.5 
RECURSE_DECREMENT = .5
XMIN, XMAX = -60., 60.
YMIN, YMAX = -60., 60.
WIDTH, HEIGHT = 50., 25. # default setting for level 1 module & interaction
INTERACTION_SPACER = 1.5
INTERACTION_OFFSET_MIN, INTERACTION_OFFSET_MAX = 4, 7
INTERACTION_FILL_ZSCORE = 10.


# generic helper function 
# return module width & height 
def get_module_width_height(glyph_count, glyph_size, module_space, has_other_part):
	# width: assume horizontal rendering in one circuit (refer to ppt)
	m_width = glyph_count * glyph_size + module_space * (glyph_count - 1) + module_space * 6
	# height: assume other parts all in one line 
	m_height = glyph_size + 3.5 * module_space
	if has_other_part:
		m_height += glyph_size + module_space
	return m_width, m_height

# helper function for get_origin_list
# return vertically stacked origin (refer to ppt)
def get_vertical_stacked_origins(module_count):
	origin_list = []

	start_x = -WIDTH
	if module_count < 3:
		start_y = 0.
	else:
		start_y = HEIGHT

	for i in range(module_count):
		origin_list.append([start_x, start_y])
		if start_y != - (HEIGHT * 2):
			start_y -= HEIGHT
		else:
			start_x = 0.
			start_y = HEIGHT
	return origin_list 

# helper func for get_origin_list
# return horizontally stacked origin (refer to ppt)
def get_horizontal_stacked_origins(submodules, glyph_sz, module_sp, original_point):
	list_origin = []
	p_width = 0
	dynamic_x, static_y = original_point

	for submodule in submodules:
		list_origin.append([dynamic_x, static_y])
		if submodule.part_list is not None:
			p_width, p_height = get_module_width_height(len(submodule.part_list.parts),
			glyph_sz, module_sp, len(submodule.other_parts) != 0)
		else: 
			p_width = 0.
		dynamic_x += p_width + module_sp 

	return list_origin


# function that takes modules from design and return list of origins for the modules 
def get_origin_list(modules, module_level, g_size, m_space_offset, original_p=None):
	# check number of modules 
	if len(modules) > MAX_MODULE:
		sys.exit("Draw Error: DNAplotlib cannot render more than 8 modules. Current design has %d modules." % len(modules))
	
	origins = []
	# module level 0 - vertical stacking 
	if module_level == 0:
		origins = get_vertical_stacked_origins(len(modules))
	# module level 1,2 - horizontal stacking 
	elif module_level == 1 or module_level == 2:
		origins = get_horizontal_stacked_origins(modules, g_size, m_space_offset, original_p)
	else:
		sys.exit("Draw Error: DNAplotlib cannot render beypnd level 3 submodules.")

	return origins

# helper function for get_module_frames
# takes the list of submodules and return frame for module containing all 
def get_biggest_module_frame(framelist, space_offset):
	max_x, max_y = (np.finfo(np.float128).min for i in range(2))
	min_x, min_y = (np.finfo(np.float128).max for i in range(2))
	for frame in framelist:
		if min_x > frame.origin[0]:
			min_x = frame.origin[0]
		if max_x < frame.origin[0] + frame.width:
			max_x = frame.origin[0] + frame.width
		if min_y > frame.origin[1]:
			min_y = frame.origin[1]
		if max_y < frame.origin[1] + frame.height:
			max_y = frame.origin[1] + frame.height 

	return rd.Frame(width=(max_x - min_x) + 4 * space_offset, 
		height=(max_y - min_y) + 3.5 * space_offset, 
		origin=[min_x - 2 * space_offset, min_y - 1.5 * space_offset])

# recursive function that takes modules from design 
# and return list of frame for the modules 
def get_module_frames(modules, module_level=0, glyph_size=GLYPHSIZE, space=SPACER, submodule_origin=None, has_frame_box=False):
	frame_list = []
	origins = get_origin_list(modules, module_level, glyph_size, space, submodule_origin)

	for i, module in enumerate(modules):
		if len(module.children) != 0.:
			frame_list += get_module_frames(module.children, 
				module_level + 1,
				GLYPHSIZE - RECURSE_DECREMENT * 2, space, 
				[origins[i][0] + 2 * space, origins[i][1] + 1.5 * space],
				True)
		else:
			width, height = get_module_width_height(len(module.part_list.parts),
				glyph_size, space, len(module.other_parts) != 0)
			frame_list.append(rd.Frame(width=width, height=height, origin=origins[i]))
			module.level = module_level

	if has_frame_box and len(frame_list) != 0.:
		frame_list.append(get_biggest_module_frame(frame_list, space))
	
	return frame_list

# function that draw module
def draw_module(ax, module, module_frame, glyph_size, module_spacer, haveBackbone=True):
	glyph_pos = [module_frame.origin[0] + 3 * module_spacer, 
		module_frame.origin[1] + 1.5 * module_spacer]
	renderer = rd.GlyphRenderer()
	strand_rd = rd.StrandRenderer()
	module_rd = rd.ModuleRenderer()	

	# check whether module is empty or not 
	if module.part_list == None:
		return module_rd.draw_empty_module_box(ax, module_frame)

	# draw each glyphs in module part list
	module.part_list.position = glyph_pos 
	for part in module.part_list.parts:
		part.frame = rd.Frame(width=glyph_size, height=glyph_size, origin=glyph_pos)
		child = renderer.draw_glyph(ax, part.type, glyph_pos, glyph_size, 0.)
		strand_rd.add_glyphs(child)
		module_rd.add_parts(child)
		glyph_pos = [glyph_pos[0] + glyph_size + module_spacer, glyph_pos[1]]

	# draw backbone 
	if haveBackbone:
		bb = strand_rd.draw_backbone_strand(ax, glyph_pos[1], module_spacer)
		module_rd.add_parts(bb)
		module.part_list.position = bb['frame'].origin
	
	return module_rd.draw_module_box(ax, module_spacer, module_spacer)


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
	print('list of coords')
	print(coords)
	for i,coord in enumerate(coords):
		if i == (len(coords) - 1): break # skip last one to prevent indexOutOfBound Error
		curr_x, next_x = coord[0], coords[i + 1][0]
		curr_y, next_y = coord[1], coords[i + 1][1]
		cx, nx = __convert_coord_into_scalar_0_1(curr_x, next_x, ax.get_xlim())
		cy, ny = __convert_coord_into_scalar_0_1(curr_y, next_y, ax.get_ylim())
		
		if i % 2 == 0: # vertical
			print('vertical body drawn')
			ax.axvline(x=curr_x, ymin=cy, ymax=ny, c=color)
		else: # horizontal
			print('horizontal body drawn')
			ax.axhline(y=curr_y, xmin=cx, xmax=nx, c=color)

	return coords

# helper function for draw interaction
# draw interaction arrow body when y diff < than height limit 
def draw_3part_interaction(ax, start_frame, end_frame, y_ofset, i_color):
	start_x = start_frame.origin[0] + start_frame.width / 2.
	start_y = start_frame.origin[1] + start_frame.height + INTERACTION_SPACER 
	end_x = end_frame.origin[0] + end_frame.width / 2.
	end_y = end_frame.origin[1] + end_frame.height + INTERACTION_SPACER
	c1x, c1y = start_x, start_y + y_ofset 
	c2x, c2y = end_x, c1y
	return __draw_arrow_body(ax, [ [start_x, start_y], [c1x, c1y], [c2x, c2y], [end_x, end_y] ], i_color)
	

# helper function for draw_5part_interaction
# determine c2/c3x for different frame interaction 
def _determine_5part_interaction_middle_x(startx, endx):
	xintrn_spacer = SPACER
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
	return __draw_arrow_body(ax, [ [start_x, start_y], [c1x, c1y], [c2x, c2y], [c3x, c3y], [c4x, c4y], [end_x, end_y] ], i_color)
	

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

def check_has_duplicate_y(list_of_c, y_ofset, y1, y2):
	for c in list_of_c:
		if c[1] == y_ofset + y1: return True
		if c[1] == y_ofset + y2: return True
	return False

# helper function for draw_all_interaction
def get_valid_offset(c_list, start_glyph, from_glyph, user_specified):
	start_y = start_glyph.frame.origin[1] + (GLYPHSIZE - 2 * RECURSE_DECREMENT * start_glyph.parent_module.level)
	from_y = from_glyph.frame.origin[1] + (GLYPHSIZE - 2 * RECURSE_DECREMENT * from_glyph.parent_module.level)
	
	if user_specified is not None:
		return user_specified, start_y, from_y
		
	while user_specified is None:
		y_offset = (np.random.random_sample() * 3) + np.random.randint(INTERACTION_OFFSET_MIN, INTERACTION_OFFSET_MAX)
		if not check_has_duplicate_y(c_list, y_offset, start_y, from_y): break

	#print('start y: %f' % (start_y + y_offset))
	#print('from y: %f' % (from_y + y_offset))
	return y_offset, start_y, from_y 

# function that draw one interaction 
# (offset can be user specified or randomly generated)
def draw_all_interaction(ax, all_intercn, coordlist=[], user_specified_y_offset=None):
	for intercn in all_intercn:
		y_offset, start_y, from_y = get_valid_offset(coordlist, intercn.part_start, intercn.part_end, user_specified_y_offset)

		# distinguish interaction to get arrowhead & color
		intercn_color = draw_interaction_arrowhead(intercn)
		
		# distinguish between 3 part / 5 part interaction  
		if abs(start_y - from_y) < HEIGHT:
			coords = draw_3part_interaction(ax, intercn.part_start.frame, intercn.part_end.frame, y_offset, intercn_color)
		else:
			coords = draw_5part_interaction(ax, intercn.part_start.frame, intercn.part_end.frame, y_offset, y_offset, intercn_color)
		
		# update coords
		intercn.coordinates = coords 
		coordlist += coords

# recursively draw all modules
def draw_all_modules(m_frames, raw_modules, index=0):
	for module in raw_modules:
		# base case
		if len(module.children) == 0:
			actual_frame = draw_module(ax, module, m_frames[index], 
				GLYPHSIZE - RECURSE_DECREMENT * 2 * module.level,
				SPACER)

		# recursive case
		else:
			index = draw_all_modules(m_frames, module.children, index)
			actual_frame = draw_module(ax, module, m_frames[index], 
				GLYPHSIZE - RECURSE_DECREMENT * 2 * module.level,
				SPACER, False)
		# ways to check rendering frames
		'''print('hoping frame: ')
		print(m_frames[index])
		print('actual frame:')
		print(actual_frame)'''
		index += 1

	return index 

# get test design 
design = dt.create_test_design()
design.print_design()
m_frames = get_module_frames(design.modules) # default setting

# render test design
fig, ax = plt.subplots(1, figsize=(8,10))
ax.set_xlim(XMIN, XMAX)
ax.set_ylim(YMIN, YMAX)
ax.set_axis_off()

# render modules
draw_all_modules(m_frames, design.modules)

# automatically render interaction 
draw_all_interaction(ax, design.interactions)

for i in design.interactions:
	print(i.coordinates)

plt.show()


