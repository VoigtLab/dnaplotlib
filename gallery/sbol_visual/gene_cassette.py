import sbol3 as sbol

sbol.set_namespace("http://sbols.org/dnaplotlib")

# Create a new Document
doc = sbol.Document()
gene_cassette = sbol.Component("GeneCassette", sbol.SBO_DNA, name="Gene Cassette")
doc.add(gene_cassette)
seq = sbol.Sequence(
    "GeneCassetteSequence",
    elements="gtaatcctatgatcgagcacacggcgcaggtcttgtccgagggaaaaagtcggtggccgcaataaaaaagtaacccttaatcatgatggtaaactcaatttaaccttatcgaactgcgttgcaggcattagccctaattagccggggctgaaaggaagaatcactgtctcagatattgagggtatgtctaacctacaccatatagcaagaagttcggactgaacgtgccttcctcctctctacgtcgttaaaggtatataatcggcctgagttagtcccagcattctaatagcgagatatagctggcctcggcttaagtgctaccggtccctttaggccaccttagacttgttggtacacatgactcgtgagtataagccgcgaagataaccttcccagaaatccctgcccaagatgttcaatacatgccttccacacggcctgagcatacggttggtaaatgcgggtggtgtgtacttgtaaatgatggactggtctcagcacgcttaccaatcaagatcccccatgggtgatggcatggaggagcgaatcgcatagaggatgtttaagtaagacgtcgttcgcacttcgaccctataacaactataatttaccttggtacgaagtagctgaaaaacgataactgacaagagtggttccgcggatattatgatccaacacattaccggaacgagtaaggatgccaacgggttcgataactggcgcagtctggtcttctcgctgtgaagcgccgcactgcgctacataggggatgctgtcatgccttaatgttttagtaagcaccaaatgggacttatgacaggcagagccacagtatacgtgtcctccgtaacgaagtagacacctctttataatcgccacaagatagaatgctgtaataggtatatcagtatccgcggaatggaaaccttatctaaagcagtgcttgccatagacgagtgcacattcctggcagctaaggaggcggtagctcaggagtactgggaagttattgtacttccgtc",
    encoding=sbol.IUPAC_DNA_ENCODING,
)
gene_cassette.sequences.append(seq)

# Define all SubComponents with their specific locations


def add_subcomponent(component, role, start, end, name):
    sub_sequence = sbol.Sequence(name + "Sequence", elements=seq.elements[start - 1 : end - 1])
    range_location = sbol.Range(start=start, end=end, sequence=sub_sequence)
    subcomponent = sbol.SubComponent(component, name=name, roles=[role], locations=range_location)
    gene_cassette.features.append(subcomponent)


# Promoter 1
add_subcomponent(sbol.SBO_DNA, sbol.SO_PROMOTER, 1, 44, "Promoter1")

# RBS 1
add_subcomponent(sbol.SBO_DNA, sbol.SO_RBS, 45, 61, "RBS1")

# Coding Sequence 1
add_subcomponent(sbol.SBO_DNA, sbol.SO_CDS, 62, 922, "CodingSequence1")

# Terminator 1
add_subcomponent(sbol.SBO_DNA, sbol.SO_TERMINATOR, 923, 1025, "Terminator1")

# Write to file
doc.write("gene_cassette.xml")
