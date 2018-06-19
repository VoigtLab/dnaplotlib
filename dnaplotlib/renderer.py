#!/usr/bin/env python
"""
New DNAplotlib renderer that can handle new data type
"""

from datatype import *
from svgpath2mpl import *
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
        if 'parametric' in key and key.endswith('}id'):
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




#print(glyph_paths)
#print('\n')








# From: http://raphaeljs.com/icons/#firefox
#firefox = "M28.4,22.469c0.479-0.964,0.851-1.991,1.095-3.066c0.953-3.661,0.666-6.854,0.666-6.854l-0.327,2.104c0,0-0.469-3.896-1.044-5.353c-0.881-2.231-1.273-2.214-1.274-2.21c0.542,1.379,0.494,2.169,0.483,2.288c-0.01-0.016-0.019-0.032-0.027-0.047c-0.131-0.324-0.797-1.819-2.225-2.878c-2.502-2.481-5.943-4.014-9.745-4.015c-4.056,0-7.705,1.745-10.238,4.525C5.444,6.5,5.183,5.938,5.159,5.317c0,0-0.002,0.002-0.006,0.005c0-0.011-0.003-0.021-0.003-0.031c0,0-1.61,1.247-1.436,4.612c-0.299,0.574-0.56,1.172-0.777,1.791c-0.375,0.817-0.75,2.004-1.059,3.746c0,0,0.133-0.422,0.399-0.988c-0.064,0.482-0.103,0.971-0.116,1.467c-0.09,0.845-0.118,1.865-0.039,3.088c0,0,0.032-0.406,0.136-1.021c0.834,6.854,6.667,12.165,13.743,12.165l0,0c1.86,0,3.636-0.37,5.256-1.036C24.938,27.771,27.116,25.196,28.4,22.469zM16.002,3.356c2.446,0,4.73,0.68,6.68,1.86c-2.274-0.528-3.433-0.261-3.423-0.248c0.013,0.015,3.384,0.589,3.981,1.411c0,0-1.431,0-2.856,0.41c-0.065,0.019,5.242,0.663,6.327,5.966c0,0-0.582-1.213-1.301-1.42c0.473,1.439,0.351,4.17-0.1,5.528c-0.058,0.174-0.118-0.755-1.004-1.155c0.284,2.037-0.018,5.268-1.432,6.158c-0.109,0.07,0.887-3.189,0.201-1.93c-4.093,6.276-8.959,2.539-10.934,1.208c1.585,0.388,3.267,0.108,4.242-0.559c0.982-0.672,1.564-1.162,2.087-1.047c0.522,0.117,0.87-0.407,0.464-0.872c-0.405-0.466-1.392-1.105-2.725-0.757c-0.94,0.247-2.107,1.287-3.886,0.233c-1.518-0.899-1.507-1.63-1.507-2.095c0-0.366,0.257-0.88,0.734-1.028c0.58,0.062,1.044,0.214,1.537,0.466c0.005-0.135,0.006-0.315-0.001-0.519c0.039-0.077,0.015-0.311-0.047-0.596c-0.036-0.287-0.097-0.582-0.19-0.851c0.01-0.002,0.017-0.007,0.021-0.021c0.076-0.344,2.147-1.544,2.299-1.659c0.153-0.114,0.55-0.378,0.506-1.183c-0.015-0.265-0.058-0.294-2.232-0.286c-0.917,0.003-1.425-0.894-1.589-1.245c0.222-1.231,0.863-2.11,1.919-2.704c0.02-0.011,0.015-0.021-0.008-0.027c0.219-0.127-2.524-0.006-3.76,1.604C9.674,8.045,9.219,7.95,8.71,7.95c-0.638,0-1.139,0.07-1.603,0.187c-0.05,0.013-0.122,0.011-0.208-0.001C6.769,8.04,6.575,7.88,6.365,7.672c0.161-0.18,0.324-0.356,0.495-0.526C9.201,4.804,12.43,3.357,16.002,3.356z"

paths_to_draw = []

for path in glyph_data['paths']:
    if path['type'] != 'baseline':
        svg_text = eval_svg_data(path['d'], glyph_data['defaults'])
        paths_to_draw.append(svg2mpl.parse_path(svg_text))
 

print(paths_to_draw[0])

####################

# Make upside down

xmin = 0
xmax = 0
ymin = 0
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






























