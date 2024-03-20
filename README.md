# DNAplotlib

DNAplotlib is a library that enables highly customizable visualization of individual genetic constructs and libraries of design variants. It can be thought of in many ways as matplotlib for genetic diagrams. Publication quality vector-based output is produced and all aspects of the rendering process can be easily customized or replaced by the user. DNAplotlib is capable of SBOL Visual compliant diagrams in addition to a format able to better illustrate the precise location and length of each genetic part. This alternative "traced-based" visualization method enables direct comparison with nucleotide-level information such as RNA-seq read depth or other base resolution measures. While it is envisaged that access will be predominantly via the programming interface, several easy to use text-based input formats can be processed by a command-line scripts to facilitate broader usage. DNAplotlib is cross-platform and open-source software released under the OSI OSL-3.0 license.

If you make use of DNAplotlib in any publications, we kindly ask that the following paper is cited:

<a href="http://pubs.acs.org/doi/abs/10.1021/acssynbio.6b00252">Der B.S., Glassey E., Bartley B.A., Enghuus C., Goodman D.B., Gordon D.B., Voigt C.A., Gorochowski T.E., "DNAplotlib: programmable visualization of genetic designs and associated data", _ACS Synthetic Biology_, 2016. (DOI: 10.1021/acssynbio.6b00252)</a>

## Installation
The DNAplotlib library is contained within the `dnaplotlib.py` file in the `lib` directory and requires Python 3.6+ and matplotlib 3.8+. To install add the location of this file to your `PYTHONPATH` and you are good to: `import dnaplotlib`

## Getting Started
We provide an extensive gallery of use cases for DNAplotlib in the `gallery` directory. Click on a thumbnail below to go directly to the example code:

### Genetic Designs and Annotation
<a href="gallery/all_parts"><img src="gallery/all_parts/all_parts.png" height="160px"/></a>
<a href="gallery/xnor_truthtable"><img src="gallery/xnor_truthtable/xnor_truthtable.png" height="160px"/></a>
<a href="gallery/scatter_annotate"><img src="gallery/scatter_annotate/scatter_annotate.png" height="160px"/></a>
<a href="gallery/offset_features"><img src="gallery/offset_features/offset_features_y_offset.png" height="80px"/></a>
<a href="gallery/annotate_design"><img src="gallery/annotate_design/annotate_design.png" height="60px"/></a>
<a href="gallery/input_gff"><img src="gallery/input_gff/input_gff.png" height="50px"/></a>

### New Part Types and Regulation
<a href="gallery/recombinase_not_gate"><img src="gallery/recombinase_not_gate/recombinase_not_gate.png" height="160px"/></a>
<a href="gallery/recombinase_array"><img src="gallery/recombinase_array/recombinase_array.png" height="160px"/></a>

### Trace-based Rendering
<a href="gallery/multiple_traces"><img src="gallery/multiple_traces/multiple_traces.png" height="200px"/></a>
<a href="gallery/rotated_design"><img src="gallery/rotated_design/rotated_design.png" height="200px"/></a>
<a href="gallery/input_bed"><img src="gallery/input_bed/input_bed.png" height="200px"/></a>

### Dynamics and Evolution
<a href="gallery/repressilator_animate"><img src="gallery/repressilator_animate/repressilator_animate.png" height="380px"/></a>

### Variant Libraries
<a href="gallery/variants_library"><img src="gallery/variants_library/variants_library.png" height="500px"/></a>
<a href="gallery/order_orientation_library"><img src="gallery/order_orientation_library/order_orientation_library.png" height="500px"/></a>

## Build

Create a virtual env:

```shell
python3 -m venv .venv
```

activate the venv:

```shell
source .venv/bin/activate
```

Install dependancies

```shell
pip install -r requirements.txt
```

## Testing

The tests are using [pytest-mpl](https://github.com/matplotlib/pytest-mpl) to check if the gallery examples remain the same (image comparison with some tolerance).
The tests are run with github actions but you can also run it manually:

```shell
pip install -r requirements-test.txt
pytest --mpl
```
