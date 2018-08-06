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
# Input
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
# Output
###############################################################################


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


