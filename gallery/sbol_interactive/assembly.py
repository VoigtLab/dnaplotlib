"""
Read an SBOL file and display its contents
"""

# Add SBOL module directory to PYTHONPATH
import os, sys
lib_path = os.path.abspath('..')
sys.path.append(lib_path)

import random  # For random sequence generation
import sbol
#from sbol import libsbol
from subprocess import Popen, PIPE, STDOUT  # For calling command line tools Clustal Omega and EMBOSS

# Command line tools for sequence verification
CLUSTAL_DIR = "C:/Program Files (x86)/clustal-omega-1.2.0-win32"
EMBOSS_DIR = "C:\mEMBOSS"

BASE_URI = "http://sbolstandard.org/examples"

PROMOTER = "http://purl.obolibrary.org/obo/SO_0000167"
RBS = "http://purl.obolibrary.org/obo/SO_0000552"
CDS = "http://purl.obolibrary.org/obo/SO_0000316"
TERMINATOR = "http://purl.obolibrary.org/obo/SO_0000141"
USER_DEFINED = "http://purl.obolibrary.org/obo/SO_0000001"
DESIGN = "http://purl.obolibrary.org/obo/SO_0000546"
SCAR = "http://purl.obolibrary.org/obo/SO_0001953"

SO_INSERTION = "http://purl.obolibrary.org/obo/SO_0000667"
SO_DELETION = "http://purl.obolibrary.org/obo/SO_0000159"
SO_POSSIBLE_ASSEMBLY_ERROR = "http://purl.obolibrary.org/obo/SO_0000702"
SO_SUBSTITUTION = "http://purl.obolibrary.org/obo/SO_1000002"
SO_NUCLEOTIDE_MATCH = "http://purl.obolibrary.org/obo/SO_0000347"

col_map = {}
col_map['red']     = (0.95, 0.30, 0.25)
col_map['green']   = (0.38, 0.82, 0.32)
col_map['blue']    = (0.38, 0.65, 0.87)
col_map['orange']  = (1.00, 0.75, 0.17)
col_map['purple']  = (0.55, 0.35, 0.64)

random.seed()

def populate_subcomponents(parent_component):
    for ann in parent_component.annotations:
        i_start = ann.start - 1
        i_end = ann.end
        sub_seq_nucleotides = parent_component.sequence.nucleotides[i_start:i_end]
        #ann.subComponent = sbol.DNAComponent(doc, '%s//subComponent' %ann.uri)
        ann.subcomponent.sequence = sbol.DNASequence(doc, '%s//Sequence' %ann.subcomponent.uri )
        ann.subcomponent.sequence.nucleotides = sub_seq_nucleotides

def find_sequence_homologs(target_seq):
    result_handle = NCBIWWW.qblast("blastn", "nt", target_seq)
    blast_records = list(NCBIXML.parse(result_handle))
    rec = blast_records[0]

    E_VALUE_THRESH = 0.04
    variant_acc_nos = []
    variant_nucleotides = []
    variant_urls = []
    for alignment in rec.alignments:
        hsp = alignment.hsps[0]  # high-scoring pairs
        variant_acc_nos.append( str(alignment.accession) )
        variant_nucleotides.append( str(hsp.sbjct) )
        #cds_variant_urls.append(alignment.accession)

    return variant_acc_nos, variant_nucleotides, variant_urls

def remove_annotation(parent_component, deleted_ann):
    """ An annotation is removed.  The precedes relationship, start and end indexes of other annotations
    are updated accordingly """

    downstream_ann = deleted_ann.precedes[0]  # Find annotation downstream of the one to be removed

    # Finds the upstream annotation that precedes the annotation to be removed
    for ann in parent_component.annotations:
        if deleted_ann in ann.precedes:
            upstream_ann = ann

    # Update precedes relationship of annotations
    upstream_ann.precedes.remove(upstream_ann.precedes[0])
    upstream_ann.precedes.append(downstream_ann)

    # Update all start and end indices for annotations downstream from insertion
    deletion_size = deleted_ann.end - deleted_ann.start + 1
    while (len(upstream_ann.precedes) > 0):
        downstream_ann = upstream_ann.precedes[0]
        old_start = downstream_ann.start
        old_end = downstream_ann.end
        new_start = old_start - deletion_size
        new_end = old_end - deletion_size
        downstream_ann.start = new_start
        downstream_ann.end = new_end
        upstream_ann = downstream_ann

    #doc.sequences.remove(deleted_ann.subcomponent.sequence)
    #doc.components.remove(deleted_ann.subcomponent)
    #doc.annotations.remove(deleted_ann)
    parent_component.annotations.remove(deleted_ann)


def insert_annotation_downstream(parent_component, upstream_ann, insert_ann):
    """ A new annotation is inserted after an upstream annotation.
    The precedes relationship, start and end indexes are update accordingly.
    The annotation is expected to have a subComponent and Sequence object attached"""
    parent_component.annotations.append(insert_ann)

    # Update start and end of annotation
    insert_size = insert_ann.end
    insert_ann.start = upstream_ann.end + 1
    insert_ann.end = upstream_ann.end + insert_size

    # Update precedes relationship of annotations
    # If inserting annotation between two existing annotations
    if upstream_ann.precedes:
        downstream_ann = upstream_ann.precedes[0]  # Assumes annotations only have one precedes relationship
        upstream_ann.precedes.remove(upstream_ann.precedes[0])
        upstream_ann.precedes.append(insert_ann)
        insert_ann.precedes.append(downstream_ann)
    else:  # If there is no annotation to the right
        upstream_ann.precedes.append(insert_ann)

    # Update all start and end indices for annotations downstream from insertion
    upstream_ann = insert_ann
    while (len(upstream_ann.precedes) > 0):
        downstream_ann = upstream_ann.precedes[0]
        old_start = downstream_ann.start
        old_end = downstream_ann.end
        new_start = old_start + insert_size
        new_end = old_end + insert_size
        downstream_ann.start = new_start
        downstream_ann.end = new_end
        upstream_ann = downstream_ann

def insert_annotation_upstream(parent_component, insert_ann, downstream_ann):
    """ A new annotation (upstream) is inserted before the downstream annotation
    The precedes relationship, start and end indexes are update accordingly """
    #print downstream_ann.uri
    #print
    for i_ann, ann in enumerate(parent_component.annotations):
        #print i_ann, ann.uri
        if downstream_ann in ann.precedes:
            upstream_uri = ann.uri  # finds the annotation upstream, because it owns the precedes
    print 'Upstream uri: %s' %upstream_uri
    upstream_ann = parent_component.annotations[upstream_uri]
    insert_annotation_downstream(parent_component, upstream_ann, insert_ann)

def assemble_subcomponents(parent_component):
    parent_seq_len = 0
    for ann in parent_component.annotations:
        parent_seq_len = parent_seq_len + len(ann.subcomponent.sequence.nucleotides)
    assembled_seq = 'n' * parent_seq_len
    for ann in parent_component.annotations:
        #assembled_seq[ann.start:ann.end] = ann.subcomponent.sequence.nucleotides
        assembled_seq = assembled_seq[:ann.start - 1] + \
                        ann.subcomponent.sequence.nucleotides + \
                        assembled_seq[ann.end:]
    parent_component.sequence.nucleotides = assembled_seq

def print_downstream_Annotations(ann):
    reader_head = ann
    print reader_head.uri,
    while reader_head.precedes:
        reader_head = reader_head.precedes[0]
        print '->', reader_head.uri,
    print

#def write_to_fasta(seq_name, nucleotides, col_length = 20) :
def write_to_fasta(entries, col_length = 20) :
    formatted_entries = []
    for seq_name, nts in entries:
        nts =  [ nts[i:i + col_length] for i in range(0, len(nts), col_length)]
        nts = '\n'.join(nts)
        formatted_entries.append( '>%s\n%s' %(seq_name, nts) )
    return '\r\n'.join(formatted_entries)



def parse_fasta(fasta_str):
    entries = fasta_str.split('>')
    entries = [entry.strip() for entry in entries]
    entries = [entry.encode('ascii','ignore') for entry in entries]
    entries = entries[1:]  # Sequence has empty entry '' at the beginning of the list
    if len(entries) < 1 :
        print('Invalid FASTA format')
        return
    else :
        parsed_entries = []
        for entry in entries :
            try:
                entry = entry.strip()
                tokens = entry.split('\n')
                seq_name = tokens[0]
                #nucleotides = '\r\n'.join(tokens[1:])
                nucleotides = ''.join(tokens[1:])
                nucleotides = nucleotides.replace('\r', '')
                parsed_entries.append((seq_name, nucleotides))
            except:
                print('Invalid entry: %s' %entry)
        return parsed_entries

def getSequenceAnnotationsAtBaseNo(parent_component, base_no, annotations_found = None):
    # Assumes parent_component is an SBOL data structure of the general form DNAComponent(->SequenceAnnotation->DNAComponent)n
    # where n+1 is an integer describing how many hierarchical levels are in the SBOL structure
    if not annotations_found :
        annotations_found = []
    # print "Searching for base no %d" %base_no
    # Look at each of this component's annotations, is the target base there?
    for ann in parent_component.annotations :
        # print ann.uri, ann.start, ann.end
        # If target base is found ...
        if base_no >= ann.start and base_no <= ann.end :
            #print "Annotation FOUND"
            annotations_found.append(ann)
            # Is this the lowest level of the hierarchy, or are there subcomponents?
            if ann.subcomponent and len(ann.subcomponent.annotations) > 0:
                #print "Descending one level"
                annotations_found = annotations_found[:-1]  # Remove parent annotation, continue search for leaf annotations
                sub_annotations_found = getSequenceAnnotationsAtBaseNo(ann.subcomponent, base_no, annotations_found)
                if len(sub_annotations_found) == len(annotations_found):  # If no leaf annotations were found at the lower level, replace the higher level annotation
                    #print "No sub annotations found"
                    annotations_found.append(ann)
                    return annotations_found
                else:
                    #print "Sub annotations found"
                    return sub_annotations_found
            else:
                #print "No sub annotations found"
                return annotations_found
    #print "Completing search at this level"
    return annotations_found
            #    return annotations_found
            # else :
            #     print base_no, ann.start, ann.end
            #     annotations_found.append(ann)
            #     return annotations_found

def verify_base(ref_base, query_base) :
    if ref_base.upper() == query_base.upper() :
        return SO_NUCLEOTIDE_MATCH
    elif ref_base == '-' and query_base.upper() == 'N':
        return SO_POSSIBLE_ASSEMBLY_ERROR
    elif ref_base == '-' and query_base.upper() in ['A', 'C', 'T', 'G'] :
        return SO_INSERTION
    elif ref_base.upper() in ['A', 'C', 'T', 'G'] and query_base.upper() == 'N' :
        return SO_POSSIBLE_ASSEMBLY_ERROR
    elif ref_base.upper() in ['A', 'C', 'T', 'G'] and query_base == '-' :
        return SO_DELETION
    elif not ref_base.upper() == query_base.upper() :
        return SO_SUBSTITUTION
    raise sbol.SBOLError('Alignment contains unrecognized character %s or %s' %(ref_base,query_base))

# def classify_mutation(ref_base, query_base) :
#     if ref_base.upper() == query_base.upper() :
#         return None
#     elif ref_base == '-' and query_base.upper() == 'N':
#         return None
#     elif ref_base == '-' and query_base.upper() in ['A', 'C', 'T', 'G'] :
#         return SO_INSERTION
#     elif ref_base.upper() in ['A', 'C', 'T', 'G'] and query_base == 'N' :
#         return SO_POSSIBLE_ASSEMBLY_ERROR
#     elif ref_base.upper() in ['A', 'C', 'T', 'G'] and query_base == '-' :
#         return SO_DELETION
#     elif not ref_base.upper() == query_base.upper() :
#         return SO_SUBSTITUTION
#     return None

def is_mutation(dna_component) :
    if dna_component.type in [
        SO_INSERTION,
        SO_DELETION,
        SO_SUBSTITUTION,
    ]:
        return True
    else:
        return False

def is_ambiguity(dna_component) :
    if dna_component.type == SO_POSSIBLE_ASSEMBLY_ERROR:
        return True
    else:
        return False

def is_match(dna_component) :
    if dna_component.type == SO_NUCLEOTIDE_MATCH:
        return True
    else:
        return False

# def calculate_identity(dna_component) :
#     reference_seq = dna_component.sequence.nucleotides
#     mutations = []
#     for i_base, base in enumerate(reference_seq):
#         ann_found = getSequenceAnnotationsAtBaseNo(dna_component, i_base)
#         for ann in ann_found:
#             if is_mutation(ann.subcomponent):
#                 mutations.append(ann)
#     identity = (1. - float(len(mutations))/float(len(reference_seq))) * 100.
#     return identity

def flatten_subtree(dc, children_annotations=[]):
    for ann in dc.annotations:
        if ann.subcomponent:
            children_annotations = flatten_subtree(ann.subcomponent, children_annotations)
    children_annotations.extend(dc.annotations)
    children_annotations = list(set(children_annotations))
    return children_annotations

def calculate_identity(dna_component) :
    matched_regions = []
    reference_seq = dna_component.sequence.nucleotides
    for ann in flatten_subtree(dna_component):
        if is_match(ann.subcomponent):
            region_length = ann.end - ann.start + 1
            print ann.start, ann.end, region_length
            matched_regions.append(region_length)
    total_matched = sum(matched_regions)
    identity = float(total_matched)/float(len(reference_seq)) * 100.
    print "Identity", total_matched, len(reference_seq)
    return identity

def calculate_error(dna_component) :
    mismatched_regions = []
    reference_seq = dna_component.sequence.nucleotides
    for ann in flatten_subtree(dna_component):
        if is_mutation(ann.subcomponent):
            region_length = ann.end - ann.start + 1
            print ann.start, ann.end, region_length

            mismatched_regions.append(region_length)
    total_mismatched = sum(mismatched_regions)
    percent_mismatched = float(total_mismatched)/float(len(reference_seq)) * 100.
    print "Error", total_mismatched, len(reference_seq)
    return percent_mismatched

def calculate_ambiguity(dna_component) :
    ambiguous_regions = []
    reference_seq = dna_component.sequence.nucleotides
    for ann in flatten_subtree(dna_component):
        if is_ambiguity(ann.subcomponent):
            region_length = ann.end - ann.start + 1
            print ann.start, ann.end, region_length

            ambiguous_regions.append(region_length)
    total_ambiguous_region = sum(ambiguous_regions)
    percent_ambiguity = float(total_ambiguous_region)/float(len(reference_seq)) * 100.
    print "Ambiguity", total_ambiguous_region, len(reference_seq)
    return percent_ambiguity

def calculate_coverage(dna_component) :
    covered_regions = []
    reference_seq = dna_component.sequence.nucleotides
    for ann in flatten_subtree(dna_component):
        if is_match(ann.subcomponent) or is_mutation(ann.subcomponent) or is_ambiguity(ann.subcomponent):

            region_length = ann.end - ann.start + 1
            print ann.start, ann.end, region_length

            covered_regions.append(region_length)
    total_covered_region = sum(covered_regions)
    percent_coverage = float(total_covered_region)/float(len(reference_seq)) * 100.
    print "Coverage:", total_covered_region, len(reference_seq)
    return percent_coverage


parts_length_dist = {
    PROMOTER : 50,
    RBS : 15,
    CDS : 1000,
    TERMINATOR : 100
}

def n():
    r = random.random()
    if r <= 0.25 :
        return 'a'
    elif r <= 0.5 :
        return 't'
    elif r <= 0.75 :
        return 'c'
    elif r <= 1 :
        return 'g'

def nnn(seq_length):
    seq = ''
    for i in range(0, seq_length) :
        seq = seq +  n()
    return seq

def random_part_length(part_type):
    mu_length = parts_length_dist[part_type]
    sigma_length = 0.2 * parts_length_dist[part_type]
    return int ( random.gauss( mu_length, sigma_length ))

def qc(design, data=None, infile=None):
    if infile:
        with open (infile, "r") as f:
            data = f.read()
    if data:
        if len(parse_fasta(data)) > 1 :
            multialignment = align(data)
            clone = find_consensus(multialignment)
        else:
            clone = data
        target_design = write_to_fasta( [(design.uri, design.sequence.nucleotides)] )
        alignment_qc = align(target_design + '\r\n' + clone, outfile='%s.align' %design.display_id)

        # Scan alignment and classify mutations
        design_seq = design.sequence.nucleotides
        reference_seq = parse_fasta(alignment_qc)[0][1][:]
        query_seq = parse_fasta(alignment_qc)[1][1][:]
        assert len(reference_seq) == len(query_seq)

        # Translate alignment coordinates into coordinates of the reference and query sequences
        l_alignment = len(reference_seq)  # Determine length of alignment
        l_ref = len(reference_seq.replace('-', ''))
        l_que = len(query_seq.replace('-', ''))

        # The following dictionaries are used like lists indexed from one
        ref_map = {}  # Maps nucleotide coordinates of reference sequence to alignment coordinates
        i_ref = 0

        # If the design sequence is not fully covered by sequencing data, there may be '---' padding the end of
        # the query sequence.  The following indices mark the padded regions of the query_seq
        # Eg,
        # ref actggtca
        # qry --tggt--
        #
        i_left = query_seq.index(next(token for token in query_seq if not token == '-'))
        i_right = len(query_seq)- query_seq[::-1].index(next(token for token in reversed(query_seq) if not token == '-'))

        for i_alignment in range(l_alignment):
            ref_base = reference_seq[i_alignment]
            que_base = query_seq[i_alignment]
            if not ref_base == '-':
                i_ref += 1
            # Do not map the design coordinates to alignment coordinates if they aren't covered
            if i_alignment >= i_left and i_alignment <= i_right:
                ref_map[i_ref] = i_alignment

        # Should be a unit test
        #for i in range(0, l_ref):
        #    assert design_sequence[i] == reference_seq[ref_map[i+1]], "%d %s does not match %s"%(i,design_sequence[i], reference_seq[ref_map[i+1]])

        # Only leaf annotations at the bottom of the hierarchy are annotated...
        leaf_annotations = []
        for i_design in range(len(design_seq)):
            target_annotations = getSequenceAnnotationsAtBaseNo(design, i_design)
            for ann in target_annotations:
                if not ann in leaf_annotations:
                    leaf_annotations.append(ann)

        # Slice the alignment into segments that pertain to each annotation,
        # then determine the covered bases in the annotation.  All, part, or several discontiguous parts of an annotation
        # may be covered
        for i_ann, ann in enumerate(leaf_annotations):
            covered_coordinates = ref_map.keys()  # List of all base coordinates for this design / reference sequence that are covered
            # Now narrow down to find just the bases in this annotation
            covered_coordinates = [ x for x in covered_coordinates if x >= ann.start and x <= ann.end ]
            # Now translate into alignment coordinates
            alignment_coordinates = [ ref_map[x] for x in covered_coordinates ]
            if len(alignment_coordinates) > 0:

                alignment_start = min(alignment_coordinates)
                alignment_end = max(alignment_coordinates)

                # Scan alignment
                print "Verifying %s from %d to %d" %(ann.subcomponent.display_id, ann.start, ann.end)
                print ''.join([ nt for nt in reference_seq[alignment_start:alignment_end]])
                print ''.join([ nt for nt in query_seq[alignment_start:alignment_end]])

                # Classification of alignment
                base_comparisons = [ verify_base(reference_seq[x], query_seq[x]) for x in alignment_coordinates ]
                for x in alignment_coordinates:
                    comparison = verify_base(reference_seq[x], query_seq[x])
                    if comparison == None:
                        print x, reference_seq[x], query_seq[x]
                # Select a contiguous region of interest in alignment coordinates
                # TODO: replace while with for
                i_alignment = 0
                regions = []
                region_classifications = []
                while i_alignment < len(base_comparisons):
                    current_term = base_comparisons[i_alignment]
                    if i_alignment == 0:
                        reg_start = 0
                        reg_end = 0
                        previous_term = None
                    elif i_alignment > 0 and i_alignment < (len(base_comparisons) - 1):
                        # Mark end of an old region of interest and beginning of a new region
                        if not current_term == previous_term:
                            ref_start = covered_coordinates[reg_start] # Translate from alignment to design / reference coordinates
                            ref_end = covered_coordinates[reg_end] # Translate from alignment to design / reference coordinates
                            region_of_interest = ((ref_start, ref_end), previous_term)
                            regions.append(region_of_interest)
                            reg_start = i_alignment
                            reg_end = i_alignment
                        # Else extend the old region of interest to include the current coordinate
                        elif current_term == previous_term:
                            reg_end = i_alignment
                    elif i_alignment == (len(base_comparisons) - 1):
                        if not current_term == previous_term:
                            reg_start = i_alignment
                            reg_end = i_alignment
                            ref_start = covered_coordinates[reg_start] # Translate from alignment to design / reference coordinates
                            ref_end = covered_coordinates[reg_end] # Translate from alignment to design / reference coordinates
                            region_of_interest = ((ref_start, ref_end), previous_term)
                            regions.append(region_of_interest)
                        elif current_term == previous_term:
                            reg_end = i_alignment
                            ref_start = covered_coordinates[reg_start] # Translate from alignment to design / reference coordinates
                            ref_end = covered_coordinates[reg_end] # Translate from alignment to design / reference coordinates
                            region_of_interest = ((ref_start, ref_end), previous_term)
                            regions.append(region_of_interest)
                    #print i_alignment, current_term, reg_start, reg_end, covered_coordinates[reg_start], covered_coordinates[reg_end]
                    previous_term = current_term
                    i_alignment += 1

                # TODO: add unit test checking that the first region starts and the last region ends

                # TODO: add unit test checking that two distinct regions of interest can be demarcated

                # TODO: add unit test checking a single base region of interest at the beginning or the start

                # TODO: add unit test checking if first or last bases of query are '-'.  These are currently classified as
                # insertions, but are in fact uncovered regions

                # Create SequenceAnnotations for QC'd regions
                doc = design.doc
                for i_region, region in enumerate(regions):
                    print i_region
                    qc_start, qc_end = region[0]
                    qc_classification = region[1]
                    n_components = len(doc.components)
                    n_annotations = len(doc.annotations)
                    if qc_classification :
                        if qc_classification == SO_NUCLEOTIDE_MATCH:  # The reference sequence matches the query sequence
                            annotated_region = sbol.SequenceAnnotation(doc, "%s/MatchedSequence/SA%d" %(design.uri, n_annotations))
                            annotated_region.start = qc_start
                            annotated_region.end = qc_end
                            annotated_region.subcomponent = sbol.DNAComponent(doc,"%s/MatchedSequence/SA%d/DC%d" %(design.uri, n_annotations, n_components) )
                            annotated_region.subcomponent.display_id = ""
                            annotated_region.subcomponent.type = qc_classification
                        else:  # A mismatch was identified
                            annotated_region = sbol.SequenceAnnotation(doc, "%s/AssemblyErrors/SA%d" %(design.uri, n_annotations))
                            annotated_region.start = qc_start
                            annotated_region.end = qc_end
                            annotated_region.subcomponent = sbol.DNAComponent(doc,"%s/AssemblyErrors/SA%d/DC%d" %(design.uri, n_annotations, n_components) )
                            annotated_region.subcomponent.display_id = ""
                            annotated_region.subcomponent.type = qc_classification
                    print "Adding %s to %s from %d to %d" %(annotated_region.uri, ann.subcomponent.display_id, annotated_region.start, annotated_region.end)
                    ann.subcomponent.annotations.append(annotated_region)

def align(sequencing_data, outfile = None):
    """
    Sequencing data is a string in FASTA format
    """
    if outfile != None :
        print ("Aligning")
        # align_sequences = Popen(['%s\clustalo.exe' % CLUSTAL_DIR, '-i', '-'], stdin=PIPE, stdout=PIPE, stderr=STDOUT, cwd=DATA_DIR)
        align_sequences = Popen(['%s\clustalo.exe' % CLUSTAL_DIR, '-i', '-', '-o', '%s'%outfile, '--outfmt', 'msf'], stdin=PIPE, stdout=PIPE, stderr=STDOUT)
        alignment = align_sequences.communicate(sequencing_data)[0].decode()
        align_sequences.terminate()
    align_sequences = Popen(['%s\clustalo.exe' % CLUSTAL_DIR, '-i', '-'], stdin=PIPE, stdout=PIPE, stderr=STDOUT)
    alignment = align_sequences.communicate(sequencing_data)[0].decode()
    align_sequences.terminate()
    return alignment

def find_consensus(alignment):
    find_consensus = Popen(['%s\cons.exe' % EMBOSS_DIR, '-filter', '-identity', '2'], stdin=PIPE, stdout=PIPE, stderr=STDOUT)
    consensus = find_consensus.communicate(input=alignment)[0].decode()
    find_consensus.terminate()
    return consensus

def initialize_design(doc):
    n_designs = len([part for part in doc.components if part.type and part.type == DESIGN])
    root = sbol.DNAComponent(doc, '%s/Design_%d' %(BASE_URI, n_designs + 1))
    root.type = DESIGN
    root.display_id = 'Design %d' %(n_designs + 1)
    root.name = 'Design %d' %(n_designs + 1)
    root.sequence = sbol.DNASequence(doc, '%s/Design_%d/Seq_%d' %(BASE_URI, n_designs + 1, n_designs + 1))
    root.sequence.nucleotides = 'n'
    return root

def construct_design(doc, root, target_design):
    # target_design is a list of part uris
    n_components = len(doc.components)
    n_annotations = len(doc.annotations)
    n_sequences = len(doc.sequences)


    sbol_parts = []
    for uri in target_design:
        #uri = uris[part_name]
        part = doc.components[uri]
        SA = sbol.SequenceAnnotation(doc, '%s/SA_%d' %(root.uri, n_annotations + 1))
        n_annotations += 1
        if not part.sequence:
            part.sequence = sbol.DNASequence(doc, '%s/Seq_%d' %(part.uri, n_sequences + 1))
            part.sequence.nucleotides = 'n'
        SA.start = 1
        SA.end = len(part.sequence.nucleotides)
        SA.orientation = '+'
        sbol_parts.append(SA)
        SA.subcomponent = part

    root.annotations.append(sbol_parts[0])
    for i_part in range(1, len(sbol_parts)):
        upstream_ann = sbol_parts[i_part - 1]
        downstream_ann = sbol_parts[i_part]
        insert_annotation_downstream( root, upstream_ann, downstream_ann )

    assemble_subcomponents(root)
    #for part in sbol_parts:
    #    print part.start, part.end, part.subcomponent.name, part.subcomponent.type, part.subcomponent.uri

    return root

def scrape_parts(doc, part_files, parts_list, TARGET_DIR = '.'):
    # Scrape parts from files
    # doc is the Document to which the scraped parts will be added
    # part_files should be a list of file names without .xml extension
    for pf in part_files:
        print pf
        sbol_in = sbol.Document()
        sbol_in.read(TARGET_DIR + '/' + pf + '.xml')
        print "Components in infile", len(sbol_in.components)

        for i_dc, dc in enumerate(sbol_in.components):
            try:
                if dc.uri in parts_list:
                    dc.move(doc)
            except:
                print 'error in ', i_dc
        libsbol.deleteDocument(sbol_in.ptr)
    return doc
