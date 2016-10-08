#!/usr/bin/env python
"""
	Animation of the repressilator gene circuit
"""

import numpy as np
from scipy.integrate import odeint
import dnaplotlib
import matplotlib.pyplot as plt
from matplotlib import gridspec

__author__  = 'Emerson Glassey <eglassey@mit.edu>, Voigt Lab, MIT'
__license__ = 'MIT'
__version__ = '1.0'

# Initialize Simulation
# Initial concentration of mRNA and Protein for each repressor
mtet, mlac, mgamma, tet, lac, gamma = initial = [1, 1, 1, 2, 1, 1]
# Non-dimensionalized production rate
alpha = 15
# Degradation Rate
beta = 2000
# Repressor/Promoter Leak
leak = 1
# Hill Coefficient
n = 8

# Initialize Parts
# tetr  is orange [1.00, 0.75, 0.17]
# lacI  is green  [0.38, 0.82, 0.32]
# gamma is blue   [0.38, 0.65, 0.87]
plac = {'name':'P_lac', 'start':1, 'end':10, 'type':'Promoter', 'opts': {'color':[0.38, 0.82, 0.32]}}
rbs1 = {'name':'RBS', 'start':11, 'end':20, 'type':'RBS', 'opts':{'linewidth': 0, 'color':[0.0, 0.0, 0.0]}}
tetr = {'name':'tetR', 'start':21, 'end':40, 'type':'CDS', 'opts':{'label': 'tetR', 'fontsize': 8,  'label_y_offset': 0, 'label_x_offset': -2, 'label_style':'italic', 'color':[1.00, 0.75, 0.17]}}
term1 = {'name':'Term', 'start':41, 'end':55, 'type':'Terminator'}
pgamma = {'name':'P_gamma', 'start':56, 'end':65, 'type':'Promoter', 'opts': {'color':[0.38, 0.65, 0.87]}}
rbs2 = {'name':'RBS', 'start':66, 'end':75, 'type':'RBS', 'opts':{'linewidth': 0, 'color':[0.0, 0.0, 0.0]}}
laci = {'name':'lacI', 'start':76, 'end':95, 'type':'CDS', 'opts':{'label': 'lacI', 'fontsize': 8,  'label_y_offset': 0, 'label_x_offset': -2, 'label_style':'italic', 'color':[0.38, 0.82, 0.32]}}
term2 = {'name':'Term', 'start':96, 'end':110, 'type':'Terminator'}
ptet = {'name':'P_tet', 'start':111, 'end':120, 'type':'Promoter', 'opts': {'color':[1.00, 0.75, 0.17]}}
rbs3 = {'name':'RBS', 'start':121, 'end':130, 'type':'RBS', 'opts':{'linewidth': 0, 'color':[0.0, 0.0, 0.0]}}
gamma = {'name':'gamma', 'start':131, 'end':150, 'type':'CDS', 'opts':{'label': 'gamma', 'fontsize': 8, 'label_y_offset': 0, 'label_x_offset': -1, 'label_style':'italic', 'color':[0.38, 0.65, 0.87]}}
term3 = {'name':'Term', 'start':151, 'end':165, 'type':'Terminator'}

lac_repress = {'from_part':laci, 'to_part':plac, 'type':'Repression', 'opts':{'linewidth':1, 'color':[0.38, 0.82, 0.32]}}
gamma_repress = {'from_part':gamma, 'to_part':pgamma, 'type':'Repression', 'opts':{'linewidth':1, 'color':[0.38, 0.65, 0.87]}}
tet_repress = {'from_part':tetr, 'to_part':ptet, 'type':'Repression', 'opts':{'linewidth':1, 'color':[1.00, 0.75, 0.17]}}

def repressilator(y, t):
    mtet, mlac, mgamma, tet, lac, gamma = y
    
    dmtet = -mtet + (alpha / (1 + lac**n)) + leak
    dtet = -beta * (tet - mtet)
    
    dmlac = -mlac + (alpha / (1 + gamma**n)) + leak
    dlac = -beta * (lac - mlac)
    
    dmgamma = -mgamma + (alpha / (1 + tet**n)) + leak
    dgamma = -beta * (gamma - mgamma)
    return [dmtet, dmlac, dmgamma, dtet, dlac, dgamma]

def repression(val, Kd, power):
    """Function takes a value and Kd. Function fits the value to a hill function with n=power and Kd
    and returns the fraction bound."""
    new_val = val**power / (Kd**power + val** power)
    return new_val
    
def expression(val, lims):
    """function takes a value between two limits (as a tuple) and returns the value normalized
    by the limits to be between 0 and 1"""
    new_val = (val - lims[0]) / (lims[1] - lims[0])
    return new_val

def rescale(val, lims):
    """function takes a value between 0 and 1 and normalizes it between the limits in lims"""
    new_val = (val*(lims[1]-lims[0])) + lims[0]
    return new_val
    
def plot_construct(ax, t, ymtet, ymlac, ymgamma, ytet, ylac, ygamma):
	tind = int(t*10)
	exp_lims = (1.0, 4.0)
	ax.set_title('t = {}'.format(t), fontsize=8)
	# Set color for each of the CDSs
	tetr['opts']['color'] = [rescale(1 - expression(ymtet[tind], exp_lims), (1.0, 1.0)),
								rescale(1 - expression(ymtet[tind], exp_lims), (0.75, 1.0)),
								rescale(1 - expression(ymtet[tind], exp_lims), (0.17, 1.0))]
	laci['opts']['color'] = [rescale(1 - expression(ymlac[tind], exp_lims), (0.38, 1.0)),
								rescale(1 - expression(ymlac[tind], exp_lims), (0.82, 1.0)),
								rescale(1 - expression(ymlac[tind], exp_lims), (0.32, 1.0))]
	gamma['opts']['color'] = [rescale(1 - expression(ymgamma[tind], exp_lims), (0.38, 1.0)),
								rescale(1 - expression(ymgamma[tind], exp_lims), (0.65, 1.0)),
								rescale(1 - expression(ymgamma[tind], exp_lims), (0.87, 1.0))]
	# Set transparency for each of the regulatory lines
	lac_repress['opts']['color'] = [0.38, 0.82, 0.32,
								rescale(repression(ylac[tind], 2.0, 8), (0.2, 1.0))]
	gamma_repress['opts']['color'] = [0.38, 0.65, 0.87,
								rescale(repression(ygamma[tind], 2.0, 8), (0.2, 1.0))]
	tet_repress['opts']['color'] = [1.00, 0.75, 0.17,
								rescale(repression(ytet[tind], 2.0, 8), (0.2, 1.0))]
	# Set width for each of the regulatory lines
	lac_repress['opts']['linewidth'] = rescale(repression(ylac[tind], 2.0, 8), (0.5, 2.0))						
	gamma_repress['opts']['linewidth'] = rescale(repression(ygamma[tind], 2.0, 8), (0.5, 2.0))							
	tet_repress['opts']['linewidth'] = rescale(repression(ytet[tind], 2.0, 8), (0.5, 2.0))
	dnaplotlib.plot_sbol_designs([ax], [[plac, rbs1, tetr, term1, pgamma, rbs2, laci, term2, ptet, rbs3, gamma, term3]],
				[[lac_repress, gamma_repress, tet_repress]])
	ax.set_ylim([-10, 31])
	
def movie(ts, ymtet, ymlac, ymgamma, ytet, ylac, ygamma):
	for t in ts:
		plt.close()
		plt.figure(figsize=(4, 3.5))
		gs = gridspec.GridSpec(3, 1, height_ratios=[2, 0.5, 1])

		ax = plt.subplot(gs[0])
		plt.plot(ts[:int(t*10)+1], ytet[:int(t*10)+1], color=[1.00, 0.75, 0.17])
		plt.plot(ts[:int(t*10)+1], ylac[:int(t*10)+1], color=[0.38, 0.82, 0.32])
		plt.plot(ts[:int(t*10)+1], ygamma[:int(t*10)+1], color=[0.38, 0.65, 0.87])
		plt.xlim([0, 30])
		plt.ylim([1,4])
		ax.tick_params(axis='both', labelsize=8, width=0.8, length=3)
		ax.yaxis.tick_left()
		ax.xaxis.tick_bottom()
		ax.set_xlabel('Time', fontsize=8, labelpad=3)
		ax.set_ylabel('Protein Concentration', fontsize=8, labelpad=4)
		plt.legend(['tetR', 'lacI', 'gamma'], frameon=False, fontsize=8, labelspacing=0.15, loc=(0.03,0.65))
		plt.plot(ts[int(t*10)], ytet[int(t*10)], '.', color=[1.00, 0.75, 0.17], markersize=6.0)
		plt.plot(ts[int(t*10)], ylac[int(t*10)], '.', color=[0.38, 0.82, 0.32], markersize=6.0)
		plt.plot(ts[int(t*10)], ygamma[int(t*10)], '.', color=[0.38, 0.65, 0.87], markersize=6.0)
		ax = plt.subplot(gs[2])
		plot_construct(ax, t, ymtet, ymlac, ymgamma, ytet, ylac, ygamma)
		plt.savefig("movie/repressilator_t{}.jpg".format(t), dpi=300)
	
def main():
	t = np.arange(0, 30.1, 0.1)
	ymtet, ymlac, ymgamma, ytet, ylac, ygamma = zip(*odeint(repressilator, initial, t))
	plt.close()
	plt.figure(figsize=(3.5, 6.5))
	gs = gridspec.GridSpec(8, 1, height_ratios=[1, 2.5, 0.1, 1, 1, 1, 1, 1])

	# Plot of repressilator circuit
	ax = plt.subplot(gs[0])
	dnaplotlib.plot_sbol_designs([ax], [[plac, rbs1, tetr, term1, pgamma, rbs2, laci, term2, ptet, rbs3, gamma, term3]],
				[[lac_repress, gamma_repress, tet_repress]])
	ax.set_ylim([-10, 31])

	# Plot of repressilator dynamics
	ax = plt.subplot(gs[1])
	plt.plot(t, ytet, color=[1.00, 0.75, 0.17])
	plt.plot(t, ylac, color=[0.38, 0.82, 0.32])
	plt.plot(t, ygamma, color=[0.38, 0.65, 0.87])
	plt.axvline(x=1, color='k', linewidth=0.7)
	plt.axvline(x=12, color='k', linewidth=0.7)
	plt.axvline(x=25.3, color='k', linewidth=0.7)
	plt.axvline(x=27.3, color='k', linewidth=0.7)
	plt.axvline(x=29.4, color='k', linewidth=0.7)
	plt.ylim([1,4])
	ax.tick_params(axis='both', labelsize=8, width=0.8, length=3)
	ax.yaxis.tick_left()
	ax.xaxis.tick_bottom()
	ax.set_xlabel('Time', fontsize=8, labelpad=1)
	ax.set_ylabel('Protein Concentration', fontsize=8, labelpad=2)
	plt.legend(['tetR', 'lacI', 'gamma'], frameon=False, fontsize=8, labelspacing=0.15, loc=(0.06,0.65))

	# Plot of each timepoint
	ax = plt.subplot(gs[3])
	plot_construct(ax, 1, ymtet, ymlac, ymgamma, ytet, ylac, ygamma)
	ax = plt.subplot(gs[4])
	plot_construct(ax, 12, ymtet, ymlac, ymgamma, ytet, ylac, ygamma)
	ax = plt.subplot(gs[5])
	plot_construct(ax, 25.3, ymtet, ymlac, ymgamma, ytet, ylac, ygamma)
	ax = plt.subplot(gs[6])
	plot_construct(ax, 27.3, ymtet, ymlac, ymgamma, ytet, ylac, ygamma)
	ax = plt.subplot(gs[7])
	plot_construct(ax, 29.4, ymtet, ymlac, ymgamma, ytet, ylac, ygamma)

	# Update subplot spacing
	plt.subplots_adjust(hspace=0.4, left=0.12, right=0.95, top=0.99, bottom=0.01)
	
	# Save the figure
	plt.savefig('repressilator_animate.pdf', transparent=True)
	plt.savefig('repressilator_animate.png', dpi=300)
	
	# Generate the movie frames
	movie(t, ymtet, ymlac, ymgamma, ytet, ylac, ygamma)
	
if __name__ == '__main__':
	main()
