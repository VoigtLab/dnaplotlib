## test script to try rendering three hierarchy

import dnaplotlib as dpl
import dnaplotlib.sbol as dpl_sbol
import sbol as sbol
import matplotlib.pyplot as plt

# Import the sbol design 
doc = sbol.Document()
doc.read('threelevel_hierarchy.xml')

# Create the DNAplotlib renderer
dr = dpl_sbol.SBOLRenderer()
print(dr)

# Instantiate rendered
part_renderers = dr.SBOL_part_renderers()
print(part_renderers)