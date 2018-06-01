# create Component Definition of protein 
import sbol

# create a file document
doc = sbol.Document()

# open world URIs
sbol.setHomespace('http://sbols.org/protein_example')
sbol.Config.setOption('sbol_compliant_uris', True) #scheme, namespace, local identifier, version number
sbol.Config.setOption('sbol_typed_uris', False)
target_protein = sbol.ComponentDefinition('target_protein', sbol.BIOPAX_PROTEIN)


# adding objects to document
doc.addComponentDefinition(target_protein)
doc.write('protein_example.xml')

print(doc)
