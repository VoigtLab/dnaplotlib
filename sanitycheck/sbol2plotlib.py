'''
render component definitions in sbol 2 compliant files
'''
import sbol
import matplotlib.pyplot as plt
from matplotlib.path import Path
import matplotlib.patches as patches


# preliminary second steps
# rendering functions 
def renderRNA():
	verts = [
		(-2., 0.),
		(-1., 1.),
		(0., 0.),
		(1., -1.),
		(2., 0.)
	]

	codes = [
		Path.MOVETO,
		Path.CURVE3,
		Path.CURVE3,
		Path.CURVE3,
		Path.CURVE3
	]

	path = Path(verts, codes)

	fig = plt.figure()
	ax = fig.add_subplot(111)
	patch = patches.PathPatch(path, facecolor='none', lw=2)
	ax.add_patch(patch)
	ax.annotate('ex: miRNA', xy=(0., -1), ha='center') # random dna name for now
	ax.set_xlim(-5, 5)
	ax.set_ylim(-5, 5)
	ax.set_axis_off()
	

	plt.show()

def renderDNA():
	verts = [
		(-2., 0.),
		(-1., 1.),
		(0., 0.),
		(1., -1.),
		(2., 0.), 
		(-2., -1),
		(-1., 0.),
		(0., -1),
		(1., -2),
		(2., -1.)
	]

	codes = [
		Path.MOVETO,
		Path.CURVE3,
		Path.CURVE3,
		Path.CURVE3,
		Path.CURVE3,
		Path.MOVETO,
		Path.CURVE3,
		Path.CURVE3,
		Path.CURVE3,
		Path.CURVE3
	]

	path = Path(verts, codes)

	fig = plt.figure()
	ax = fig.add_subplot(111)
	patch = patches.PathPatch(path, facecolor='none', lw=2)
	ax.add_patch(patch)
	ax.annotate('ex: b0032', xy=(0., -2), ha='center') # random dna name for now
	ax.set_xlim(-5, 5)
	ax.set_ylim(-5, 5)
	ax.set_axis_off()
	

	plt.show()


# first step
# open sbol compliant files 
doc = sbol.Document()
doc.read('allCDinSeqConstr.xml')

# assume that root componentDefinition contains primary structure
for comp in doc.componentDefinitions:
	if comp.displayId == 'root':
		primary_structure = comp.getPrimaryStructure()

renderDNA()
renderRNA()

