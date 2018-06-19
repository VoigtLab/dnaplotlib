#!/usr/bin/env python
"""
New DNAplotlib renderer that can handle new data type
"""

from datatype import *
import svgpath2mpl as svg2mpl

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


# https://github.com/yongyehuang/svg_parser
# https://docs.python.org/2/library/xml.etree.elementtree.html#module-xml.etree.ElementTree
# https://matplotlib.org/gallery/showcase/firefox.html#sphx-glr-gallery-showcase-firefox-py

class DesignRenderer:
    """ Class defining the rendering funtionality.
    """

    # Standard part types
    STD_PART_TYPES = ['Promoter', 
                      'CDS', 
                      'Terminator',
                      'RBS',
                      'Scar',
                      'Spacer',
                      'EmptySpace',
                      'Ribozyme',
                      'Ribonuclease',
                      'ProteinStability',
                      'Protease',
                      'Operator',
                      'Origin',
                      'Insulator',
                      '5Overhang',
                      '3Overhang',
                      'RestrictionSite',
                      'BluntRestrictionSite',
                      'PrimerBindingSite',
                      '5StickyRestrictionSite',
                      '3StickyRestrictionSite',
                      'UserDefined',
                      'Signature']

    # Standard regulatory types
    STD_REG_TYPES = ['Repression',
                     'Activation',
                     'Connection']

    def __init__(self, scale=1.0, linewidth=1.0, linecolor=(0,0,0), 
                 backbone_pad_left=0.0, backbone_pad_right=0.0):
        """ Constructor to generate an empty DNARenderer.

        Parameters
        ----------
        scale : float (default=1.0)
            A scaling factor for the plot. Only used if rendering traces.

        linewidth : float (default=1.0)
            The default linewidth for all part drawing.

        backbone_pad_left : float (default=0.0)
            Padding to add to the left side of the backbone.

        backbone_pad_right : float (default=0.0)
            Padding to add to the left side of the backbone.
        """
        self.scale = scale
        self.linewidth = linewidth
        self.linecolor = linecolor
        self.backbone_pad_left = backbone_pad_left
        self.backbone_pad_right = backbone_pad_right
        self.reg_height = 15

###############################################################################
# Testing
###############################################################################


def extract_tag_details(tag_attributes):
    tag_details = {}
    tag_details['type'] = None
    tag_details['defaults'] = None
    tag_details['d'] = None
    # Pull out the relevant details
    for key in tag_attributes.keys():
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
    glyph_data = {}
    glyph_data['paths'] = []
    glyph_data['defaults'] = extract_tag_details(root.attrib)['defaults']
    for child in root:
        # Cycle through and find all paths
        if child.tag.endswith('path'):
            glyph_data['paths'].append(extract_tag_details(child.attrib))
    return glyph_data


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





"""
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


