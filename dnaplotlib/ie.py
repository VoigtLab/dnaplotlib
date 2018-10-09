"""
Import & Export
: script for importing / exporting sbol file 
"""
import sbol, csv, sys
import datatype as dt, render as rd, draw 
import matplotlib.pyplot as plt


# plt const
XMIN, XMAX = -60., 60.
YMIN, YMAX = -60., 60.
STANDARD_INTERACTION = 'interaction_n'

###############################################################################
# Import  
###############################################################################

# helper function for extract_full_modules
# match functional component with component definition
def fetch_cd_by_fc(cd_list, fc_id):
	for comp in cd_list:
		if comp.displayId == fc_id:
			return comp

# helper function for extract_full_modules
# match module with module definition
def fetch_module_def(doc, md_id):
	for md in doc.moduleDefinitions:
		if md.displayId == md_id:
			return md

# helper function to extract_full_modules
# get parts from raw_module then add to module
def add_parts_to_module(mod, raw_md, cd_list):
	renderer = rd.GlyphRenderer()
	for fc in raw_md.functionalComponents:
		c = fetch_cd_by_fc(cd_list, fc.displayId)
		
		# create part
		if len(c.roles) == 0: # when part is RNA, does not have so term 
			part = dt.Part(mod, fc.displayId, 'RNA')
		else:
			part = dt.Part(mod, fc.displayId, renderer.glyph_soterm_map.get(c.roles[0]))
		
		# add part to strand / non-strand
		if c.types[0] == sbol.BIOPAX_DNA:
   			mod.add_part(part)
   		else:
   			mod.add_other_part(part)
   	return mod

# recursive function for extracting module and components from design 
# return list of modules with component definitions 
def extract_full_modules(doc, design, module_ids):
	md_list = []

	while len(module_ids) != 0:
		for md in doc.moduleDefinitions:
			if md.displayId in module_ids:
				module = dt.Module(design, md.displayId)
				module_ids.remove(md.displayId)
				module = add_parts_to_module(module, md, doc.componentDefinitions)
				
				# add submodules
				if len(md.modules) != 0:
					submod_ids = list(map(lambda sm: sm.displayId, md.modules))
					module.children = extract_full_modules(doc, design, submod_ids)
					submod_ids = list(map(lambda sm: sm.displayId, md.modules)) # need again, since deleted
					module_ids = [i for i in module_ids if i not in submod_ids]
				md_list.append(module)

	return md_list

# helper function for extract interactions
# return part corresponding with participant id 
def fetch_part_by_id(modules, ids):
	parts = []
	for m in modules:
		if m.part_list is not None:
			for p in m.part_list.parts:
				if p.name in ids:
					parts.append(p)
		for op in m.other_parts:
			if op.name in ids:
				parts.append(op)
		# recursively search for parts
		parts += fetch_part_by_id(m.children, ids)
	return parts

# helper function for assemble_raw_interactions
# receive interaction sboltype, return interaction type
def fetch_interaction_type(i_type):
	if i_type == 'http://identifiers.org/biomodels.sbo/SBO:0000168':
		return 'control'
	elif i_type == 'http://identifiers.org/biomodels.sbo/SBO:0000179':
		return 'degradation'
	elif i_type == 'http://identifiers.org/biomodels.sbo/SBO:0000169':
		return 'inhibition'
	elif i_type == 'http://identifiers.org/biomodels.sbo/SBO:0000589':
		return 'process'
	elif i_type == 'http://identifiers.org/biomodels.sbo/SBO:0000170':
		return 'stimulation'
	sys.exit('unidentified interaction found while fetching interaction type.')

# helper func for assemble_raw_interactions
# get raw parts then return the correct order of parts 
def assemble_parts_by_order(order1, p_list1, p_list2):
	if order1[-1] == 0:
		return p_list1 + p_list2
	return p_list2 + p_list1

# helper function for extract_interactions
# assemble raw intrxn from md into interxn
def assemble_raw_interactions(interxn_lists, modules):
	complete, incomplete = [], []
	for i in interxn_lists:
		interxn_type = fetch_interaction_type(i.types[0]) # assume first types as primary rendering
		parts = fetch_part_by_id(modules, list(map(lambda p: p.displayId, i.participations)))

		if i.displayId.count('_') == 1: # has single part
			complete.append((interxn_type, parts))
		else:
			i_index = i.displayId[:len(STANDARD_INTERACTION)] 
			if i_index in [inc[0] for inc in incomplete]:
				for inc in incomplete:
					if i_index == inc[0]:
						parts = assemble_parts_by_order(i.displayId, parts, inc[1])
						complete.append((interxn_type, parts))
			else:
				incomplete.append([i_index, parts])
	
	return complete

# extract interaction from document then return list of interaction datatype
def extract_interactions(document, design_modules):
	i_list = []
	interactions = []
	# first extract all interactions from document
	for md in document.moduleDefinitions:
		for interaction in md.interactions:
			i_list.append(interaction)

	# assemble interactions (esp intermodular interactions)
	i_list = assemble_raw_interactions(i_list, design_modules)

	for i_type, parts in i_list:
		if len(parts)==1:
			interactions.append(dt.Interaction(i_type, parts[0]))
		elif len(parts)==2:
			interactions.append(dt.Interaction(i_type, parts[0], parts[1]))
		else:
			sys.exit('too many parts found while importing interactions: found %d parts' % len(parts))
	return interactions

# func to read doc and produce design
def read_doc_into_design(doc):
	design = dt.Design('default_design')
	design.add_module(extract_full_modules(doc, design, 
			list(map(lambda m: m.displayId, doc.moduleDefinitions))))
	design.add_interaction(extract_interactions(doc, design.modules))
	return design


###############################################################################
# Export
###############################################################################

# helper function for save_modules_and_components
# return type of other part - need to add small molecule / complex 
def get_other_part_biopax_type(other_part_name):
	if other_part_name == 'RNA':
		return sbol.BIOPAX_RNA
	return sbol.BIOPAX_PROTEIN

# helper function for save_interactions
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


# helper function for save_interactions
# receive doc and interaction, return functionalComponents and modules of parts involved in interaction
def find_fcs_mds_of_interaction(doc, interxn):
	if interxn.part_end is None:
		find = [interxn.part_start.name]
	else: 
		find = [interxn.part_start.name, interxn.part_end.name]
	fc_list, md_list = [], []
	for md in doc.moduleDefinitions:
		for fc in md.functionalComponents:
			if fc.displayId in find:
				index = find.index(fc.displayId)
				md_list.insert(index, md)
				fc_list.insert(index, fc)
	return fc_list, md_list
			
# helper function for save_interactions
# receive interaction, return roles of parts_start, parts_end
def find_roles_of_interaction_parts(intrxn):
	roles = []

	if intrxn.part_end is None:
		parts = [intrxn.part_start]
	else: 
		parts = [intrxn.part_start, intrxn.part_end]

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
def save_interactions(doc, des_interactions):
	for interaction in des_interactions: 
		displayId = ('interaction_%d' % des_interactions.index(interaction))
		fcs, mds = find_fcs_mds_of_interaction(doc, interaction)
		roles = find_roles_of_interaction_parts(interaction)

		# create participation 
		participant_list = []
		for participant, role in zip(fcs, roles):
			pp = sbol.Participation(participant.displayId, participant.identity)
			pp.roles = role
			participant_list.append(pp)

		if len(participant_list) == 1 or len(list(set(mds))) == 1: # single interaction 
			new_interxn = sbol.Interaction(displayId, get_interaction_type(interaction))
			new_interxn.participations.add(participant_list[0])
			mds[0].interactions.add(new_interxn)

		else:
			for partp, md in zip(participant_list, mds): # save as two interactions 
				new_interxn = sbol.Interaction(displayId + '_%d' % participant_list.index(partp), get_interaction_type(interaction))
				new_interxn.participations.add(partp)
				md.interactions.add(new_interxn)

# helper function for save_modules_and_components_from_design
# add extension to save frame (width, height, originX, originY)
def save_frame_into_file(sbol_def, width, height, x, y):
	sbol_def.width = sbol.FloatProperty(sbol_def.this, 'http://dnaplotlib.org#Width', '0', '1', width)  
	sbol_def.height = sbol.FloatProperty(sbol_def.this, 'http://dnaplotlib.org#Height', '0', '1', height)  
	sbol_def.xcoord = sbol.FloatProperty(sbol_def.this, 'http://dnaplotlib.org#XCoordinate', '0', '1', x)  
	sbol_def.ycoord = sbol.FloatProperty(sbol_def.this, 'http://dnaplotlib.org#YCoordinate', '0', '1', y)  

# helper function for save_modules_and_components_from_design
# save part as component definition
def save_part_as_component_definition(docu, md, part, bp_type):
	part_rd = rd.GlyphRenderer()
	comp = sbol.ComponentDefinition(part.name, bp_type)
	if bp_type != sbol.BIOPAX_RNA: # RNA does not have so term
		comp.roles = part_rd.get_so_term(part.type)
	func_comp = md.functionalComponents.create(comp.displayId)
	func_comp.definition = comp
	save_frame_into_file(comp, part.frame.width, part.frame.height, part.frame.origin[0], part.frame.origin[1])
	docu.addComponentDefinition(comp)

# recursive file export func 
# get modules and components 
def save_modules_and_components(doc, modules, count=1):
	submodules = []
	for m in modules:
		md = sbol.ModuleDefinition('md_%d_%d' % (m.level, count))
		count += 1
		submodules.append(md)
		save_frame_into_file(md, m.frame.width, m.frame.height, m.frame.origin[0], m.frame.origin[1])
		
		# save parts on strand 
		if m.part_list is not None:
			for part in m.part_list.parts:
				save_part_as_component_definition(doc, md, part, sbol.BIOPAX_DNA)
		
		# save parts not on strand
		for opart in m.other_parts:
			op_biopax_type = get_other_part_biopax_type(opart.name)
			save_part_as_component_definition(doc, md, opart, op_biopax_type)
		
		# check children modules
		if len(m.children) != 0:
			subcount = 0
			m_list = save_modules_and_components(doc, m.children)
			md.assemble(m_list)

		doc.addModuleDefinition(md)

	return submodules


# func to save design into sbol document 
def save_design_into_doc(doc, design):
	save_modules_and_components(doc, design.modules)
	save_interactions(doc, design.interactions)

# open doc
'''doc = sbol.Document()
doc.addNamespace('http://dnaplotlib.org#', 'dnaplotlib')

# defaults
design = dt.create_test_design6_2()
m_frames = draw.get_module_frames(design.modules)
fig, ax = plt.subplots(1, figsize=(8,10))
ax.set_xlim(XMIN, XMAX)
ax.set_ylim(YMIN, YMAX)
ax.set_axis_off()

draw.draw_all_modules(ax, m_frames, design.modules)
draw.draw_all_interactions(ax, design.interactions)

save_design_into_doc(doc, design)
doc.write('test_6_2.xml')

plt.show()
'''
'''
doc = sbol.Document()
doc.read('test_6_2.xml')

# create design 
design_import = read_doc_into_design(doc)
design_import.print_design()

print('-------------------')
design_original = dt.create_test_design6_2()
design_original.print_design()

m_frames = draw.get_module_frames(design_original.modules) # default setting


design = dt.create_test_design6_1()
m_frames = draw.get_module_frames(design.modules)
fig, ax = plt.subplots(1, figsize=(8,10))
ax.set_xlim(XMIN, XMAX)
ax.set_ylim(YMIN, YMAX)
ax.set_axis_off()

draw.draw_all_modules(ax, m_frames, design.modules)
draw.draw_all_interactions(ax, design.interactions)


'''

#design = dt.create_test_design5()
'''doc = sbol.Document()
doc.read('test_6_2.xml')

# UPDATES
m = doc.moduleDefinitions['foo']
import_design = dt.import_design_from_file(module)

design_imported = 
design.print_design()'''

design = dt.create_test_design8()
'''doc = sbol.Document()
doc.read('test_8.xml')
design_import = dt.Design('design8')
design_import.add_module(
	extract_full_modules(doc, design_import, 
		list(map(lambda m: m.displayId, doc.moduleDefinitions))))
design_import.add_interaction(extract_interactions(doc, design_import.modules))
design_import.print_design()'''

m_frames = draw.get_module_frames(design.modules)

fig, ax = plt.subplots(1, figsize=(8,10))
ax.set_xlim(XMIN, XMAX)
ax.set_ylim(YMIN, YMAX)
ax.set_axis_off()

user_customization = [
	{'target': 'p1c',
	'size': 1.5,
	'facecolor': 'lime'},
	{'target': 'r1',
	'facecolor': 'lime'	
	},
	{'target': 'p2c',
	'size': 1.5,
	'facecolor': 'yellow'},
	{'target': 'r2',
	'facecolor': 'yellow'	
	}
]

draw.draw_all_modules(ax, m_frames, design.modules, user_params=user_customization)
draw.draw_all_interactions(ax, design.interactions)

'''document = sbol.Document()
document.addNamespace('http://dnaplotlib.org#', 'dnaplotlib')
save_design_into_doc(document, design)
document.write('test_8.xml')'''
plt.show()
