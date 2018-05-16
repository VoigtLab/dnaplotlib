# visualization file to understand sbol1 files

import sbol
#import assembly 

import dnaplotlib as dnaplotlib
import dnaplotlib.sbol as dpl_sbol 

import matplotlib.pyplot as pyplot

# test pySBOL interface
doc = sbol.Document()
doc.read('BBa_I0462.xml')
#target = doc.components['http://partsregistry.org/Part:BBa_I0462']

print(doc)
for obj in doc:
	print(obj)