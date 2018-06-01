# create nonsensical design that uses all of the supported sbol terms in current sbolplotlib
import sbol



#role identifier namespace
ROLE_IDENTIFIER = "http://identifiers.org/so/SO:"

# list of functions to add components
def addPromoter(d):
	promoter = sbol.ComponentDefinition('promoter', sbol.BIOPAX_DNA)
	promoter.roles = ROLE_IDENTIFIER + "0000167"
	d.addComponentDefinition(promoter)

def addCDS(d):
	# create coding sequence
	# referenced from: https://github.com/SynBioDex/pySBOL/blob/master/docs/repositories.rst
	cds = sbol.ComponentDefinition('b0032', sbol.BIOPAX_DNA)
	d.addComponentDefinition(cds)

def addTerminator(d):
	terminator = sbol.ComponentDefinition('terminator', sbol.BIOPAX_DNA)
	terminator.roles = ROLE_IDENTIFIER + "0000141"
	d.addComponentDefinition(terminator)

def addRBS(d):
	# creade ribosome binding site
	# reference from: https://github.com/SynBioDex/pySBOL/blob/master/docs/repositories.rst
	rbs = sbol.ComponentDefinition('e0040', sbol.BIOPAX_RNA)
	rbs.roles = ROLE_IDENTIFIER + "0000552"
	d.addComponentDefinition(rbs)

def addScar(d):
	# scar from restriction enzyme after ligation
	scar = sbol.ComponentDefinition('Scar', sbol.BIOPAX_DNA)
	scar.roles = ROLE_IDENTIFIER + "0001953"
	d.addComponentDefinition(scar)

def addRibozyme(d):
	ribozyme = sbol.ComponentDefinition('ribozyme', sbol.BIOPAX_RNA)
	ribozyme.roles = ROLE_IDENTIFIER + "000037"
	d.addComponentDefinition(ribozyme)

def addRibonuclease(d):
	ribonuclease = sbol.ComponentDefinition('ribonuclease', sbol.BIOPAX_PROTEIN)
	ribonuclease.roles = ROLE_IDENTIFIER + "0001977"
	d.addComponentDefinition(ribonuclease)

def addProteinStability(d):
	# A polypeptide region that proves structure in a protein that affects the stability of the protein.
	proteinStability = sbol.ComponentDefinition('protein_stability', sbol.BIOPAX_PROTEIN)
	proteinStability.roles = ROLE_IDENTIFIER + "0001955"
	d.addComponentDefinition(proteinStability)

def addProtease(d):
	protease = sbol.ComponentDefinition('protease', sbol.BIOPAX_PROTEIN)
	protease.roles = ROLE_IDENTIFIER + "0001956"
	d.addComponentDefinition(protease)

def addOperator(d):
	# polypeptide_region that codes for a protease cleavage site.
	operator = sbol.ComponentDefinition('operator', sbol.BIOPAX_PROTEIN)
	operator.roles = ROLE_IDENTIFIER + "0001956"
	d.addComponentDefinition(operator)

def addOrigin(d):
	# origin of replication
	origin = sbol.ComponentDefinition('origin', sbol.BIOPAX_DNA)
	origin.roles = ROLE_IDENTIFIER + "0000296"
	d.addComponentDefinition(origin)

def add5Overhang(d):
	# restriction enzyme five prime single strand overhang
	fiveOverhang = sbol.ComponentDefinition('fiveOverhang', sbol.BIOPAX_PROTEIN)
	fiveOverhang.roles = ROLE_IDENTIFIER + "0001932"
	d.addComponentDefinition(fiveOverhang)

def add3Overhang(d):
	# restriction enzyme three prime single strand overhang
	threeOverhang = sbol.ComponentDefinition('threeOverhang', sbol.BIOPAX_PROTEIN)
	threeOverhang.roles = ROLE_IDENTIFIER + "0001933"
	d.addComponentDefinition(threeOverhang)

def addRestrictionSite(d):
	# restriction endonuclease recognition site (usually palindrome)
	restriction_site = sbol.ComponentDefinition('restriction_site', sbol.BIOPAX_DNA)
	restriction_site.roles = ROLE_IDENTIFIER + "0001687"
	d.addComponentDefinition(restriction_site)

def addRecombinaseSite(d):
	recombination_site = sbol.ComponentDefinition('recombination_site', sbol.BIOPAX_DNA)
	recombination_site.roles = ROLE_IDENTIFIER + "0000299"
	d.addComponentDefinition(recombination_site)

def addBluntRSSite(d):
	bluntRSsite = sbol.ComponentDefinition('bluntRSsite', sbol.BIOPAX_DNA)
	bluntRSsite.roles = ROLE_IDENTIFIER + "0000299"
	d.addComponentDefinition(bluntRSsite)

def addPrimerBindingSite(d):
	primerBindingSite = sbol.ComponentDefinition('primerBindingSite', sbol.BIOPAX_DNA)
	primerBindingSite.roles = ROLE_IDENTIFIER + "0005850"
	d.addComponentDefinition(primerBindingSite)

def add5StickyRestrictionSite(d):
	# single strand restriction enzyme cleavage site
	fiveStickyRSSite = sbol.ComponentDefinition('fiveStickyRSSite', sbol.BIOPAX_DNA)
	fiveStickyRSSite.roles = ROLE_IDENTIFIER + "0001694"
	d.addComponentDefinition(fiveStickyRSSite)

def add3StickyRestrictionSite(d):
	threeStickyRSSite = sbol.ComponentDefinition('threeStickyRSSite', sbol.BIOPAX_DNA)
	threeStickyRSSite.roles = ROLE_IDENTIFIER + "0001690"
	d.addComponentDefinition(threeStickyRSSite)

def addUserDefined(d):
	userDefined = sbol.ComponentDefinition('userDefined', sbol.BIOPAX_DNA)
	userDefined.roles = ROLE_IDENTIFIER + "0000001"
	d.addComponentDefinition(userDefined)

def addSignature(d):
	signature = sbol.ComponentDefinition('signature', sbol.BIOPAX_DNA)
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
	addUserDefined(doc)
	addSignature(doc)

	doc.write('allComponentDefinitions.xml')
	print(doc)


if __name__ == "__main__":
	main()
