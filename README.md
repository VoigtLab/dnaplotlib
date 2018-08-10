# DNAplotlib supporting pySBOL2 

DNAplotlib is a library that enables highly customizable visualization of individual genetic constructs and libraries of design variants. The original repository is developed under Voight Lab in the following link: 
<a href="https://github.com/VoigtLab/dnaplotlib">Der B.S., Glassey E., Bartley B.A., Enghuus C., Goodman D.B., Gordon D.B., Voigt C.A., Gorochowski T.E., "DNAplotlib: programmable visualization of genetic designs and associated data", ACS Synthetic Biology, 2016. (DOI: 10.1021/acssynbio.6b00252)</a>

This folked repository is updated by Sunwoo Kang as a part of Google's Summer of Code 2018 project. Her work was guided by mentors Thomas Gorochowski and Bryan Bartley. The updates are mainly: 

1. making DNAplotlib compatible with <a href=http://sbolstandard.org/visual/glyphs/>SBOL Visual Standard 2</a>
1. Rendering of non-DNA components
2. Defining modules and interactions between them
3. Visualizing submodules within modules 
4. Importing/exporting design data from SBOL files

## List of Commits
<a href=https://github.com/swkang73/dnaplotlib/commits/master?after=e7ec582f68b08caeb8dbbe1cdec76be9a8a3d0f2+34/>ac58dd3</a> setup for rendering sbol files
<a href=https://github.com/swkang73/dnaplotlib/commits/master?after=e7ec582f68b08caeb8dbbe1cdec76be9a8a3d0f2+34/>e38ccd1</a> sanity check for componentDefinition & targer promoter file



## Installation
DNAplotlib is based on pySBOL2. Thus, the user need to first download the latest pySBOL package. The DNAplotlib library is contained within the `dnaplotlib.py` file in the `lib` directory and requires Python 2.6 and matplotlib 1.2 or newer. To install add the location of this file to your `PYTHONPATH` and you are good to: `import dnaplotlib`


## To Do 
- debug StopIteration Error during recursive reading of submodules 
- import/export csv files containing genetic circuit design data 
- read/save interaction into design data
- support user rendering customization (color, linewidth, etc)
