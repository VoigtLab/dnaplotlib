'''Two Interlocking Regulatory Circuits
# move to upper directory for rendering
'''
import sbol
import  datatype as dt, draw
import matplotlib.pyplot as plt

# CONST
XMIN, XMAX = -60., 60.
YMIN, YMAX = -60., 60.

design = dt.create_test_design8()
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

draw.draw_all_modules(ax, m_frames, design.modules)
draw.draw_all_interactions(ax, design.interactions)

plt.show()