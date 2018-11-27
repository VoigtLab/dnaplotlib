"""
Import & Export
: script for importing / exporting sbol file 
"""
import sbol, numpy as np, csv, sys
import datatype as dt, render as rd, draw 
import matplotlib.pyplot as plt


# plt const
XMIN, XMAX = -60., 60.
YMIN, YMAX = -60., 60.
STANDARD_INTERACTION = 'interaction_n'

###############################################################################
# Import  
###############################################################################

# helper function to extract_full_modules
# get parts from raw_module then add to module
def add_parts_to_module(mod, raw_md, d):
	renderer = rd.GlyphRenderer()
	for fc in raw_md.functionalComponents:
		c = d.componentDefinitions[fc.displayId]
		
		# create part
		if sbol.BIOPAX_DNA in c.types:
			part = dt.Part(mod, fc.displayId, renderer.glyph_soterm_map.get(c.roles[0]))
   			mod.add_strand_part(part)
   		else:
			if sbol.BIOPAX_RNA in c.types:
				part = dt.Part(mod, fc.displayId, 'RNA')	
			elif sbol.BIOPAX_PROTEIN in c.types:
				part = dt.Part(mod, fc.displayId, 'Macromolecule')	
			else:
				part = dt.Part(mod, fc.displayId, 'Unspecified')
	   		mod.add_non_strand_part(part)			

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
				module = add_parts_to_module(module, md, doc)
				
				# add submodules
				if len(md.modules) != 0:
					submod_ids = list(map(lambda sm: sm.displayId, md.modules))
					module.children = extract_full_modules(doc, design, submod_ids)
					submod_ids = list(map(lambda sm: sm.displayId, md.modules)) # need again, since deleted
					module_ids = [i for i in module_ids if i not in submod_ids]
				md_list.append(module)
	return md_list

# helper function for extract interactions
# return part corresponding with participant id (assume 2 ids)
def fetch_part_by_id(modules, ids, fetched_part=[1,1]):
	for m in modules:
		if m.part_list is not None:
			for p in m.part_list.parts:
				if p.name in ids:
					fetched_part[ids.index(p.name)] = p
						
		for op in m.other_parts:
			if op.name in ids:
				fetched_part[ids.index(op.name)] = op

		# recursively search for parts
		fetched_part = fetch_part_by_id(m.children, ids, fetched_part)
	return fetched_part

# helper function for assemble_raw_interactions
# receive interaction sboltype, return interaction type
def fetch_interaction_type(i_type):
	if i_type == 'http://identifiers.org/biomodels.sbo/SBO:0000168':
		return 'control'
	elif i_type == 'http://identifiers.org/biomodels.sbo/SBO:0000179':
		return 'degradation'
	elif i_type == 'http://identifiers.org/biomodels.sbo/SBO:0000169':
		return 'inhibition'
	# note that process includes genetic production & non-covalent binding 
	elif i_type == 'http://identifiers.org/biomodels.sbo/SBO:0000589':
		return 'process'
	elif i_type == 'http://identifiers.org/biomodels.sbo/SBO:0000170':
		return 'stimulation'
	sys.exit('unidentified interaction found while fetching interaction type.')

# helper function for extract_interactions
# assemble raw intrxn from md into interxn
def assemble_raw_interactions(interxn_lists, modules):
	interactions = []
	for i in interxn_lists:
		interxn_type = fetch_interaction_type(i.types[0]) # assume first types as primary rendering
		parts = fetch_part_by_id(modules, list(map(lambda p: p.displayId, i.participations)))

		if len(parts)==1:
			interactions.append(dt.Interaction(interxn_type, parts[0]))
		elif len(parts)==2:
			interactions.append(dt.Interaction(interxn_type, parts[0], parts[1]))
		else:
			sys.exit('too many parts found while importing interactions: found %d parts' % len(parts))
	
	return interactions

# extract interaction from document then return list of interaction datatype
def extract_interactions(document, design_modules):
	i_list = []
	interactions = []
	# first extract all interactions from document
	for md in document.moduleDefinitions:
		for interaction in md.interactions:
			i_list.append(interaction)

	i_list = assemble_raw_interactions(i_list, design_modules)

	return i_list

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
	elif interxn.type == 'process' or interxn.type == 'genetic-process' or interxn.type == 'non-covalent-binding':
		return 'http://identifiers.org/biomodels.sbo/SBO:0000589'
	elif interxn.type == 'stimulation':
		return 'http://identifiers.org/biomodels.sbo/SBO:0000170'
	sys.exit('unidentified interaction found while getting interaction type.')


# helper function for save_interactions
# receive doc and interaction, return functionalComponents and modules of parts involved in interaction
def find_fcs_mds_of_interaction(doc, parts):
	find_module_by_name = []
	for p in parts:
		if p is not None: 
			find_module_by_name.append(p.parent_module.name)

	md_list, fc_list, cds_list = ([] for i in range(3))
	for f, p in zip(find_module_by_name, parts):
		that_module = doc.moduleDefinitions[f]
		md_list.append(that_module) 
		fc_list.append(that_module.functionalComponents[p.name])
		cds_list.append(doc.componentDefinitions[p.name])
	return md_list, fc_list, cds_list
			
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
		elif intrxn.type == 'process' or intrxn.type == 'genetic-process' or intrxn.type == 'non-covalent-binding':
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
		mds, fcs, cds = find_fcs_mds_of_interaction(doc, [interaction.part_start, interaction.part_end])
		roles = find_roles_of_interaction_parts(interaction)

		# create participation 
		participant_list = []
		for participant, role in zip(fcs, roles):
			pp = sbol.Participation(participant.displayId, participant.identity)
			pp.roles = role
			participant_list.append(pp)

		# Use proper MapsTo for intramodular interxns
		if mds[0].displayId != mds[-1].displayId:
			output_module_from = mds[0].setOutput(cds[0])
			input_module_to = mds[-1].setInput(cds[0])
			output_module_from.connect(input_module_to)

		# save as new interaction
		new_interxn = sbol.Interaction(displayId, get_interaction_type(interaction))
		for p in participant_list:
			new_interxn.participations.add(p)
		mds[-1].interactions.add(new_interxn) # save into last module in case of intermodular 

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
	if bp_type != sbol.BIOPAX_RNA: 
		comp.roles = part_rd.get_so_term(part.type)
	func_comp = md.functionalComponents.create(comp.displayId)
	func_comp.definition = comp
	save_frame_into_file(comp, part.frame.width, part.frame.height, part.frame.origin[0], part.frame.origin[1])
	docu.addComponentDefinition(comp)

# recursive file export func 
# get modules and components 
def save_modules_and_components(doc, modules):
	submodules = []
	for m in modules:
		md = sbol.ModuleDefinition(m.name)
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
			m_list = save_modules_and_components(doc, m.children)
			md.assemble(m_list)

		doc.addModuleDefinition(md)
	return submodules


# func to save design into sbol document 
def save_design_into_doc(doc, design):
	print('===== start saving dnaplotlib design into sbol document =====')
	doc.addNamespace('http://dnaplotlib.org#', 'dnaplotlib')
	save_modules_and_components(doc, design.modules)
	print('modules and components saved')
	save_interactions(doc, design.interactions)
	print('interactions saved')
	print('===== done saving design into the document! =====')

