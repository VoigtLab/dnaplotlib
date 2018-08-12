"""
New DNAplotlib script for handling input and output
"""
import sbol, csv
import datatype as dt, render as rd, draw
import matplotlib.pyplot as plt


# plt const
XMIN, XMAX = -60., 60.
YMIN, YMAX = -60., 60.

###############################################################################
# Import  
###############################################################################

# helper function for extract_module_and_components
# match functional component with component definition
def fetch_comp_role_type(doc, comp_id):
	for comp in doc.componentDefinitions:
		if comp.displayId == comp_id:
			return comp.roles, comp.types

# helper function for extract_module_and_components
# match module with module definition
def fetch_module_def(doc, md_id):
	for md in doc.moduleDefinitions:
		if md.displayId == md_id:
			return md

def add_parts_to_module(docu, mod, fc_list):
	for i in range(len(fc_list)):
		fc = fc_list[i]
		c_role, c_type = fetch_comp_role_type(docu, fc.displayId)
		# create part
		if len(c_role) == 0: # when part is RNA, does not have so term 
			part = dt.Part(mod, fc.displayId, 'RNA')
		else:
			part = dt.Part(mod, fc.displayId, renderer.glyph_soterm_map.get(c_role[0]))
		# add part to strand / non-strand
		if c_type[0] == sbol.BIOPAX_DNA:
   			mod.add_part(part)
   		else:
   			mod.add_other_part(part)

# recursive function for extracting module and components 
# return list of modules to be saved in design
def extract_module_and_components(doc, design, mod_defs):
	md_list = []
	for md in mod_defs:
		module = dt.Module(design, md.displayId)
		add_parts_to_module(doc, module, md.functionalComponents)
		
		# add submodules
		if len(md.modules) != 0:
			smd_list = []
			for submd in md.modules:
				smd_list.append(fetch_module_def(doc, submd.displayId))
			module.children += extract_module_and_components(doc, design, smd_list)

		md_list.append(module)

	return md_list

###############################################################################
# Export
###############################################################################
# helper function for get_module_and_components
# return type of other part
def get_other_part_type(other_part_name):
	if other_part_name == 'RNA':
		return sbol.BIOPAX_RNA
	return sbol.BIOPAX_PROTEIN

# TODO: save interaction into sbol file
def save_interaction_from_design(doc, interactions):
	for interaction in interactions:
		md = sbol.ModuleDefinition('random_module')
		print('module created')
		interaction1 = md.interactions.create('interaction1') # inhibition
		interaction1.type = 'SBO:0000169'
		participation1 = md.participation.create(func_comp1, 'http://identifiers.org/biomodels.sbo/SBO:0000020') # inhibitor 
		participation2 = md.participate.create(func_comp2, 'http://identifiers.org/biomodels.sbo/SBO:0000642') # inhibited
		interaction1.add_participations([participation1, participation2])
		print('interaction added!')

# helper function for save_module_and_components_from_design
# add extension to save frame (width, height, originX, originY)
def save_frame_into_file(sbol_def, width, height, x, y):
	sbol_def.width = sbol.FloatProperty(sbol_def.this, 'http://dnaplotlib.org#Width', '0', '1', width)  
	sbol_def.height = sbol.FloatProperty(sbol_def.this, 'http://dnaplotlib.org#Height', '0', '1', height)  
	sbol_def.xcoord = sbol.FloatProperty(sbol_def.this, 'http://dnaplotlib.org#XCoordinate', '0', '1', x)  
	sbol_def.ycoord = sbol.FloatProperty(sbol_def.this, 'http://dnaplotlib.org#YCoordinate', '0', '1', y)  

# helper function for save_module_and_components_from_design
# save part as component definition
def save_part_as_component_definition(docu, part, part_type):
	part_rd = rd.GlyphRenderer()
	comp = sbol.ComponentDefinition(part.name, sbol.BIOPAX_DNA)
	if part_type != sbol.BIOPAX_RNA:
		comp.roles = part_rd.get_so_term(part_type)
	func_comp = md.functionalComponents.create(comp.displayId)
	func_comp.definition = comp
	save_frame_into_file(comp, part.frame.width, part.frame.height, part.frame.origin[0], part.frame.origin[1])
	doc.addComponentDefinition(comp)

# recursive file export func 
# get modules and components 
def save_module_and_components_from_design(doc, modules, count=1):
	submodules = []
	for m in modules:
		md = sbol.ModuleDefinition('md_%d_%d' % (m.level, count))
		count += 1
		submodules.append(md)
		save_frame_into_file(md, m.frame.width, m.frame.height, m.frame.origin[0], m.frame.origin[1])
		
		# save parts on strand 
		if m.part_list is not None:
			for part in m.part_list.parts:
				save_part_as_component_definition(doc, part, part.type)
		
		# save parts not on strand
		for opart in m.other_parts:
			op_biopax_type = get_other_part_type(op.name)
			save_part_as_component_definition(doc, opart, op_biopax_type)
		
		# check children modules
		if len(m.children) != 0:
			subcount = 0
			m_list = get_module_and_components(d, m.children)
			md.assemble(m_list)

		doc.addModuleDefinition(md)

	return submodules


# initialize renderer
renderer = rd.GlyphRenderer()

# open doc
doc = sbol.Document()
doc.read('test_design5.xml')

# create design 
design = dt.Design('design5')
design.add_module(extract_module_and_components(doc, design, doc.moduleDefinitions))
design.print_design()
m_frames = draw.get_module_frames(design.modules) # default setting


fig, ax = plt.subplots(1, figsize=(8,10))
ax.set_xlim(XMIN, XMAX)
ax.set_ylim(YMIN, YMAX)
ax.set_axis_off()

# render modules
draw.draw_all_modules(ax, m_frames, design.modules)

plt.show()


