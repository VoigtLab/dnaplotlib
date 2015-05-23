#DNAplotlib

DNAplotlib is a computational toolkit that enables highly customizable visualization of individual genetic constructs and libraries of design variants. Publication quality vector-based output is produced and all aspects of the rendering process can be easily customized or replaced by the user. DNAplotlib is capable of SBOL Visual compliant diagrams in addition to a format able to better illustrate the precise location and length of each genetic part. This alternative visualization method enables direct comparison with nucleotide-level information such as RNA-seq read depth. While it is envisaged that access will be predominantly via the programming interface, several easy to use text-based input formats can be processed by a command-line scripts to facilitate broader usage. An experimental web front-end is also available.

##Installation
The DNAplotlib library is contained within the `dnaplotlib.py` file in the `lib` directory and requires Python 2.6 and matplotlib 1.2 or newer. To install add the location of this file to your `PYTHONPATH` and you are good to: `import dnaplotlib`

DNAplotlib is cross-platform and open-source software developed using Python and released under the OSI Open Software License 3.0 (OSL-3.0) license.

##Getting Started
We provide an extensive gallery of use cases for DNAplotlib in the `gallery` directory. Click on a thumbnail below to go directly to the example:

###Single Designs and Annotation
<a href="gallery/all_parts"><img src="gallery/all_parts/all_parts.png" height="200px"/></a>
<a href="gallery/xnor_truthtable"><img src="gallery/xnor_truthtable/xnor_truthtable.png" height="200px"/></a>
<a href="gallery/scatter_annotate"><img src="gallery/scatter_annotate/scatter_annotate.png" height="200px"/></a>

###New Part Types
<a href="gallery/recombinase_not_gate"><img src="gallery/recombinase_not_gate/recombinase_not_gate.png" height="200px"/></a>
<a href="gallery/recombinase_array"><img src="gallery/recombinase_array/recombinase_array.png" height="200px"/></a>

###Trace-based Rendering
<a href="gallery/multiple_traces"><img src="gallery/multiple_traces/multiple_traces.png" height="200px"/></a>
<a href="gallery/rotated_design"><img src="gallery/rotated_design/rotated_design.png" height="200px"/></a>

###Dynamics and Evolution
<a href="gallery/repressilator_animate"><img src="gallery/repressilator_animate/repressilator_animate.png" height="200px"/></a>

###Library Visualisation
<a href="gallery/variants_library"><img src="gallery/variants_library/variants_library.png" height="350px"/></a>
<a href="gallery/order_orientation_library"><img src="gallery/order_orientation_library/order_orientation_library.png" height="350px"/></a>




