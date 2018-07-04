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
import matplotlib.lines as lines
from collections import namedtuple

__author__  = 'Thomas E. Gorochowski <tom@chofski.co.uk>'
__license__ = 'MIT'
__version__ = '2.0'

###############################################################################
# New Renderer
###############################################################################

# global constants 
MOVETO = 1
LINE = 2

# define named tuple called frame for containing glyph (struct)
Frame = namedtuple("Frame", "width height origin")

class GlyphRenderer:
    """ Class defining the part renders.
    """

    def __init__(self, glyph_path='glyphs/', global_defaults=None):
        self.glyphs_library, self.glyph_soterm_map = self.load_glyphs_from_path(glyph_path)
    
    def extract_tag_details(self, tag_attributes):
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

    def eval_svg_data(self, svg_text, parameters):
        # Use regular expression to extract and then replace with evaluated version
        # https://stackoverflow.com/questions/38734335/python-regex-replace-bracketed-text-with-contents-of-brackets
        svgpaths = re.sub(r"{([^{}]+)}", lambda m: str(eval(m.group()[1:-1], parameters)), svg_text)
        #print(svgpaths)
        return svgpaths

    def load_glyph(self, filename):
        tree = ET.parse(filename)
        root = tree.getroot()
        root_attributes = self.extract_tag_details(root.attrib)
        glyph_type = root_attributes['glyphtype']
        glyph_soterms = root_attributes['soterms']
        glyph_data = {}
        glyph_data['paths'] = []
        glyph_data['defaults'] = root_attributes['defaults']
        for child in root:
            # Cycle through and find all paths
            if child.tag.endswith('path'):
                glyph_data['paths'].append(self.extract_tag_details(child.attrib))
        return glyph_type, glyph_soterms, glyph_data

    def load_glyphs_from_path(self, path):
        glyphs_library = {}
        glyph_soterm_map = {}
        for infile in glob.glob( os.path.join(path, '*.svg') ):
            glyph_type, glyph_soterms, glyph_data = self.load_glyph(infile)
            glyphs_library[glyph_type] = glyph_data
            for soterm in glyph_soterms:
                glyph_soterm_map[soterm] = glyph_type
        return glyphs_library, glyph_soterm_map

    # helper function for getframe
    # get rectangular frame that fit raw svg extract
    def updateFrameParam(self, index, currParam, currParamPoint, newVertice):
        if newVertice[index] < currParamPoint[index]:
        	dis = currParamPoint[index] - newVertice[index]
        	currParam += dis
        	currParamPoint = newVertice
        else:
        	dis = newVertice[index] - currParamPoint[index]
        	if dis > currParam:
        		currParam = dis 
        return currParam, currParamPoint

    # helper function for draw_glyph
    # get rectangular frame that fit raw svg extract 
    def getframe(self, raw_paths):
        widthPoint, heightPoint, origin = ((0.0, 0.0) for i in range(3)) 
        width, height = (0.0 for i in range(2))
        for path in raw_paths:
            for vertice, code in path.iter_segments():
                # check and update origin
                if origin[0] == origin[1] and origin[0] == 0.0:
                    origin = (float(vertice[0]), float(vertice[1]))
                    widthPoint = origin
                    heightPoint = origin
                if vertice[0] < origin[0]:
                    origin = (float(vertice[0]), origin[1])
                elif vertice[1] < origin[1]:
                	origin = (origin[0], float(vertice[1])) 

                # check and update width (index 0) / height (index 1)
                width, widthPoint = self.updateFrameParam(0, width, widthPoint, vertice)
                height, heightPoint = self.updateFrameParam(1, width, heightPoint, vertice)
 
        return Frame(width, height, origin)

    # helper function for draw_glyph
    # get rectangular frame that fit raw svg extract
    def shiftToPosition(self, pathsToDraw, origFrame, pos):
        # shift paths
        newPath = []
        deltaX = pos[0] - origFrame.origin[0]
        deltaY = pos[1] - origFrame.origin[1]
        for path in pathsToDraw:
            verts, codes = ([] for i in range(2))
            for oldVert, code in path.iter_segments():
                newVert = (oldVert[0] + deltaX, oldVert[1] + deltaY)
                verts.append(newVert)
                codes.append(code)
            path = Path(verts, codes)
            newPath.append(path)

        return newPath

    # helper function to resizeToFrame
    # shift old vertice by scalefactor in reference to refpoint
    def shiftVert(self, ref, old, sfactor): 
        xdis = ref[0] - old[0] 
        ydis = ref[1] - old[1]
        newXdis = sfactor * xdis
        newYdis = sfactor * ydis 
        return [float(ref[0] - newXdis), float(ref[1] - newYdis)]
        
    # helper function for draw_glyph 
    # resize the path into scalefactor
    def resizeToFrame(self, pathsToD, refpoint, oldFrame, newFrame):
        newPath = []
        scalefactor = newFrame.width / oldFrame.width

        for path in pathsToD:
            verts, codes = ([] for i in range(2))
            for oldVert, code in path.iter_segments():
                newVert = self.shiftVert(refpoint, oldVert, scalefactor)
                verts.append(newVert)
                codes.append(code)
            path = Path(verts, codes)
            newPath.append(path)

        return newPath


    def draw_glyph(self, ax, glyph_type, position, size, user_parameters=None):
        # convert svg path into matplotlib path 
        glyph = self.glyphs_library[glyph_type]
        merged_parameters = glyph['defaults'].copy()
        if user_parameters is not None:
            # Collate parameters (user parameters take priority) 
            for key in user_parameters.keys():
                merged_parameters[key] = user_parameters[key]
        paths_to_draw = []
        for path in glyph['paths']:
            #if path['type'] not in ['bounding-box']:
            if path['type'] not in ['baseline', 'bounding-box']:
	            svg_text = self.eval_svg_data(path['d'], merged_parameters)
	            paths_to_draw.append(svg2mpl.parse_path(svg_text))

        
        # Draw glyph to the axis at position 
        initialFrame = self.getframe(paths_to_draw) 
        newFrame = Frame(width=size, height=size, origin=position)
        paths_to_draw = self.shiftToPosition(paths_to_draw, initialFrame, position)
        paths_to_draw = self.resizeToFrame(paths_to_draw, position, initialFrame, newFrame)

        for path in paths_to_draw:
            patch = patches.PathPatch(path, facecolor='white', edgecolor='black', lw=2)
            ax.add_patch(patch)

        # return type to be pieced together in StrandRenderer
        return {'identity': glyph_type, 'frame': newFrame}


class DesignRenderer:
    """ Class defining the rendering funtionality (assumes layout already generated).
    """

    def __init__(self):
        return None

# piece glyphs together 
class StrandRenderer:
	""" Class defining the strand for part renders.
    """

	def __init__(self):
		self.glyphs_contained = [] #primary sequence

	def addGlyphs(self, glyphAndFrame):
		self.glyphs_contained += glyphAndFrame

	# helper function for adjusting backbone axis
	def _convertXaxis(self, stX, eX, axis, ofset):
		xmin, xmax = axis 
		dis = xmax - xmin 
		start = (abs(xmin - stX) - ofset) / dis
		end = start + (eX - stX + ofset*2)/dis
		return start, end 

	# draw horizontal backbone strand line (drawn blue)
	def drawBackboneStrand(self, ax, offset=3, user_parameters=None):
		# need at least one glyph 
		#if len(self.glyphs_contained) == 0: return 

		startX, endX, height = (0. for i in range(3))
	
		for i in range(len(self.glyphs_contained)):
			glyphFrame = self.glyphs_contained[i]['frame']
			if i == 0:
				startX = glyphFrame.origin[0]
				endX = glyphFrame.origin[0] + glyphFrame.width
				Y = glyphFrame.origin[1]
			else:
				# update x axis 
				if glyphFrame.origin[0] < startX:
					startX = glyphFrame.origin[0]
				elif glyphFrame.origin[0] + glyphFrame.width > endX:
					endX = glyphFrame.origin[0] + glyphFrame.width
				# update y axis (defined by midpoint between glyph origin)
				if glyphFrame.origin[1] != Y:
					Y = (Y + glyphFrame.origin[1]) / 2.0
			
		start, end = self._convertXaxis(startX, endX, ax.get_xlim(), offset)	
		ax.axhline(y=Y, xmin=start, xmax=end)



###############################################################################
# Testing
###############################################################################

strand = StrandRenderer()
renderer = GlyphRenderer()
#print(renderer.glyphs_library['Promoter'])
#print('------------')
#print(renderer.glyph_soterm_map)


fig = plt.figure(figsize=(5,5))
ax = fig.add_subplot(111)
ax.set_xlim(-50.0, 50.0)
ax.set_ylim(-50.0, 50.0)

#for glyph_type in renderer.glyphs_library.keys():
insulator = renderer.draw_glyph(ax, 'Insulator', (0.0, 0.0), 20)
promoter = renderer.draw_glyph(ax, 'Promoter', (-30.0, 0.0), 20.)

strand.addGlyphs([insulator, promoter]) #primary sequence 
strand.drawBackboneStrand(ax)

ax.annotate('(-30.0, 0.0)', xy=[-30.0, 0.0], ha='center')
ax.annotate('(20.0, 0.0)', xy=[20.0, 0.0], ha='center')

ax.set_axis_off()
plt.show()



"""
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
