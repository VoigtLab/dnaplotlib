# create nonsensical design that uses all of the supported sbol terms in current sbolplotlib

import sbol

#type property
BIOPAX_DNA = "http://www.biopax.org/release/biopax- level3.owl#DnaRegion"
BIOPAX_RNA = "http://www.biopax.org/release/biopax- level3.owl#RnaRegion"
BIOPAX_PROTEIN = "http://www.biopax.org/release/biopax- level3.owl#Protein"
BIOPAX_SMALL_MOLECULE = "http://www.biopax.org/release/biopax- level3.owl#SmallMolecule"
BIOPAX_COMPLEX = "http://www.biopax.org/release/biopax- level3.owl#Complex"

#role identifier namespace
ROLE_IDENTIFIER = "http://identifiers.org/so/SO:"

# list of functions to add components
def addPromoter(d):
	promoter = sbol.ComponentDefinition('promoter', BIOPAX_DNA)
	promoter.roles = ROLE_IDENTIFIER + "0000167"
	d.addComponentDefinition(promoter)

def addCDS(d):
	# create coding sequence
	# referenced from: https://github.com/SynBioDex/pySBOL/blob/master/docs/repositories.rst
	cds = sbol.ComponentDefinition('b0032', BIOPAX_DNA)
	d.addComponentDefinition(cds)

def addTerminator(d):
	terminator = sbol.ComponentDefinition('terminator', BIOPAX_DNA)
	terminator.roles = ROLE_IDENTIFIER + "0000141"
	d.addComponentDefinition(terminator)

def addRBS(d):
	# creade ribosome binding site
	# reference from: https://github.com/SynBioDex/pySBOL/blob/master/docs/repositories.rst
	rbs = sbol.ComponentDefinition('e0040', BIOPAX_RNA)
	rbs.roles = ROLE_IDENTIFIER + "0000552"
	d.addComponentDefinition(rbs)

def addScar(d):
	# scar from restriction enzyme after ligation
	scar = sbol.ComponentDefinition('Scar', BIOPAX_DNA)
	scar.roles = ROLE_IDENTIFIER + "0001953"
	d.addComponentDefinition(scar)

def addRibozyme(d):
	ribozyme = sbol.ComponentDefinition('ribozyme', BIOPAX_RNA)
	ribozyme.roles = ROLE_IDENTIFIER + "000037"
	d.addComponentDefinition(ribozyme)

def addRibonuclease(d):
	ribonuclease = sbol.ComponentDefinition('ribonuclease', BIOPAX_PROTEIN)
	ribonuclease.roles = ROLE_IDENTIFIER + "0001977"
	d.addComponentDefinition(ribonuclease)

def addProteinStability(d):
	# A polypeptide region that proves structure in a protein that affects the stability of the protein.
	proteinStability = sbol.ComponentDefinition('protein_stability', BIOPAX_PROTEIN)
	proteinStability.roles = ROLE_IDENTIFIER + "0001955"
	d.addComponentDefinition(proteinStability)

def addProtease(d):
	protease = sbol.ComponentDefinition('protease', BIOPAX_PROTEIN)
	protease.roles = ROLE_IDENTIFIER + "0001956"
	d.addComponentDefinition(protease)

def addOperator(d):
	# polypeptide_region that codes for a protease cleavage site.
	operator = sbol.ComponentDefinition('operator', BIOPAX_PROTEIN)
	operator.roles = ROLE_IDENTIFIER + "0001956"
	d.addComponentDefinition(operator)

def addOrigin(d):
	# origin of replication
	origin = sbol.ComponentDefinition('origin', BIOPAX_DNA)
	origin.roles = ROLE_IDENTIFIER + "0000296"
	d.addComponentDefinition(origin)

def add5Overhang(d):
	# restriction enzyme five prime single strand overhang
	fiveOverhang = sbol.ComponentDefinition('fiveOverhang', BIOPAX_PROTEIN)
	fiveOverhang.roles = ROLE_IDENTIFIER + "0001932"
	d.addComponentDefinition(fiveOverhang)

def add3Overhang(d):
	# restriction enzyme three prime single strand overhang
	threeOverhang = sbol.ComponentDefinition('threeOverhang', BIOPAX_PROTEIN)
	threeOverhang.roles = ROLE_IDENTIFIER + "0001933"
	d.addComponentDefinition(threeOverhang)

def addRestrictionSite(d):
	# restriction endonuclease recognition site (usually palindrome)
	restriction_site = sbol.ComponentDefinition('restriction_site', BIOPAX_DNA)
	restriction_site.roles = ROLE_IDENTIFIER + "0001687"
	d.addComponentDefinition(restriction_site)

def addRecombinaseSite(d):
	recombination_site = sbol.ComponentDefinition('recombination_site', BIOPAX_DNA)
	recombination_site.roles = ROLE_IDENTIFIER + "0000299"
	d.addComponentDefinition(recombination_site)

def addBluntRSSite(d):
	bluntRSsite = sbol.ComponentDefinition('bluntRSsite', BIOPAX_DNA)
	bluntRSsite.roles = ROLE_IDENTIFIER + "0000299"
	d.addComponentDefinition(bluntRSsite)

def addPrimerBindingSite(d):
	primerBindingSite = sbol.ComponentDefinition('primerBindingSite', BIOPAX_DNA)
	primerBindingSite.roles = ROLE_IDENTIFIER + "0005850"
	d.addComponentDefinition(primerBindingSite)

def add5StickyRestrictionSite(d):
	# single strand restriction enzyme cleavage site
	fiveStickyRSSite = sbol.ComponentDefinition('fiveStickyRSSite', BIOPAX_DNA)
	fiveStickyRSSite.roles = ROLE_IDENTIFIER + "0001694"
	d.addComponentDefinition(fiveStickyRSSite)

def add3StickyRestrictionSite(d):
	threeStickyRSSite = sbol.ComponentDefinition('threeStickyRSSite', BIOPAX_DNA)
	threeStickyRSSite.roles = ROLE_IDENTIFIER + "0001690"
	d.addComponentDefinition(threeStickyRSSite)

def addSignature(d):
	signature = sbol.ComponentDefinition('signature', BIOPAX_DNA)
	signature.roles = ROLE_IDENTIFIER + "0001978"
	d.addComponentDefinition(signature)


def main():
	# create a file
	doc = sbol.Document()

	# open world URI
	sbol.setHomespace('http://sbols.org/sanitcheck_allComponentDefinitions')
	sbol.Config.setOption('sbol_compliant_uris', True) 
	sbol.Config.setOption('sbol_typed_uris', False)

	# list of components 
	addPromoter(doc)
	addCDS(doc)
	addTerminator(doc)
	addRBS(doc)
	addScar(doc)
	addRibozyme(doc)
	addRibonuclease(doc)
	addProteinStability(doc)
	addProtease(doc)
	addOrigin(doc)
	add5Overhang(doc)
	add3Overhang(doc)
	addRestrictionSite(doc)
	addRecombinaseSite(doc)
	addBluntRSSite(doc)
	addPrimerBindingSite(doc)
	add5StickyRestrictionSite(doc)
	add3StickyRestrictionSite(doc)
	addSignature(doc)

	doc.write('allComponentDefinitions.xml')
	print(doc)


if __name__ == "__main__":
	main()
