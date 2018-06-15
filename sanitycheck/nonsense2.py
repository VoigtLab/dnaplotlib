# create nonsensical design that uses all of the supported sbol terms in current sbolplotlib
import sbol



#role identifier namespace
ROLE_IDENTIFIER = "http://identifiers.org/so/SO:"

# list of functions to add components
def createPromoter(d):
	# create component definition
	promoter = sbol.ComponentDefinition('promoter', sbol.BIOPAX_DNA)
	promoter.roles = ROLE_IDENTIFIER + "0000167"
	d.addComponentDefinition(promoter)
	return promoter

	

def createCDS(d):
	# create coding sequence
	# referenced from: https://github.com/SynBioDex/pySBOL/blob/master/docs/repositories.rst
	cds = sbol.ComponentDefinition('b0032', sbol.BIOPAX_DNA)
	d.addComponentDefinition(cds)
	return cds

def createTerminator(d):
	terminator = sbol.ComponentDefinition('terminator', sbol.BIOPAX_DNA)
	terminator.roles = ROLE_IDENTIFIER + "0000141"
	d.addComponentDefinition(terminator)
	return terminator

def createRBS(d):
	# creade ribosome binding site
	# reference from: https://github.com/SynBioDex/pySBOL/blob/master/docs/repositories.rst
	rbs = sbol.ComponentDefinition('e0040', sbol.BIOPAX_RNA)
	rbs.roles = ROLE_IDENTIFIER + "0000552"
	d.addComponentDefinition(rbs)
	return rbs

def createScar(d):
	# scar from restriction enzyme after ligation
	scar = sbol.ComponentDefinition('Scar', sbol.BIOPAX_DNA)
	scar.roles = ROLE_IDENTIFIER + "0001953"
	d.addComponentDefinition(scar)
	return scar

def createRibozyme(d):
	ribozyme = sbol.ComponentDefinition('ribozyme', sbol.BIOPAX_RNA)
	ribozyme.roles = ROLE_IDENTIFIER + "000037"
	d.addComponentDefinition(ribozyme)
	return ribozyme

def createRibonuclease(d):
	ribonuclease = sbol.ComponentDefinition('ribonuclease', sbol.BIOPAX_PROTEIN)
	ribonuclease.roles = ROLE_IDENTIFIER + "0001977"
	d.addComponentDefinition(ribonuclease)
	return ribonuclease

def createProteinStability(d):
	# A polypeptide region that proves structure in a protein that affects the stability of the protein.
	proteinStability = sbol.ComponentDefinition('protein_stability', sbol.BIOPAX_PROTEIN)
	proteinStability.roles = ROLE_IDENTIFIER + "0001955"
	d.addComponentDefinition(proteinStability)
	return proteinStability

def createProtease(d):
	protease = sbol.ComponentDefinition('protease', sbol.BIOPAX_PROTEIN)
	protease.roles = ROLE_IDENTIFIER + "0001956"
	d.addComponentDefinition(protease)
	return protease

def createOperator(d):
	# polypeptide_region that codes for a protease cleavage site.
	operator = sbol.ComponentDefinition('operator', sbol.BIOPAX_PROTEIN)
	operator.roles = ROLE_IDENTIFIER + "0001956"
	d.addComponentDefinition(operator)
	return operator

def createOrigin(d):
	# origin of replication
	origin = sbol.ComponentDefinition('origin', sbol.BIOPAX_DNA)
	origin.roles = ROLE_IDENTIFIER + "0000296"
	d.addComponentDefinition(origin)
	return origin

def create5Overhang(d):
	# restriction enzyme five prime single strand overhang
	fiveOverhang = sbol.ComponentDefinition('fiveOverhang', sbol.BIOPAX_PROTEIN)
	fiveOverhang.roles = ROLE_IDENTIFIER + "0001932"
	d.addComponentDefinition(fiveOverhang)
	return fiveOverhang

def create3Overhang(d):
	# restriction enzyme three prime single strand overhang
	threeOverhang = sbol.ComponentDefinition('threeOverhang', sbol.BIOPAX_PROTEIN)
	threeOverhang.roles = ROLE_IDENTIFIER + "0001933"
	d.addComponentDefinition(threeOverhang)
	return threeOverhang

def createRestrictionSite(d):
	# restriction endonuclease recognition site (usually palindrome)
	restriction_site = sbol.ComponentDefinition('restriction_site', sbol.BIOPAX_DNA)
	restriction_site.roles = ROLE_IDENTIFIER + "0001687"
	d.addComponentDefinition(restriction_site)
	return restriction_site

def createRecombinaseSite(d):
	recombination_site = sbol.ComponentDefinition('recombination_site', sbol.BIOPAX_DNA)
	recombination_site.roles = ROLE_IDENTIFIER + "0000299"
	d.addComponentDefinition(recombination_site)
	return recombination_site

def createBluntRSSite(d):
	bluntRSsite = sbol.ComponentDefinition('bluntRSsite', sbol.BIOPAX_DNA)
	bluntRSsite.roles = ROLE_IDENTIFIER + "0000299"
	d.addComponentDefinition(bluntRSsite)
	return bluntRSsite

def createPrimerBindingSite(d):
	primerBindingSite = sbol.ComponentDefinition('primerBindingSite', sbol.BIOPAX_DNA)
	primerBindingSite.roles = ROLE_IDENTIFIER + "0005850"
	d.addComponentDefinition(primerBindingSite)
	return primerBindingSite

def create5StickyRestrictionSite(d):
	# single strand restriction enzyme cleavage site
	fiveStickyRSSite = sbol.ComponentDefinition('fiveStickyRSSite', sbol.BIOPAX_DNA)
	fiveStickyRSSite.roles = ROLE_IDENTIFIER + "0001694"
	d.addComponentDefinition(fiveStickyRSSite)
	return fiveStickyRSSite

def create3StickyRestrictionSite(d):
	threeStickyRSSite = sbol.ComponentDefinition('threeStickyRSSite', sbol.BIOPAX_DNA)
	threeStickyRSSite.roles = ROLE_IDENTIFIER + "0001690"
	d.addComponentDefinition(threeStickyRSSite)
	return threeStickyRSSite

def createUserDefined(d):
	userDefined = sbol.ComponentDefinition('userDefined', sbol.BIOPAX_DNA)
	userDefined.roles = ROLE_IDENTIFIER + "0000001"
	d.addComponentDefinition(userDefined)
	return userDefined

def createSignature(d):
	signature = sbol.ComponentDefinition('signature', sbol.BIOPAX_DNA)
	signature.roles = ROLE_IDENTIFIER + "0001978"
	d.addComponentDefinition(signature)
	return signature


def main():
	# create a file
	doc = sbol.Document()

	# create root components
	root = sbol.ComponentDefinition('root', sbol.BIOPAX_DNA)
	doc.addComponentDefinition(root)

	# list of components 
	promoC = createPromoter(doc)
	cdsC = createCDS(doc)
	termC = createTerminator(doc)
	rbsC = createRBS(doc)
	scarC = createScar(doc)
	ribozyC = createRibozyme(doc)
	ribonucC = createRibonuclease(doc)
	psC = createProteinStability(doc)
	prC = createProtease(doc)
	originC = createOrigin(doc)
	overhang5 = create5Overhang(doc)
	overhang3 = create3Overhang(doc)
	rsSite = createRestrictionSite(doc)
	rcSite = createRecombinaseSite(doc)
	bluntrsSite = createBluntRSSite(doc)
	primerSite = createPrimerBindingSite(doc)
	srsite5 = create5StickyRestrictionSite(doc)
	srsite3 = create3StickyRestrictionSite(doc)
	usrdef = createUserDefined(doc)
	sig = createSignature(doc)
	

	# setting reverse primary structure 
	root.assemblePrimaryStructure([sig, usrdef, srsite3, srsite5, primerSite, 
		bluntrsSite, rcSite, rsSite, overhang3, overhang5, originC, prC, psC, ribonucC,
		ribozyC, scarC, rbsC, termC, cdsC, promoC], doc)

	# checking primary structure 
	primary_structure = root.getPrimaryStructure()
	for component in primary_structure:
		print(component.displayId)

	# check whether valid
	print(doc.write('allCDinSeqConstr.xml'))
	


if __name__ == "__main__":
	main()
