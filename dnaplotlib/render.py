#!/usr/bin/env python
"""
New DNAplotlib renderer that can handle new data type
"""

from datatype import *
import svgpath2mpl as svg2mpl

import os, glob, re, numpy as np
import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt, matplotlib.patches as patches, matplotlib.lines as lines
from matplotlib.path import Path
from collections import namedtuple


__author__  = 'Thomas E. Gorochowski <tom@chofski.co.uk>', 'Sunwoo Kang <swkang73@stanford.edu>'
__license__ = 'MIT'
__version__ = '2.0'

###############################################################################
# New Renderer
###############################################################################

# define named tuple called frame for containing glyph (struct)
Frame = namedtuple("Frame", "width height origin")

# Global const
STRANDZSCORE = 1.0 # low to send strand back
GLYPHZSCORE = 10.0 # high to send glyph front 

class GlyphRenderer:
    """ Class defining the part renders.
    """

    def __init__(self, glyph_path='glyphs/', global_defaults=None):
        self.glyphs_library, self.glyph_soterm_map = self.load_glyphs_from_path(glyph_path)
    
    # extract tag details for so term 
    def extract_tag_details(self, tag_attributes):
        tag_details = {}
        tag_details['glyphtype'] = None
        tag_details['soterms'] = []
        tag_details['defaults'] = None
        # Pull out the relevant details
        for key in tag_attributes.keys():
            if key == 'glyphtype':
                tag_details['glyphtype'] = tag_attributes[key]
            if key == 'soterms':
                tag_details['soterms'] = tag_attributes[key].split(';')
            if 'parametric' in key and key.endswith('}defaults'):
                split_defaults_text = tag_attributes[key].split(';')
                defaults = {}
                for element in split_defaults_text:
                    key_value = element.split(':')
                    defaults[key_value[0].strip()] = float(key_value[1].strip())
                tag_details['defaults'] = defaults
        
        return tag_details

    # extract tag details for path 
    def extract_tag_details_path(self, tag_attributes):
        tag_details = {}
        # Pull out the relevant details
        for key in tag_attributes.keys():
            if key == 'class':
                tag_details['type'] = tag_attributes[key]
            if 'parametric' in key and key.endswith('}y'): #y for baseline
                tag_details['y'] = tag_attributes[key]  
            elif 'parametric' in key and key.endswith('}d'): #path to be drawn
                tag_details['d'] = tag_attributes[key]
                      
        return tag_details


    # extract tag details for circle 
    def extract_tag_details_circle(self, tag_attributes):
        tag_details = {}
        tag_details['type'] = None # svg name
        tag_details['cx'] = None # x coord
        tag_details['cy'] = None # y coord
        tag_details['r'] = None # radius

        # Pull out the relevant details
        for key in tag_attributes.keys():
            if key == 'class':
                tag_details['type'] = tag_attributes[key]
            if 'parametric' in key and key.endswith('}cx'):
                tag_details['cx'] = float(tag_attributes[key])
            if 'parametric' in key and key.endswith('}cy'):
                tag_details['cy'] = float(tag_attributes[key])
            if 'parametric' in key and key.endswith('}r'):
                tag_details['r'] = float(tag_attributes[key])

        return tag_details

    def eval_svg_data(self, svg_text, parameters):
        # Use regular expression to extract and then replace with evaluated version
        # https://stackoverflow.com/questions/38734335/python-regex-replace-bracketed-text-with-contents-of-brackets
        svgpaths = re.sub(r"{([^{}]+)}", lambda m: str(eval(m.group()[1:-1], parameters)), svg_text)
        return svgpaths

    def load_glyph(self, filename):
        tree = ET.parse(filename)
        root = tree.getroot()
        root_attributes = self.extract_tag_details(root.attrib)
        glyph_type = root_attributes['glyphtype']
        glyph_soterms = root_attributes['soterms']
        glyph_data = {}
        glyph_data['paths'] , glyph_data['circles'] = ([] for i in range(2))
        glyph_data['defaults'] = root_attributes['defaults']
        for child in root:
            # Cycle through and find all paths and circles
            if child.tag.endswith('path'):
                glyph_data['paths'].append(self.extract_tag_details_path(child.attrib))
            elif child.tag.endswith('circle'):
                glyph_data['circles'].append(self.extract_tag_details_circle(child.attrib))
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

    # turn list of vertices into coordinates
    def list_into_coord(self, vlist):
        x, y = (0. for i in range(2))
        verts = []
        for i in range(len(vlist)):
            if i%2 == 0:
                x = float(vlist[i])
            else: 
                y = float(vlist[i])
                verts.append([x, y])
        return verts

    # helper function for getframe (width, height, origin)
    # get rectangular frame that fit raw svg extract
    def update_frame_param(self, index, curr_param, curr_param_point, new_vertice):
        if new_vertice[index] < curr_param_point[index]:
        	distance = curr_param_point[index] - new_vertice[index]
        	curr_param += distance
        	curr_param_point = new_vertice
        else:
        	distance = new_vertice[index] - curr_param_point[index]
        	if distance > curr_param:
        		curr_param = distance
        return curr_param, curr_param_point

    # helper function for draw_glyph
    # get rectangular frame that fit raw svg extract 
    def getframe(self, raw_paths):
        width_point, height_point, origin = ((0.0, 0.0) for i in range(3)) 
        width, height, index = (0.0 for i in range(3))
        for path in raw_paths:
            for vertices, code in path.iter_segments():
                verts = self.list_into_coord(vertices)
                for vert in verts:
                    if index == 0: # check initialization
                        origin = (float(vert[0]), float(vert[1]))
                        width_point = origin
                        height_point = origin
                        index += 1
                    if vert[0] < origin[0]:
                        origin = (float(vert[0]), origin[1])
                    if vert[1] < origin[1]:
                        origin = (origin[0], float(vert[1])) 
                    # check and update width (index 0) / height (index 1)
                    width, width_point = self.update_frame_param(0, width, width_point, vert)
                    height, height_point = self.update_frame_param(1, width, height_point, vert)
 
        return Frame(width, height, origin)

    # helper function for shift_to_position
    # function that return translated set of vertices and codes
    def update_vertices(self, verts, code, dx, dy):
        new_verts, new_codes = ([] for i in range(2))
        verts = self.list_into_coord(verts)
        for vert in verts:
            new_vert = (float(vert[0]) + dx, float(vert[1]) + dy)
            new_verts.append(new_vert)
            new_codes.append(code)
        return new_verts, new_codes

    # helper function for draw_glyph
    def shift_to_position(self, paths_draw, orig_frame, pos):
        # shift paths
        new_path = []
        deltaX = pos[0] - orig_frame.origin[0]
        deltaY = pos[1] - orig_frame.origin[1]
        for path in paths_draw:
            verts, codes = ([] for i in range(2))
            for old_verts, code in path.iter_segments():
                new_vertices, new_codes = self.update_vertices(old_verts, code, deltaX, deltaY)
                verts += new_vertices
                codes += new_codes
            path = Path(verts, codes)
            new_path.append(path)

        return new_path

    # helper function to resize_to_frame
    # shift old vertice by scalefactor in reference to refpoint
    def shift_verts(self, ref, old_verts, sfactor, code_type): 
        new_verts, new_codes = ([] for i in range(2))
        old_vs = self.list_into_coord(old_verts)
        for old in old_vs:
            xdis = ref[0] - old[0] 
            ydis = ref[1] - old[1]
            newXdis = sfactor * xdis
            newYdis = sfactor * ydis 
            new_verts.append((float(ref[0] - newXdis), float(ref[1] - newYdis)))
            new_codes.append(code_type)       
        return new_verts, new_codes
        
    # helper function for draw_glyph 
    # resize the path into scalefactor
    def resize_to_frame(self, paths_to_d, refpoint, old_frame, new_frame):
        new_path = []
        if old_frame.width == old_frame.height and old_frame.width == 0: return # cannot calculate resize factor
        # calculate scae factor
        if new_frame.width != 0:
            scalefactor = new_frame.width / old_frame.width
        else:
            scalefactor = new_frame.height / old_frame.height
        # update paths by scale factor 
        for path in paths_to_d:
            verts, codes = ([] for i in range(2))
            for old_verts, code in path.iter_segments():
                new_verts, new_codes = self.shift_verts(refpoint, old_verts, scalefactor, code)
                verts += new_verts
                codes += new_codes
            path = Path(verts, codes)
            new_path.append(path)

        return new_path

    # helper function for rotate_at_position
    # rotate each vertices by degree angle
    def rotate_verts(self, old_verts, d_angle, code_type):
        new_v, new_c = ([] for i in range(2))
        old_verts = self.list_into_coord(old_verts)
        for old_vert in old_verts:
            x = old_vert[0] * np.cos(d_angle) - old_vert[1] * np.sin(d_angle)
            y = old_vert[0] * np.sin(d_angle) + old_vert[1] * np.cos(d_angle)
            new_v.append((x, y))
            new_c.append(code_type)
        return new_v, new_c

    # rotate paths at the counterclockwise dir of angle (in rad [-pi, pi])
    # return rotated path and updated paths
    def rotate_at_position(self, paths_to_rotate, pos, ang):
        new_path = []
        for path in paths_to_rotate:
            verts, codes = ([] for i in range(2))
            for old_verts, code in path.iter_segments():
                new_verts, new_codes = self.rotate_verts(old_verts, ang, code)
                verts += new_verts
                codes += new_codes
            path = Path(verts, codes)
            new_path.append(path)

        return new_path

    # helper function to extract y of baseline 
    def get_baseline_y(self, paths):
        for p in paths:
            if p['type'] == 'baseline':
                return float(p['y'])

    #helper function to correct_y_orientation 
    # add the deltas from baseline 
    def correct_y(self, old_verts, c, baseline):
        new_v, new_c = ([] for i in range(2))
        old_vs = self.list_into_coord(old_verts)
        for old_v in old_vs:
            new_v.append( (old_v[0], -(old_v[1] - baseline)) )
            new_c.append(c)
        return new_v, new_c

    # helper function to correct orientation 
    def correct_y_orientation(self, paths_t_d, baseline_y):
        corrected_path = []
        for path in paths_t_d:
            verts, codes = ([] for i in range(2))
            for off_verts, code in path.iter_segments():
                corr_v, new_c = self.correct_y(off_verts, code, baseline_y)
                verts += corr_v
                codes += new_c 
            path = Path(verts, codes)
            corrected_path.append(path)
        return corrected_path
            

    # function that turn cx, cy, r into circle path 
    def get_circle_path(self, circle):
        verts = [
            (circle['cx'] - circle['r'], circle['cy']),
            (circle['cx'] - circle['r'], circle['cy'] + circle['r']),
            (circle['cx'], circle['cy'] + circle['r']),
            (circle['cx'] + circle['r'], circle['cy'] + circle['r']),
            (circle['cx'] + circle['r'], circle['cy']),
            (circle['cx'] + circle['r'], circle['cy'] - circle['r']),
            (circle['cx'], circle['cy'] - circle['r']),
            (circle['cx'] - circle['r'], circle['cy'] - circle['r']),
            (circle['cx'] - circle['r'], circle['cy'])
        ]

        codes = [
            Path.MOVETO, 
            Path.CURVE3,
            Path.CURVE3,
            Path.CURVE3,
            Path.CURVE3,
            Path.CURVE3,
            Path.CURVE3,
            Path.CURVE3,
            Path.CURVE3
        ]

        return Path(verts, codes)

    # extract paths / circ from glyph the return raw paths to draw
    def get_rawpaths_to_draw(self, glyph, merged_params):
        new_paths_to_draw = []
        for path in glyph['paths']:
            if path['type'] not in ['baseline']:
                svg_text = self.eval_svg_data(path['d'], merged_params)
                new_paths_to_draw.append(svg2mpl.parse_path(svg_text))
        for circle in glyph['circles']:
            new_paths_to_draw.append(self.get_circle_path(circle))

        return new_paths_to_draw

    def draw_glyph(self, ax, glyph_type, position, size, angle, user_parameters=None):
        # convert svg path into matplotlib path 
        glyph = self.glyphs_library[glyph_type]
        merged_parameters = glyph['defaults'].copy()
        if user_parameters is not None:
            # Collate parameters (user parameters take priority) 
            for key in user_parameters.keys():
                merged_parameters[key] = user_parameters[key]
        paths_to_draw = self.get_rawpaths_to_draw(glyph, merged_parameters)

        # get & set frames
        initial_frame = self.getframe(paths_to_draw) 
        new_frame = Frame(width=size, height=size, origin=position)

        # update path positions 
        paths_to_draw = self.correct_y_orientation(paths_to_draw, self.get_baseline_y(glyph['paths']))
        paths_to_draw = self.shift_to_position(paths_to_draw, initial_frame, position)
        paths_to_draw = self.resize_to_frame(paths_to_draw, position, initial_frame, new_frame)
        paths_to_draw = self.rotate_at_position(paths_to_draw, position, angle)
        paths_to_draw = self.shift_to_position(paths_to_draw, self.getframe(paths_to_draw), position)

        # add paths 
        for path in paths_to_draw:
            print(path)
            patch = patches.PathPatch(path, facecolor='white', edgecolor='black', lw=2, zorder=GLYPHZSCORE)
            ax.add_patch(patch)

        # return type to be pieced together in StrandRenderer
        return {'identity': glyph_type, 'frame': self.getframe(paths_to_draw)}

# piece glyphs together 
class StrandRenderer:
	""" Class defining the strand for part renders.
    """

	def __init__(self):
		self.glyphs_contained = [] #primary sequence

	def add_glyphs(self, glyph_n_frame):
		self.glyphs_contained += glyph_n_frame

	# private
	# helper function for adjusting backbone axis
	def _convertXaxis(self, stX, eX, axis, ofset):
		xmin, xmax = axis 
		dis = xmax - xmin 
		start = (abs(xmin - stX) - ofset) / dis
		end = start + (eX - stX + ofset*2)/dis
		return start, end 

	# draw horizontal backbone strand line (drawn blue)
	def draw_backbone_strand(self, ax, y_loc, offset=3, user_parameters=None):
		start_x, end_x, height = (0. for i in range(3))
		for i in range(len(self.glyphs_contained)):
			glyph_frame = self.glyphs_contained[i]['frame']
			if i == 0:
				start_x = glyph_frame.origin[0]
				end_x = glyph_frame.origin[0] + glyph_frame.width
			else:
				# update x axis 
				if glyph_frame.origin[0] < start_x:
					start_x = glyph_frame.origin[0]
				elif glyph_frame.origin[0] + glyph_frame.width > end_x:
					end_x = glyph_frame.origin[0] + glyph_frame.width
			
		start, end = self._convertXaxis(start_x, end_x, ax.get_xlim(), offset)	
		ax.axhline(y=y_loc, xmin=start, xmax=end, zorder=STRANDZSCORE)
		strand_frame = Frame(width=(end_x - start_x + 2*offset), 
		height=0., # height updated to strokewidth later
		origin=(start_x - offset, y_loc)) 

		return {'identity': 'backbone-strand', 'frame': strand_frame}


# visualize module for hierarchical rendering
class ModuleRenderer:
	""" Class defining the strand for part renders.
    """
   

	def __init__(self):
		self.parts_contained = [] # glyphs + interaction

	def add_parts(self, glyph_n_frame):
		self.parts_contained += glyph_n_frame

	# draw horizontal backbone strand line (drawn blue)
	def draw_module_box(self, ax, x_offset=None, y_offset=None, user_parameters=None):
		max_x, max_y = (np.finfo(np.float128).min for i in range(2)) # initialize to minimum 
		min_x, min_y = (np.finfo(np.float128).max for i in range(2))

		if x_offset is None:
			x_offset = 1.5 # default x offset
		if y_offset is None:
			y_offset = 3 # default y offset

		for i in range(len(self.parts_contained)):
			part_frame = self.parts_contained[i]['frame']
			# extract min/max x, min/max y 
			if min_x > part_frame.origin[0]:
				min_x = part_frame.origin[0]
			if min_y > part_frame.origin[1]:
				min_y = part_frame.origin[1]
			if max_x < part_frame.origin[0] + part_frame.width:
				max_x = part_frame.origin[0] + part_frame.width
			if max_y < part_frame.origin[1] + part_frame.height:
				max_y = part_frame.origin[1] + part_frame.height

		p = patches.Rectangle((min_x - x_offset, min_y - y_offset), 
			(max_x - min_x + 2*x_offset), # width
			(max_y - min_y + 2*y_offset), # height
			fill=False)
		ax.add_patch(p)

		return Frame(width=(max_x - min_x + 2*x_offset), 
			height=(max_y - min_y + 2*y_offset),
			origin=(min_x - x_offset, min_y - y_offset))


###############################################################################
# Testing
###############################################################################

# default setting
strand = StrandRenderer()
renderer = GlyphRenderer()
module1 = ModuleRenderer()

#print(renderer.glyphs_library)
#print('------------')
#print(renderer.glyph_soterm_map)

fig, ax = plt.subplots(1, figsize=(8,10))
# need to set axis first 
ax.set_xlim(-50.0, 50.0)
ax.set_ylim(-50.0, 50.0)

promoter = renderer.draw_glyph(ax, 'Promoter', (-40., -30.), 50., 0.)
ax.annotate('(-40,-30)', xy=[-40,-30], ha='center')

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
