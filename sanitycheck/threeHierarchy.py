#create 3 hierarchy example 
import sbol 

# create file 
doc = sbol.Document()

# create root ComponentDefinitions
root = sbol.ComponentDefinition('root', sbol.BIOPAX_DNA)
sub = sbol.ComponentDefinition('sub', sbol.BIOPAX_DNA)
subsub = sbol.ComponentDefinition('subsub', sbol.BIOPAX_DNA) 

# create comp
sub_0 = sbol.Component('sub_0')
sub_0.definition = sub
root.components.add(sub_0)
subsub_0 = sbol.Component('subsub_0')
subsub_0.definition = subsub
sub.components.add(subsub_0)

# create seq 
rootSeq = sbol.Sequence('root', 'atcg', sbol.SBOL_ENCODING_IUPAC)
root.sequence = rootSeq 
subSeq = sbol.Sequence('sub', 'aaa', sbol.SBOL_ENCODING_IUPAC)
sub.sequence = subSeq
subsubSeq = sbol.Sequence('subsub', 'ttt', sbol.SBOL_ENCODING_IUPAC)
subsub.sequence = subsubSeq

# add to doc 
doc.addComponentDefinition(root)
doc.addComponentDefinition(sub)
doc.addComponentDefinition(subsub)
doc.addSequence(rootSeq)
doc.addSequence(subSeq)
doc.addSequence(subsubSeq)

# export
print(doc.write('threelevel_hierarchy.xml'))