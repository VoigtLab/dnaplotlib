#!/usr/bin/python

"""
Simple demo of a scatter plot.
"""
import numpy as np
import matplotlib.pyplot as plt
import dnaplotlib as dpl
import csv


filename_in ='data_points.txt'

data_reader = csv.reader(open(filename_in, 'rU'), delimiter=' ')

x = [];
y = [];

for row in data_reader:
	y.append( float(row[1]) )
	x.append( float(row[2]) )


fig = plt.figure(figsize=(2.8,2.32))

ax = plt.subplot(1, 1, 1)

ax.set_yscale('log')
ax.set_xlim([0.85,1.05])
ax.set_ylim([1,500])
ax.set_xticks([0.85, 0.9, 0.95, 1.0, 1.05])
ax.tick_params(axis='y', labelsize=8)
ax.tick_params(axis='x', labelsize=8)
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
ax.yaxis.set_ticks_position('left')
ax.xaxis.set_ticks_position('bottom')
plt.xlabel('Parameter 1', fontsize=8, labelpad=0)
plt.ylabel('Parameter 2', fontsize=8, labelpad=0)
ax.tick_params(axis='y', which='major', pad=1)
plt.scatter(x, y, c='none', s=6, edgecolor=(0.5,0.5,0.5), lw = 0.8) #(0.38, 0.65, 0.87)

plt.annotate(
        '', 
        xy = (0.8785, 323.5), xytext = (25, 5),
        textcoords = 'offset points', ha = 'right', va = 'bottom',
        bbox = dict(boxstyle = 'round,pad=0.5', fc = 'yellow', alpha = 0.5),
        arrowprops = dict(arrowstyle = '->', linewidth=1.0, connectionstyle = 'arc3,rad=0'))


plt.annotate(
        '', 
        xy = (0.977, 34), xytext = (20, 14),
        textcoords = 'offset points', ha = 'right', va = 'bottom',
        bbox = dict(boxstyle = 'round,pad=0.5', fc = 'yellow', alpha = 0.5),
        arrowprops = dict(arrowstyle = '->', linewidth=1.0, connectionstyle = 'arc3,rad=0'))

plt.annotate(
        '', 
        xy = (0.982, 3.3), xytext = (22, 10),
        textcoords = 'offset points', ha = 'right', va = 'bottom',
        bbox = dict(boxstyle = 'round,pad=0.5', fc = 'yellow', alpha = 0.5),
        arrowprops = dict(arrowstyle = '->', linewidth=1.0, connectionstyle = 'arc3,rad=0'))



# Color maps (let's make sure we use similar colors)
col_map = {}
col_map['black']   = (0.00, 0.00, 0.00)
col_map['white']   = (1.00, 1.00, 1.00)
col_map['red']     = (0.95, 0.30, 0.25)
col_map['green']   = (0.38, 0.82, 0.32)
col_map['blue']    = (0.38, 0.65, 0.87)
col_map['orange']  = (1.00, 0.75, 0.17)
col_map['purple']  = (0.55, 0.35, 0.64)
col_map['yellow']  = (0.98, 0.97, 0.35)


lw = 1.0



p1_1 = {'type':'Promoter', 'name':'pA', 'fwd':True, 'opts':{'linewidth':lw, 'color':col_map['black']}}
rbs_1_1 = {'type':'RBS', 'name':'rbs_f', 'fwd':True, 'opts':{'linewidth':lw, 'color':col_map['black'], 'start_pad':-6, 'x_extent':6}}
gA_1 = {'type':'CDS', 'name':'gA',  'fwd':True, 'opts':{'linewidth':lw, 'color':col_map['red'], 'edgecolor':col_map['red'], 'x_extent':24, 'label':'A', 'label_style':'italic', 'label_color':(1,1,1), 'label_x_offset':-3, 'label_y_offset':-1}}
rbs_1_2 = {'type':'RBS', 'name':'rbs_r', 'fwd':True, 'opts':{'linewidth':lw, 'color':col_map['black'], 'start_pad':2, 'x_extent':6}}
gB_1  = {'type':'CDS', 'name':'gB',  'fwd':True, 'opts':{'linewidth':lw, 'color':col_map['blue'], 'edgecolor':col_map['blue'], 'x_extent':24, 'label':'B', 'label_style':'italic', 'label_color':(1,1,1), 'label_x_offset':-3, 'label_y_offset':-1}}
t1_1 = {'type':'Terminator', 'name':'t0', 'fwd':True, 'opts':{'linewidth':lw, 'color':col_map['black'], 'start_pad':-1}}
design1 = [p1_1, rbs_1_1, gA_1, rbs_1_2, gB_1, t1_1]


t1_2 = {'type':'Terminator', 'name':'t0', 'fwd':False, 'opts':{'linewidth':lw, 'color':col_map['black'], 'start_pad':-1}}
gA_2 = {'type':'CDS', 'name':'gA',  'fwd':False, 'opts':{'linewidth':lw, 'color':col_map['red'], 'edgecolor':col_map['red'], 'x_extent':24, 'label':'A', 'label_style':'italic', 'label_color':(1,1,1), 'label_x_offset':2, 'label_y_offset':-1}}
rbs_1_2 = {'type':'RBS', 'name':'rbs_f', 'fwd':False, 'opts':{'linewidth':lw, 'color':col_map['black'], 'start_pad':-6, 'x_extent':6}}
p1_2 = {'type':'Promoter', 'name':'pA', 'fwd':False, 'opts':{'linewidth':lw, 'color':col_map['black']}}

p2_2 = {'type':'Promoter', 'name':'pA', 'fwd':True, 'opts':{'linewidth':lw, 'color':col_map['black']}}
rbs_2_2 = {'type':'RBS', 'name':'rbs_r', 'fwd':True, 'opts':{'linewidth':lw, 'color':col_map['black'], 'start_pad':-6, 'x_extent':6}}
gB_2  = {'type':'CDS', 'name':'gB',  'fwd':True, 'opts':{'linewidth':lw, 'color':col_map['blue'], 'edgecolor':col_map['blue'], 'x_extent':24, 'label':'B', 'label_style':'italic', 'label_color':(1,1,1), 'label_x_offset':-3, 'label_y_offset':-1}}
t2_2 = {'type':'Terminator', 'name':'t0', 'fwd':True, 'opts':{'linewidth':lw, 'color':col_map['black'], 'start_pad':-1}}

design2 = [t1_2, gA_2, rbs_1_2, p1_2, p2_2, rbs_2_2, gB_2, t2_2]


p1_3 = {'type':'Promoter', 'name':'pA', 'fwd':True, 'opts':{'linewidth':lw, 'color':col_map['black']}}
rbs_1_3 = {'type':'RBS', 'name':'rbs_r', 'fwd':True, 'opts':{'linewidth':lw, 'color':col_map['black'], 'start_pad':-6, 'x_extent':6}}
gA_3  = {'type':'CDS', 'name':'gB',  'fwd':True, 'opts':{'linewidth':lw, 'color':col_map['red'], 'edgecolor':col_map['red'], 'x_extent':24, 'label':'A', 'label_style':'italic', 'label_color':(1,1,1), 'label_x_offset':-3, 'label_y_offset':-1}}
t1_3 = {'type':'Terminator', 'name':'t0', 'fwd':True, 'opts':{'linewidth':lw, 'color':col_map['black'], 'start_pad':-1}}

t2_3 = {'type':'Terminator', 'name':'t0', 'fwd':False, 'opts':{'linewidth':lw, 'color':col_map['black'], 'start_pad':-1}}
gB_3 = {'type':'CDS', 'name':'gA',  'fwd':False, 'opts':{'linewidth':lw, 'color':col_map['blue'], 'edgecolor':col_map['blue'], 'x_extent':24, 'label':'B', 'label_style':'italic', 'label_color':(1,1,1), 'label_x_offset':0, 'label_y_offset':-1}}
rbs_2_3 = {'type':'RBS', 'name':'rbs_f', 'fwd':False, 'opts':{'linewidth':lw, 'color':col_map['black'], 'start_pad':-6, 'x_extent':6}}
p2_3 = {'type':'Promoter', 'name':'pA', 'fwd':False, 'opts':{'linewidth':lw, 'color':col_map['black']}}

design3 = [p1_3, rbs_1_3, gA_3, t1_3, t2_3, gB_3, rbs_2_3, p2_3]








g0 = {'type':'CDS', 'name':'g0_ON',  'fwd':True, 'opts':{'linewidth':lw, 'color':col_map['white']}}
g1 = {'type':'CDS', 'name':'g1_ON',  'fwd':True, 'opts':{'linewidth':lw, 'color':col_map['red']}}
g2 = {'type':'CDS', 'name':'g2_ON',  'fwd':True, 'opts':{'linewidth':lw, 'color':col_map['blue']}}
g3 = {'type':'CDS', 'name':'g3_ON',  'fwd':True, 'opts':{'linewidth':lw, 'color':col_map['green']}}
g4 = {'type':'CDS', 'name':'g4_ON',  'fwd':True, 'opts':{'linewidth':lw, 'color':col_map['orange']}}
g5 = {'type':'CDS', 'name':'g5_ON',  'fwd':True, 'opts':{'linewidth':lw, 'color':col_map['purple']}}
g6 = {'type':'CDS', 'name':'g6_ON',  'fwd':True, 'opts':{'linewidth':lw, 'color':col_map['yellow']}}

i0 = {'type':'Ribozyme', 'name':'i0', 'fwd':True, 'opts':{'linewidth':lw, 'color':col_map['black']}}
i1 = {'type':'Ribozyme', 'name':'i1', 'fwd':True, 'opts':{'linewidth':lw, 'color':col_map['red']}}
i2 = {'type':'Ribozyme', 'name':'i2', 'fwd':True, 'opts':{'linewidth':lw, 'color':col_map['blue']}}
i3 = {'type':'Ribozyme', 'name':'i3', 'fwd':True, 'opts':{'linewidth':lw, 'color':col_map['green']}}
i4 = {'type':'Ribozyme', 'name':'i4', 'fwd':True, 'opts':{'linewidth':lw, 'color':col_map['orange']}}
i5 = {'type':'Ribozyme', 'name':'i5', 'fwd':True, 'opts':{'linewidth':lw, 'color':col_map['purple']}}
i6 = {'type':'Ribozyme', 'name':'i6', 'fwd':True, 'opts':{'linewidth':lw, 'color':col_map['yellow']}}

pA = {'type':'Promoter', 'name':'pA', 'fwd':True, 'opts':{'linewidth':lw, 'color':col_map['black']}}
pB = {'type':'Promoter', 'name':'pB', 'fwd':True, 'opts':{'linewidth':lw, 'color':col_map['black']}}
p1 = {'type':'Promoter', 'name':'p1', 'fwd':True, 'opts':{'linewidth':lw, 'color':col_map['red']}}
p2 = {'type':'Promoter', 'name':'p2', 'fwd':True, 'opts':{'linewidth':lw, 'color':col_map['blue']}}
p3 = {'type':'Promoter', 'name':'p3', 'fwd':True, 'opts':{'linewidth':lw, 'color':col_map['green']}}
p4 = {'type':'Promoter', 'name':'p4', 'fwd':True, 'opts':{'linewidth':lw, 'color':col_map['orange']}}
p5 = {'type':'Promoter', 'name':'p5', 'fwd':True, 'opts':{'linewidth':lw, 'color':col_map['purple']}}
p6 = {'type':'Promoter', 'name':'p6', 'fwd':True, 'opts':{'linewidth':lw, 'color':col_map['yellow']}}

t0 = {'type':'Terminator', 'name':'t0', 'fwd':True, 'opts':{'linewidth':lw, 'color':col_map['black']}}
t1 = {'type':'Terminator', 'name':'t1', 'fwd':True, 'opts':{'linewidth':lw, 'color':col_map['red']}}
t2 = {'type':'Terminator', 'name':'t2', 'fwd':True, 'opts':{'linewidth':lw, 'color':col_map['blue']}}
t3 = {'type':'Terminator', 'name':'t3', 'fwd':True, 'opts':{'linewidth':lw, 'color':col_map['green']}}
t4 = {'type':'Terminator', 'name':'t4', 'fwd':True, 'opts':{'linewidth':lw, 'color':col_map['orange']}}
t5 = {'type':'Terminator', 'name':'t5', 'fwd':True, 'opts':{'linewidth':lw, 'color':col_map['purple']}}
t6 = {'type':'Terminator', 'name':'t6', 'fwd':True, 'opts':{'linewidth':lw, 'color':col_map['yellow']}}

u0 = {'type':'RBS', 'name':'u0', 'fwd':True, 'opts':{'linewidth':lw, 'color':col_map['black']}}
u1 = {'type':'RBS', 'name':'u1', 'fwd':True, 'opts':{'linewidth':lw, 'color':col_map['red']}}
u2 = {'type':'RBS', 'name':'u2', 'fwd':True, 'opts':{'linewidth':lw, 'color':col_map['blue']}}
u3 = {'type':'RBS', 'name':'u3', 'fwd':True, 'opts':{'linewidth':lw, 'color':col_map['green']}}
u4 = {'type':'RBS', 'name':'u4', 'fwd':True, 'opts':{'linewidth':lw, 'color':col_map['orange']}}
u5 = {'type':'RBS', 'name':'u5', 'fwd':True, 'opts':{'linewidth':lw, 'color':col_map['purple']}}
u6 = {'type':'RBS', 'name':'u6', 'fwd':True, 'opts':{'linewidth':lw, 'color':col_map['yellow']}}


# A design is merely a list of parts and their properties
#design1 = [pA, pB, i4, u4, g4, t4,  pB, p4, i3, u3, g3, t3,  pA, p4, i2, u2, g2, t2,  p3, p2, i1, u1, g1, t1,  p1, i0, u0, g0, t0]
#design2 = [pA, pB, i5, u5, g5, t5,  pB, p5, i1, u1, g1, t1,  pA, p5, i2, u2, g2, t2,  p1, p2, i4, u4, g4, t4,  p4, i0, u0, g0, t0]
#design3 = [pA, pB, i3, u3, g3, t3,  pB, p3, i2, u2, g2, t2,  pA, p3, i4, u4, g4, t4,  p2, p4, i5, u5, g5, t5,  p5, i0, u0, g0, t0]
#design1 = [pA, pB, i4, u4, g4, t4,  pB, p4, i3, u3, g3, t3,  pA, p4, i2, u2, g2, t2,  p3, p2, i1, u1, g1, t1,  p1]
#design2 = [pA, pB, i5, u5, g5, t5,  pB, p5, i1, u1, g1, t1,  pA, p5, i2, u2, g2, t2,  p1, p2, i4, u4, g4, t4,  p4]
#design3 = [pA, pB, i3, u3, g3, t3,  pB, p3, i2, u2, g2, t2,  pA, p3, i4, u4, g4, t4,  p2, p4, i5, u5, g5, t5,  p5]



ax_dna1 = plt.axes([0.35, 0.83, 0.35, 0.12])
ax_dna2 = plt.axes([0.61, 0.65, 0.4, 0.12])
ax_dna3 = plt.axes([0.58,  0.32, 0.4, 0.12])

# Create the DNAplotlib renderer
dr = dpl.DNARenderer()

# Redender the DNA to axis
start, end = dr.renderDNA(ax_dna1, design1, dr.SBOL_part_renderers())

# Set bounds and display options for the axis
dna_len = end-start
ax_dna1.set_xlim([start, end])
ax_dna1.set_ylim([-15,15])
ax_dna1.set_aspect('equal')
ax_dna1.set_xticks([])
ax_dna1.set_yticks([])
ax_dna1.axis('off')

start, end = dr.renderDNA(ax_dna2, design2, dr.SBOL_part_renderers())

ax_dna2.set_xlim([start, end])
ax_dna2.set_ylim([-15,15])
ax_dna2.set_aspect('equal')
ax_dna2.set_xticks([])
ax_dna2.set_yticks([])
ax_dna2.axis('off')

start, end = dr.renderDNA(ax_dna3, design3, dr.SBOL_part_renderers())
ax_dna3.set_xlim([start, end])
ax_dna3.set_ylim([-15,15])
ax_dna3.set_aspect('equal')
ax_dna3.set_xticks([])
ax_dna3.set_yticks([])
ax_dna3.axis('off')

plt.subplots_adjust(hspace=0.01, left=0.13, right=0.95, top=0.93, bottom=0.13)

fig.savefig('scatter_annotate.pdf', transparent=True)
fig.savefig('scatter_annotate.png', dpi=300)

