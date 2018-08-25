"""
draw 
: script for bringing datatype and render func together 
: mainly for calculating position
"""
import sys, numpy as np, sbol
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

# generic helper function 
# return module width & height 
def get_module_width_height(glyph_count, glyph_size, module_space, other_part_count):
	# width: assume horizontal rendering in one circuit (refer to ppt)
	m_width = glyph_count * glyph_size + module_space * (glyph_count - 1) + module_space * 6
	if other_part_count > glyph_count:
		m_width += (other_part_count - glyph_count) * (module_space + glyph_size)
		
	# height: assume other parts all in one line 
	m_height = glyph_size + 3.5 * module_space
	if other_part_count != 0:
		m_height += glyph_size + module_space * 2
	return m_width, m_height

# helper function for get_origin_list
# return vertically stacked origin (refer to ppt)
def get_vertical_stacked_origins(module_count):
	origin_list = []

	start_x = -WIDTH
	if module_count < 3: start_y = 0.
	else: start_y = HEIGHT

	for i in range(module_count):
		origin_list.append([start_x, start_y])
		if start_y != - (HEIGHT * 2): start_y -= HEIGHT
		else:
			start_x = 0.
			start_y = HEIGHT
	return origin_list 

# helper function for get_horizontal_stacked_origin
# cumulative in the sense of recursion
def get_cumulative_parts_count(module):
	parts_count = 0
	if module.part_list is not None:
		parts_count += len(module.part_list.parts)
	if len(module.children) != 0:
		for m in module.children:
			parts_count += get_cumulative_parts_count(m)
	return parts_count

# helper function for get_horizontal_stacked_origin
def get_cumulative_other_parts_count(module):
	other_parts_count = 0
	other_parts_count += len(module.other_parts)
	if len(module.children) != 0:
		for m in module.children:
			other_parts_count += get_cumulative_other_parts_count(m)
	return other_parts_count

# helper function for get_horizontal_stacked_origin
def get_cumulative_layers_count(module):
	layer_count = 0
	if len(module.children) != 0:
		layer_count += 1 + get_cumulative_layers_count(module.children[0])
	return layer_count

# helper func for get_origin_list
# return horizontally stacked origin (refer to ppt)
def get_horizontal_stacked_origins(submodules, glyph_sz, module_sp, original_point):
	list_origin = []
	dynamic_x, static_y = original_point

	for submodule in submodules:
		list_origin.append([dynamic_x, static_y])
		p_width, p_height = get_module_width_height(get_cumulative_parts_count(submodule),
			glyph_sz, module_sp, get_cumulative_other_parts_count(submodule))
		dynamic_x += p_width + (4 + get_cumulative_layers_count(submodule))* module_sp 

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
				[origins[i][0] + 2 * space, 
				origins[i][1] + 1.5 * space],
				True)
		else:
			if module.part_list != None:
				parts_count = len(module.part_list.parts)
			else: parts_count = 0
			width, height = get_module_width_height(parts_count, glyph_size, space, len(module.other_parts))
			frame_list.append(rd.Frame(width=width, height=height, origin=origins[i]))
			module.level = module_level

	if has_frame_box and len(frame_list) != 0.:
		frame_list.append(get_biggest_module_frame(frame_list, space))
	
	return frame_list

# helper function for drawing module 
# return list of position for other parts depending on other part count
def __get_other_part_pos(o_p_count, frame, part_sz, glyph_sz, m_sp):
	o_p_pos = []
	# initialize first pos 
	dyn_x = frame.origin[0] + (frame.width / 2.) - (part_sz / 2.)
	fixed_y = frame.origin[1] + (m_sp * 3.5) + glyph_sz
	if o_p_count % 2 == 0:
		dyn_x += part_sz / 2.
	dyn_x -= (m_sp + part_sz) * (o_p_count / 2) 
	# shifting pos
	for i in range(o_p_count):
		o_p_pos.append([dyn_x, fixed_y])
		dyn_x += glyph_sz + m_sp 

	return o_p_pos

# function that draw module
def draw_module(ax, module, module_frame, glyph_size, module_spacer, haveBackbone=True):
	glyph_pos = [module_frame.origin[0] + 3 * module_spacer, 
		module_frame.origin[1] + 1.5 * module_spacer]
	renderer = rd.GlyphRenderer()
	strand_rd = rd.StrandRenderer()
	module_rd = rd.ModuleRenderer()	

	# check whether module is empty or not 
	if module.part_list == None:
		if len(module.children) != 0:
			return module_rd.draw_empty_module_box(ax, module_frame)
		elif len(module.other_parts) == 0: return

	# draw each glyphs in module part list
	else: 
		module.part_list.position = glyph_pos 
		for part in module.part_list.parts:
			part.frame = rd.Frame(width=glyph_size, height=glyph_size, origin=glyph_pos)
			child = renderer.draw_glyph(ax, part.type, glyph_pos, glyph_size, 0.)
			strand_rd.add_glyphs(child)
			module_rd.add_parts(child)
			glyph_pos = [glyph_pos[0] + glyph_size + module_spacer, glyph_pos[1]]

	# draw backbone 
	if haveBackbone and module.part_list != None:
		bb = strand_rd.draw_backbone_strand(ax, glyph_pos[1], module_spacer)
		module_rd.add_parts(bb)
		module.part_list.position = bb['frame'].origin

	# draw other parts 
	if len(module.other_parts) != 0:
		op_pos_list = __get_other_part_pos(len(module.other_parts), module_frame, glyph_size, glyph_size, module_spacer)
		other_part_frames = []
		for i, other_part in enumerate(module.other_parts):
			other_part.frame = rd.Frame(width=glyph_size, height=glyph_size, origin=op_pos_list[i])
			other_part_frames.append(other_part.frame)
			other_child = renderer.draw_glyph(ax, other_part.type, op_pos_list[i], glyph_size, 0.)
			module_rd.add_parts(other_child)

	# step of deciding whether to draw  module frame box 
		# do not draw module frame box if only has other part 
		if module.part_list == None:
			return get_biggest_module_frame(other_part_frames, module_spacer)
	# draw frame module box 
	return module_rd.draw_module_box(ax, module_spacer, module_spacer)

# helper function for draw interaction
# draw interaction arrow body when y diff < than height limit 
def get_3part_interaction_coord(ax, start_frame, end_frame, y_ofset):
	start_x = start_frame.origin[0] + start_frame.width / 2.
	start_y = start_frame.origin[1] + start_frame.height + INTERACTION_SPACER 
	end_x = end_frame.origin[0] + end_frame.width / 2.
	end_y = end_frame.origin[1] + end_frame.height + INTERACTION_SPACER
	c1x, c1y = start_x, start_y + y_ofset 
	c2x, c2y = end_x, c1y
	return [[start_x, start_y], [c1x, c1y], [c2x, c2y], [end_x, end_y]]
	

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
def get_5part_interaction_coord(ax, start_frame, end_frame, y_1_ofset, y_2_ofset):
	start_x = start_frame.origin[0] + start_frame.width / 2.
	start_y = start_frame.origin[1] + start_frame.height + INTERACTION_SPACER 
	end_x = end_frame.origin[0] + end_frame.width / 2.
	end_y = end_frame.origin[1] + end_frame.height + INTERACTION_SPACER
	c1x, c1y = start_x, start_y + y_1_ofset 
	c2x, c2y = _determine_5part_interaction_middle_x(start_x, end_x), c1y
	c3x, c3y = _determine_5part_interaction_middle_x(start_x, end_x), end_y + y_2_ofset
	c4x, c4y = end_x, c3y
	return [[start_x, start_y], [c1x, c1y], [c2x, c2y], [c3x, c3y], [c4x, c4y], [end_x, end_y]]

# helper function for get_valid_offset
# check whether the randomly selected  y_ofset has duplicate in past list of coordinates
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

	return y_offset, start_y, from_y 

# function that draw one interaction 
# (offset can be user specified or randomly generated)
def draw_all_interaction(ax, all_intercn, coordlist=[], user_specified_y_offset=None):
	for intercn in all_intercn:
		y_offset, start_y, from_y = get_valid_offset(coordlist, intercn.part_start, intercn.part_end, user_specified_y_offset)
		
		# distinguish between 3 part / 5 part interaction  
		if abs(start_y - from_y) < HEIGHT:
			coords = get_3part_interaction_coord(ax, intercn.part_start.frame, intercn.part_end.frame, y_offset)
		else:
			coords = get_5part_interaction_coord(ax, intercn.part_start.frame, intercn.part_end.frame, y_offset, y_offset)
		
		# update coords
		interaction_rd = rd.InteractionRenderer(intercn.type, intercn.part_start, intercn.part_end, coords, INTERACTION_SPACER)
		intercn.coordinates = coords 
		coordlist += coords

		interaction_rd.draw_interaction(ax)

# recursively draw all modules
def draw_all_modules(ax, m_frames, raw_modules, index=0):
	for module in raw_modules: 
		if len(module.children) == 0: # base case
			actual_frame = draw_module(ax, module, m_frames[index], 
				GLYPHSIZE - RECURSE_DECREMENT * 2 * module.level,
				SPACER)
		else:
			index = draw_all_modules(m_frames, module.children, index)
			actual_frame = draw_module(ax, module, m_frames[index], 
				GLYPHSIZE - RECURSE_DECREMENT * 2 * module.level,
				SPACER, False)
		
		module.frame = actual_frame
		index += 1

	return index 


'''func to be put to ie
'''
# helper function for get_module_and_components
# return type of other part
def get_other_part_type(other_part_name):
	if other_part_name == 'RNA':
		return sbol.BIOPAX_RNA
	return sbol.BIOPAX_PROTEIN

# helper function for save_interaction_from_design 
# receive interaction datatype, return sbo term 
def get_interaction_type(interxn):
	if interxn.type == 'control':
		return 'http://identifiers.org/biomodels.sbo/SBO:0000168'
	elif interxn.type == 'degradation':
		return 'http://identifiers.org/biomodels.sbo/SBO:0000179'
	elif interxn.type == 'inhibition':
		return 'http://identifiers.org/biomodels.sbo/SBO:0000169'
	elif interxn.type == 'process':
		return 'http://identifiers.org/biomodels.sbo/SBO:0000589'
	elif interxn.type == 'stimulation':
		return 'http://identifiers.org/biomodels.sbo/SBO:0000170'
	sys.exit('unidentified interaction found while getting interaction type.')

# helper function for save_interaction_from_design
# receive doc and interaction, return functionalComponents of parts involved in interaction
def find_mds_of_interaction(doc, interxn):
	find = [interxn.part_start.name, interxn.part_end.name]
	md_list = []
	for md in doc.moduleDefinitions:
		for fc in md.functionalComponents:
			if fc.displayId in find:
				index = find.index(fc.displayId)
				md_list.insert(index, md)
	return md_list

# helper function for save_interaction_from_design
# receive doc and interaction, return 
def find_comps_of_interaction(doc, interxn):
	find = [interxn.part_start.name, interxn.part_end.name]
	comp_list = []
	for comp in doc.componentDefinitions:
		if comp.displayId in find:
			comp_list.insert(find.index(comp.displayId), comp)
	return comp_list
			
# helper function for save_interaction_from_design
# receive interaction, return roles of parts_start, parts_end
def find_roles_of_interaction_parts(intrxn):
	parts = [intrxn.part_start, intrxn.part_end]
	roles = []
	for p in parts:
		if p.type == 'Promoter':
			roles.append('http://identifiers.org/biomodels.sbo/SBO:0000598')
		elif intrxn.type == 'control':
			if p == parts[0]:
				roles.append('http://identifiers.org/biomodels.sbo/SBO:0000019')
			else:
				roles.append('http://identifiers.org/biomodels.sbo/SBO:0000644')
		elif intrxn.type == 'degradation':
			roles.append('http://identifiers.org/biomodels.sbo/SBO:0000010')
		elif intrxn.type == 'inhibition':
			if p == parts[0]:
				roles.append('http://identifiers.org/biomodels.sbo/SBO:0000020')
			else:
				roles.append('http://identifiers.org/biomodels.sbo/SBO:0000642')
		elif intrxn.type == 'process':
			if p == parts[0]:
				roles.append('http://identifiers.org/biomodels.sbo/SBO:0000645')
			else:
				roles.append('http://identifiers.org/biomodels.sbo/SBO:0000011')
		elif intrxn.type == 'stimulation':
			if p == parts[0]:
				roles.append('http://identifiers.org/biomodels.sbo/SBO:0000459')
			else:
				roles.append('http://identifiers.org/biomodels.sbo/SBO:0000643')

	return roles 

# save all interactions from design into doc 
def save_interaction_from_design(doc, des):
	for index in range(len(des.interactions)):
		# create interaction 
		interaction = des.interactions[index]
		displayId = ('interaction_%d' % index)
		mds = find_mds_of_interaction(doc, interaction)
		comps = find_comps_of_interaction(doc, interaction)
		roles = find_roles_of_interaction_parts(interaction)

		# create participation 
		participants_list = []
		for participant, role in zip(comps, roles):
			pp = sbol.Participation(displayId, participant)
			pp.roles = role
			participants_list.append(pp)

		# save into md 
		if mds[0].displayId == mds[1].displayId: # intramodular interaction
			new_interxn = sbol.Interaction(displayId, get_interaction_type(interaction))
			new_interxn.participations = participants_list
			mds[0].interactions.add(new_interxn)
		else:
			count = 0
			for partp, md in zip(participants_list, mds):
				new_interxn = sbol.Interaction(displayId + '_' + str(count), get_interaction_type(interaction))
				count += 1
				new_interxn.participations.add(partp)
				md.interactions.add(new_interxn)

# helper function for save_module_and_components_from_design
# add extension to save frame (width, height, originX, originY)
def save_frame_into_file(sbol_def, width, height, x, y):
	sbol_def.width = sbol.FloatProperty(sbol_def.this, 'http://dnaplotlib.org#Width', '0', '1', width)  
	sbol_def.height = sbol.FloatProperty(sbol_def.this, 'http://dnaplotlib.org#Height', '0', '1', height)  
	sbol_def.xcoord = sbol.FloatProperty(sbol_def.this, 'http://dnaplotlib.org#XCoordinate', '0', '1', x)  
	sbol_def.ycoord = sbol.FloatProperty(sbol_def.this, 'http://dnaplotlib.org#YCoordinate', '0', '1', y)  

# helper function for save_module_and_components_from_design
# save part as component definition
def save_part_as_component_definition(docu, md, part, part_type):
	part_rd = rd.GlyphRenderer()
	comp = sbol.ComponentDefinition(part.name, sbol.BIOPAX_DNA)
	if part_type != sbol.BIOPAX_RNA:
		comp.roles = part_rd.get_so_term(part_type)
	func_comp = md.functionalComponents.create(comp.displayId)
	func_comp.definition = comp
	save_frame_into_file(comp, part.frame.width, part.frame.height, part.frame.origin[0], part.frame.origin[1])
	docu.addComponentDefinition(comp)

# recursive file export func 
# get modules and components 
def save_modules_and_components_from_design(doc, modules, count=1):
	submodules = []
	for m in modules:
		md = sbol.ModuleDefinition('md_%d_%d' % (m.level, count))
		count += 1
		submodules.append(md)
		save_frame_into_file(md, m.frame.width, m.frame.height, m.frame.origin[0], m.frame.origin[1])
		
		# save parts on strand 
		if m.part_list is not None:
			for part in m.part_list.parts:
				save_part_as_component_definition(doc, md, part, part.type)
		
		# save parts not on strand
		for opart in m.other_parts:
			op_biopax_type = get_other_part_type(opart.name)
			save_part_as_component_definition(doc, md, opart, op_biopax_type)
		
		# check children modules
		if len(m.children) != 0:
			subcount = 0
			m_list = get_module_and_components(d, m.children)
			md.assemble(m_list)

		doc.addModuleDefinition(md)

	return submodules

# get test design 
design = dt.create_test_design5()
m_frames = get_module_frames(design.modules) # default setting

# render test design
fig, ax = plt.subplots(1, figsize=(8,10))
ax.set_xlim(XMIN, XMAX)
ax.set_ylim(YMIN, YMAX)
ax.set_axis_off()

# render modules
draw_all_modules(ax, m_frames, design.modules)

# automatically render interaction 
draw_all_interaction(ax, design.interactions)

# export to xml file 
document = sbol.Document()
document.addNamespace('http://dnaplotlib.org#', 'dnaplotlib')
save_modules_and_components_from_design(document, design.modules)
save_interaction_from_design(document, design)
document.write('test_design5.xml')

# display canvas
plt.show()




