"""
New DNAplotlib script for handling input and output
"""
import sbol, csv
import datatype as dt, draw, render as rd

###############################################################################
# Input
###############################################################################

###############################################################################
# Output
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

# recursive function for extracting module and components and saving as design 
def extract_module_and_components(doc, design, mod_defs):
	md_list = []
	for md in mod_defs:
		module = dt.Module(design, md.displayId)

		for fc in md.functionalComponents:
			c_role, c_type = fetch_comp_role_type(doc, fc.displayId)
			print(module.name)
			print(renderer.glyph_soterm_map.get(c_role[0]))
			print(fc.displayId)
			part = dt.Part(module, fc.displayId, renderer.glyph_soterm_map.get(c_role[0]))
			print(part)
			if c_type[0] == sbol.BIOPAX_DNA:
	   			module.add_part(part)
	   		else:
	   			module.add_other_part(part)

		# add submodules
		if len(md.modules) != 0:
			smd_list = []
			for submd in md.modules:
				smd_list.append(fetch_module_def(doc, submd.displayId))
			module.children += extract_module_and_components(doc, design, smd_list)

		md_list.append(module)

	return md_list

# initialize renderer
renderer = rd.GlyphRenderer()

# open doc
doc = sbol.Document()
doc.read('test_design3_2.xml')

# create design 
design = dt.Design('root_design')
extract_module_and_components(doc, design, doc.moduleDefinitions)
m_frames = get_module_frames(design.modules) # default setting
fig, ax = plt.subplots(1, figsize=(8,10))
ax.set_xlim(XMIN, XMAX)
ax.set_ylim(YMIN, YMAX)
ax.set_axis_off()

# render modules
draw_all_modules(m_frames, design.modules)

plt.show()


