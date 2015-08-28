DNAplotlib
==========

DNAplotlib is a library that enables highly customizable visualization of individual genetic constructs and libraries of design variants. It can be thought of in many ways as matplotlib for genetic diagrams. Publication quality vector-based output is produced and all aspects of the rendering process can be easily customized or replaced by the user. DNAplotlib is capable of SBOL Visual compliant diagrams in addition to a format able to better illustrate the precise location and length of each genetic part. This alternative "traced-based" visualization method enables direct comparison with nucleotide-level information such as RNA-seq read depth or other base resolution measures. While it is envisaged that access will be predominantly via the programming interface, several easy to use text-based input formats can be processed by a command-line scripts to facilitate broader usage. DNAplotlib is cross-platform and open-source software released under the OSI OSL-3.0 license.

DEPENDENCIES
============
NumPy, matplotlib

INSTALLATION
============

1. DNAPlotLib can be easily installed using setuptools, available here https://pypi.python.org/pypi/setuptools#downloads. (Setuptools is a stable and well-supported library that makes distributing Python projects easier):

2. Run the installer script in the project root directory using the following command line:
$ python setup.py install

3. To use DNAPlotLib:
>>> import dnaplotlib

4. To use pySBOL (if available on system):
>>> import dnaplotlib.sbol
