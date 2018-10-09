import numpy as np, datatype as dt, draw
from scipy.integrate import odeint
import matplotlib.pyplot as plt
from matplotlib import gridspec

# drawing const
TETR_COLOR = [1.00, 0.75, 0.17]
LAC_COLOR = [0.38, 0.82, 0.32] # lac1
GAMMA_COLOR = [0.38, 0.65, 0.87] 

###############################################################################
# Initialize Simulation
# Initial concentration of mRNA and Protein for each repressor
###############################################################################
mtet, mlac, mgamma, tet, lac, gamma = initial = [1, 1, 1, 2, 1, 1]
# Non-dimensionalized production rate
alpha = 15
# Degradation Rate
beta = 2000
# Repressor/Promoter Leak
leak = 1
# Hill Coefficient
n = 8

def repressilator(y, t):
    mtet, mlac, mgamma, tet, lac, gamma = y
    
    dmtet = -mtet + (alpha / (1 + lac**n)) + leak
    dtet = -beta * (tet - mtet)
    
    dmlac = -mlac + (alpha / (1 + gamma**n)) + leak
    dlac = -beta * (lac - mlac)
    
    dmgamma = -mgamma + (alpha / (1 + tet**n)) + leak
    dgamma = -beta * (gamma - mgamma)
    return [dmtet, dmlac, dmgamma, dtet, dlac, dgamma]

t = np.arange(0, 30.1, 0.1)
ymtet, ymlac, ymgamma, ytet, ylac, ygamma = list(zip(*odeint(repressilator, initial, t)))
gs = gridspec.GridSpec(2, 1, top=0.8)

###############################################################################
# plot the genetic circuit
###############################################################################

design = dt.Design('repressilator')
module = dt.Module(design, 'md')

# tetR
p1 = dt.Part(module, 'tetR_promoter', 'Promoter')
cds1 = dt.Part(module, 'tetR', 'CDS')
module.add_part([p1, dt.Part(module, 'tetR_res', 'RibosomeEntrySite'),
			cds1, dt.Part(module, 'tetR_terminator', 'Terminator')])
# lac1
p2 = dt.Part(module, 'lac_promoter', 'Promoter')
cds2 = dt.Part(module, 'lac1', 'CDS')
module.add_part([p2, dt.Part(module, 'lac_res', 'RibosomeEntrySite'),
			cds2, dt.Part(module, 'lac_terminator', 'Terminator')])
# gamma 
p3 = dt.Part(module, 'gamma_promoter', 'Promoter')
cds3 = dt.Part(module, 'gamma', 'CDS')
module.add_part([p3, dt.Part(module, 'gamma_res', 'RibosomeEntrySite'),
			cds3, dt.Part(module, 'gamma_terminator', 'Terminator')])
design.add_module(module)
# interactions
design.add_interaction([
    dt.Interaction('inhibition', cds1, p3),
	dt.Interaction('inhibition', cds2, p1),
	dt.Interaction('inhibition', cds3, p2)])

# rendering 
m_frames = draw.get_module_frames(design.modules)
ax1 = plt.subplot(gs[0])
ax1.set_xlim(draw.XMIN/1.2, draw.XMAX)
ax1.set_ylim(0, draw.YMAX)
ax1.set_axis_off()

# draw modules
custom_rendering = [
    {'target': cds1.name,
    'size': 1.5,
    'facecolor': TETR_COLOR},
    {'target': cds2.name,
    'size': 1.5,
    'facecolor': LAC_COLOR},
    {'target': cds3.name,
    'size': 1.5,
    'facecolor': GAMMA_COLOR},
    {'target': p3.name,
    'edgecolor': TETR_COLOR},
    {'target': p1.name,
    'edgecolor': LAC_COLOR},
    {'target': p2.name,
    'edgecolor': GAMMA_COLOR}
]
draw.draw_all_modules(ax1, m_frames, design.modules, user_params=custom_rendering)


# draw interactions
colors =[TETR_COLOR, LAC_COLOR, GAMMA_COLOR]
draw.draw_all_interactions(ax1, design.interactions, colors=colors)


###############################################################################
# Plot of repressilator dynamics
###############################################################################

ax2 = plt.subplot(gs[1])
plt.plot(t, ytet, color=TETR_COLOR)
plt.plot(t, ylac, color=LAC_COLOR)
plt.plot(t, ygamma, color=GAMMA_COLOR)
plt.ylim([1,4])
ax2.tick_params(axis='both', labelsize=8, width=0.8, length=3)
ax2.set_xlabel('Time', fontsize=8, labelpad=1)
ax2.set_ylabel('Protein Concentration', fontsize=8, labelpad=2)
plt.legend(['tetR', 'lacI', 'gamma'], frameon=False, fontsize=8, labelspacing=0.15, loc=(0.06,0.65))

# Save the figure
plt.show()
#plt.savefig('repressilator_animate.png', dpi=300)
#plt.savefig('repressilator_animate.pdf', transparent=True)