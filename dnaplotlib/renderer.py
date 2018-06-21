#!/usr/bin/env python
"""
New DNAplotlib renderer that can handle new data type
"""

from datatype import *
import svgpath2mpl as svg2mpl

import os
import glob
import xml.etree.ElementTree as ET
import re
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.path import Path
import matplotlib.patches as patches

__author__  = 'Thomas E. Gorochowski <tom@chofski.co.uk>'
__license__ = 'MIT'
__version__ = '2.0'

###############################################################################
# New Renderer
###############################################################################

class PartRenderer:
    """ Class defining the part renders.
    """

    def __init__(self, paths, parameters):
        self.part_library_filename = part_library_filename
        # Load strings of the parametric SVG part definitions

    def render_svg(self, ax, svg_str, position):
        return 0

    def render_part(self, ax, part, start_position):
        return 0

class DesignRenderer:
    """ Class defining the rendering funtionality (assumes layout already generated).
    """

    def __init__(self, ):
        return None
        

###############################################################################
# Testing
###############################################################################


def extract_tag_details(tag_attributes):
    tag_details = {}
    tag_details['glyphtype'] = None
    tag_details['soterms'] = []
    tag_details['type'] = None
    tag_details['defaults'] = None
    tag_details['d'] = None
    # Pull out the relevant details
    for key in tag_attributes.keys():
        if key == 'glyphtype':
            tag_details['glyphtype'] = tag_attributes[key]
        if key == 'soterms':
            tag_details['soterms'] = tag_attributes[key].split(';')
        if key == 'class':
            tag_details['type'] = tag_attributes[key]
        if 'parametric' in key and key.endswith('}d'):
            tag_details['d'] = tag_attributes[key]
        if 'parametric' in key and key.endswith('}defaults'):
            split_defaults_text = tag_attributes[key].split(';')
            defaults = {}
            for element in split_defaults_text:
                key_value = element.split(':')
                defaults[key_value[0].strip()] = float(key_value[1].strip())
            tag_details['defaults'] = defaults
    return tag_details


def eval_svg_data (svg_text, parameters):
    # Use regular expression to extract and then replace with evaluated version
    # https://stackoverflow.com/questions/38734335/python-regex-replace-bracketed-text-with-contents-of-brackets
    return re.sub(r"{([^{}]+)}", lambda m: str(eval(m.group()[1:-1], parameters)), svg_text)


def load_glyph(filename):
    tree = ET.parse(filename)
    root = tree.getroot()
    root_attributes = extract_tag_details(root.attrib)
    glyph_type = root_attributes['glyphtype']
    glyph_soterms = root_attributes['soterms']
    glyph_data = {}
    glyph_data['paths'] = []
    glyph_data['defaults'] = root_attributes['defaults']
    for child in root:
        # Cycle through and find all paths
        if child.tag.endswith('path'):
            glyph_data['paths'].append(extract_tag_details(child.attrib))
    return glyph_type, glyph_soterms, glyph_data


def load_glyphs_from_path(path):
    glyphs_library = {}
    glyph_soterm_map = {}
    for infile in glob.glob( os.path.join(path, '*.svg') ):
        glyph_type, glyph_soterms, glyph_data = load_glyph(infile)
        glyphs_library[glyph_type] = glyph_data
        for soterm in glyph_soterms:
            glyph_soterm_map[soterm] = glyph_type
    return glyphs_library, glyph_soterm_map


glyphs_library, glyph_soterm_map = load_glyphs_from_path('./glyphs/')

print(glyphs_library)
print('------------')
print(glyph_soterm_map)
"""

glyph_data = load_glyph('example.svg')
paths_to_draw = []
for path in glyph_data['paths']:
    if path['type'] not in ['baseline', 'bounding-box']:
        svg_text = eval_svg_data(path['d'], glyph_data['defaults'])
        paths_to_draw.append(svg2mpl.parse_path(svg_text))
 



####################
# Make upside down
xmin = 100
xmax = 0
ymin = 100
ymax = 0
fig = plt.figure(figsize=(5, 5))
ax = fig.add_axes([0.0, 0.0, 1.0, 1.0], frameon=False, aspect=1)
# Actual shape with black outline
for path in paths_to_draw:
    patch = patches.PathPatch(path, facecolor='orange', edgecolor='k', lw=2)
    ax.add_patch(patch)
    verts = path.vertices
    xmin, xmax = min(xmin, verts[:, 0].min()-1), max(xmax, verts[:, 0].max()+1)
    ymin, ymax = min(ymin, verts[:, 1].min()-1), max(ymax, verts[:, 1].max()+1)
# Centering
ax.set_xlim(xmin, xmax)
ax.set_ylim(ymin, ymax)
# No ticks
ax.set_xticks([])
ax.set_yticks([])
# Display
plt.show()
####################



def create_test_design ():
    design = Design('design1')
    # Create DNA module 1 (containing sub-modules)
    module1 = Module(design, None, 'module1')
    module1a = module1.add_module('module1a')
    module1a.add_part( Part(module1a, '1a','CDS') )
    module1b = module1.add_module('module1b')
    module1b.add_part( Part(module1b, '1b','CDS') )
    module1c = module1.add_module('module1c')
    module1c.add_part( Part(module1c, '1c','CDS') )
    # Create DNA module 2
    module2 = Module(design, None, 'module2')
    module2.add_part( Part(module2, '2','CDS') )
    # Attach the different DNA segments to design
    design.add_module(module1)
    design.add_module(module2)
    return design
# Let's try it out!
design = create_test_design()
design.print_design()
"""
