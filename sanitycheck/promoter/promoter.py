# create ComponentDefinition of promoter
import sbol

# role property 
ROLE_PROMOTER = "http://identifiers.org/so/SO:0000167" 
ROLE_PCR_PRODUCT = "http://identifiers.org/so/SO:0000006"



# create a file document
doc = sbol.Document()

# open world URIs
sbol.setHomespace('http://sbols.org/promoter_example/')
sbol.Config.setOption('sbol_compliant_uris', True) #scheme, namespace, local identifier, version number
sbol.Config.setOption('sbol_typed_uris', False)
target_promoter = sbol.ComponentDefinition('target_promoter', sbol.BIOPAX_DNA)
target_promoter.roles = [ROLE_PROMOTER, ROLE_PCR_PRODUCT]

# adding objects to document
doc.addComponentDefinition(target_promoter)
doc.write('promoter_example.xml')

print(doc)
