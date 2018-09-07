'''standard script for rendering test designs
More test designs provided in datatype.py

need to be moved outside the example directory 
at the same directory as render.py
'''

import datatype as dt, ie, draw
import matplotlib.pyplot as plt, sbol



# plt const
XMIN, XMAX = -60., 60.
YMIN, YMAX = -60., 60.

# get test design 
design = dt.create_test_design5() # can be different test design (more in datatype.py)
m_frames = draw.get_module_frames(design.modules) # default setting

# render test design
fig, ax = plt.subplots(1, figsize=(8,10))
ax.set_xlim(XMIN, XMAX)
ax.set_ylim(YMIN, YMAX)
ax.set_axis_off()

# render modules
draw.draw_all_modules(ax, m_frames, design.modules)

# render interaction 
draw.draw_all_interaction(ax, design.interactions)

# export to xml file 
document = sbol.Document()
document.addNamespace('http://dnaplotlib.org#', 'dnaplotlib')
ie.save_modules_and_components_from_design(document, design.modules)
ie.save_interaction_from_design(document, design)
document.write('test_design5.xml')

# display canvas
plt.show()