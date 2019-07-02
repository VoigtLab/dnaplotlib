import numpy as np, datatype as dt, draw
from scipy.integrate import odeint
import matplotlib.pyplot as plt
from matplotlib import gridspec

design = dt.Design("NpHR Circuit")
module = dt.Module(design, 'md')

# NpHR 
p1 = dt.Part(module, 'EF1a_promoter1', 'Promoter')
cds1 = dt.Part(module, 'NpHR', 'CDS')
cds2 = dt.Part(module, 'EYFP', 'CDS')
t1 = dt.Part(module, 'term1', "Terminator")

# ChR2
p2 = dt.Part(module, 'EF1a_promoter2', 'Promoter')
cds3 = dt.Part(module, 'ChR2', 'CDS')
cds4 = dt.Part(module, 'mCherry', 'CDS')
t2 = dt.Part(module, 'term2', "Terminator")

module.add_strand_part([p1, cds1, cds2, t1, p2, cds3, cds4, t2])
design.add_module(module)

custom_rendering = [
	{'target': cds1.name,
	'facecolor': [0.38, 0.82, 0.32] 
	},
	{'target': cds2.name,
	'facecolor': [0.38, 0.82, 0.32] 
	},
	{'target': cds3.name,
	'facecolor': [1., 0., 0.] 
	},
	{'target': cds4.name,
	'facecolor': [1., 0., 0.] 
	}
]

m_frames = draw.get_module_frames(design.modules)

XMIN=-60
XMAX=60
YMIN=-60
YMAX=60

fig, ax = plt.subplots(1, figsize=(8,10))
ax.set_axis_off()
ax.set_xlim(XMIN, XMAX) # recommend XMIN=-60, XMAX=60
ax.set_ylim(YMIN, YMAX) # recommend YMIN=-60, YMAX=60


draw.draw_all_modules(ax, m_frames, design.modules, user_params=custom_rendering)


plt.show()