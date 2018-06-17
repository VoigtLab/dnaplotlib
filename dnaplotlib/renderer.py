#!/usr/bin/env python
"""
New DNAplotlib renderer that can handle new data type
"""

from datatype import *

__author__  = 'Thomas E. Gorochowski <tom@chofski.co.uk>'
__license__ = 'MIT'
__version__ = '2.0'

###############################################################################
# New Renderer
###############################################################################

class PartRenderer:
    """ Class defining the part renders.
    """

    def __init__(self, part_library_filename):
        self.part_library_filename = part_library_filename
        # Load strings of the parametric SVG part definitions

    def render_svg(self, ax, svg_str, position):
        return 0

    def render_part(self, ax, part, position):
        return 0


# https://github.com/yongyehuang/svg_parser
# https://docs.python.org/2/library/xml.etree.elementtree.html#module-xml.etree.ElementTree


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

    def SBOL_part_renderers (self):
        """ Return dictionary of all standard built-in SBOL part renderers.
        """
        return {
            'Promoter'         :sbol_promoter, 
            'CDS'              :sbol_cds, 
            'Terminator'       :sbol_terminator,
            'RBS'              :sbol_rbs,
            'Scar'             :sbol_scar,
            'Spacer'           :sbol_spacer,
            'EmptySpace'       :sbol_empty_space,
            'Ribozyme'         :sbol_ribozyme,
            'Ribonuclease'     :sbol_ribonuclease,
            'ProteinStability' :sbol_protein_stability,
            'Protease'         :sbol_protease,
            'Operator'         :sbol_operator,
            'Origin'           :sbol_origin,
            'Insulator'        :sbol_insulator,
            '5Overhang'        :sbol_5_overhang,
            '3Overhang'        :sbol_3_overhang,
            'RestrictionSite'  :sbol_restriction_site,
            'BluntRestrictionSite'   :sbol_blunt_restriction_site,
            'PrimerBindingSite'      :sbol_primer_binding_site,
            '5StickyRestrictionSite' :sbol_5_sticky_restriction_site,
            '3StickyRestrictionSite' :sbol_3_sticky_restriction_site,
            'UserDefined'      :sbol_user_defined,
            'Signature'        :sbol_signature}

    def trace_part_renderers (self):
        """ Return dictionary of all standard built-in trace part renderers.
        """
        return {
            'Promoter'         :trace_promoter, 
            'CDS'              :trace_cds, 
            'Terminator'       :trace_terminator,
            'RBS'              :trace_rbs,
            'UserDefined'      :trace_user_defined} 

    def std_reg_renderers (self):
        """ Return dictionary of all standard built-in regulation renderers.
        """
        return {
            'Repression' :repress, 
            'Activation' :induce,
            'Connection' :connect}

    def renderDNA (self, ax, parts, part_renderers, regs=None, reg_renderers=None, plot_backbone=True):
        """ Render the parts on the DNA and regulation.

        Parameters
        ----------
        ax : matplotlib.axes
            Axes to draw the design to.

        parts : list(dict)
            The design to draw. This is a list of dicts, where each dict relates to
            a part and must contain the following keys:
            - name (string)
            - type (string)  
            - fwd (bool)
            - start (float, optional)
            - end (float, optional)
            These will then be drawn in accordance with the renders selected

        part_renderers : dict(functions)
            Dict of functions where the key in the part type and the dictionary returns
            the function to be used to draw that part type.

        regs : list(dict) (default=None)
            Regulation present in the design. This is a list of dicts, where each dict
            relates to a single regulation arc and must contain the following keys:
            - type (string)
            - from_part (part object dict)  
            - to_part (part object dict)
            These will then be drawn in accordance with the renders selected.

        reg_renderers : dict(functions) (default=None)
            Dict of functions where the key in the regulation type and the dictionary 
            returns the function to be used to draw that regulation type.

        Returns
        -------
        start : float
            The x-point in the axis space that drawing begins.

        end : float
            The x-point in the axis space that drawing ends.
        """
        # Update the matplotlib rendering default for drawing the parts (we want mitered edges)
        matplotlib.rcParams['lines.dash_joinstyle']  = 'miter'
        matplotlib.rcParams['lines.dash_capstyle']   = 'butt'
        matplotlib.rcParams['lines.solid_joinstyle'] = 'miter'
        matplotlib.rcParams['lines.solid_capstyle']  = 'projecting'
        # Make text editable in Adobe Illustrator
        matplotlib.rcParams['pdf.fonttype']          = 42 
        # Plot the parts to the axis
        part_num = 0
        prev_end = 0
        first_start = 0
        first_part = True

        for part in parts:
            keys = list(part.keys())

            # Check the part has minimal details required
            if 'type' in keys:
                if 'fwd' not in keys:
                    part['fwd'] = True
                if 'start' not in keys:
                    if part['fwd'] == True:
                        part['start'] = part_num
                    else:
                        part['start'] = part_num+1
                if 'end' not in keys:
                    if part['fwd'] == True:
                        part['end'] = part_num+1
                    else:
                        part['end'] = part_num
                # Extract custom part options (if available)
                part_opts = None
                if 'opts' in list(part.keys()):
                    part_opts = part['opts']
                # Use the correct renderer
                if 'renderer' in list(part.keys()):
                    # Use custom renderer
                    prev_start, prev_end = part['renderer'](ax, part['type'], part_num, 
                                     part['start'], part['end'], prev_end,
                                     self.scale, self.linewidth, 
                                     opts=part_opts)

                    #update start,end for regulation
                    #part['start'] = prev_start
                    #part['end'] = prev_end

                    if first_part == True:
                        first_start = prev_start
                        first_part = False
                else:
                    # Use standard renderer, if one exists
                    if part['type'] in list(part_renderers.keys()):
                        prev_start, prev_end = part_renderers[part['type']](ax, 
                                       part['type'], part_num, 
                                       part['start'], part['end'], 
                                       prev_end, self.scale, 
                                       self.linewidth, opts=part_opts)
                        
                        #update start,end for regulation [TEG]
                        if part['fwd'] == True:
                            part['start'] = prev_start
                            part['end'] = prev_end
                        else:
                            part['start'] = prev_end
                            part['end'] = prev_start
                        
                        if first_part == True:
                            first_start = prev_start
                            first_part = False
            part_num += 1
        
        # first pass to get all of the arcranges
        if regs != None:

            for reg in regs:
                keys = list(reg.keys())

                # Check the part has minimal details required
                if 'type' in keys and 'from_part' in keys and 'to_part' in keys:
                    # Extract custom part options (if available)

                    reg_opts = None
                    if 'opts' in list(reg.keys()):
                        reg_opts = reg['opts']
                    
                    if reg['type'] in list(reg_renderers.keys()):
                        
                        ##############################################################################
                        arcstart = (reg['from_part']['start'] + reg['from_part']['end']) / 2
                        arcend   = (reg['to_part']['start']   + reg['to_part']['end']) / 2
                        arcrange = [arcstart,arcend]
                        reg['arclength'] = math.fabs(arcstart-arcend)
                        reg['arc_height_index'] = 1
                        ##############################################################################

            #sort regs by arc ranges from shortest to longest
            regs.sort(key=lambda x: x['arclength'], reverse=False)

            reg_num = 0
            pos_arc_ranges = [] # arc above DNA backbone if to_part is fwd
            neg_arc_ranges = [] # arc below DNA backbone if to_part is reverse
            current_max = 1

            # second pass to render all the arcs
            for reg in regs:
                keys = list(reg.keys())

                # Check the part has minimal details required
                if 'type' in keys and 'from_part' in keys and 'to_part' in keys:
                    # Extract custom part options (if available)

                    reg_opts = None
                    if 'opts' in list(reg.keys()):
                        reg_opts = reg['opts']
                    
                    if reg['type'] in list(reg_renderers.keys()):
                        
                        ##############################################################################
                        # arc height algorithm: greedy from left-to-right on DNA design
                        
                        arcstart = (reg['from_part']['start'] + reg['from_part']['end']) / 2
                        arcend   = (reg['to_part']['start']   + reg['to_part']['end']) / 2
                        
                        arcmin = min(arcstart,arcend)
                        arcmax = max(arcstart,arcend)
                        arcrange = [arcmin,arcmax,reg['arc_height_index']]
                        arc_height_index = 1
                        
                        # arc above if to_part is fwd
                        if(reg['to_part']['fwd'] == True):
                            # find max arc height index of ONLY the prior arcs that clash with the current arc
                            current_max = 1
                            for r in pos_arc_ranges:
                                if  (arcrange[0] > r[0] and arcrange[0] < r[1]):
                                    if(r[2] > current_max):
                                        current_max = r[2]
                                elif(arcrange[0] > r[1] and arcrange[0] < r[0]):
                                    if(r[2] > current_max):
                                        current_max = r[2]
                                elif(arcrange[1] > r[0] and arcrange[0] < r[1]):
                                    if(r[2] > current_max):
                                        current_max = r[2]
                                elif(arcrange[1] > r[1] and arcrange[0] < r[0]):
                                    if(r[2] > current_max):
                                        current_max = r[2]
                                    
                            # if arcs cross over, increment the arc height index
                            for r in pos_arc_ranges:
                                if  (arcrange[0] > r[0] and arcrange[0] < r[1]):
                                    reg['arc_height_index'] = current_max + 1
                                    arcrange[2] = reg['arc_height_index']
                                elif(arcrange[0] > r[1] and arcrange[0] < r[0]):
                                    reg['arc_height_index'] = current_max + 1
                                    arcrange[2] = reg['arc_height_index']
                                elif(arcrange[1] > r[0] and arcrange[0] < r[1]):
                                    reg['arc_height_index'] = current_max + 1
                                    arcrange[2] = reg['arc_height_index']
                                elif(arcrange[1] > r[1] and arcrange[0] < r[0]):
                                    reg['arc_height_index'] = current_max + 1
                                    arcrange[2] = reg['arc_height_index']
                            pos_arc_ranges.append(arcrange)
                        
                        # arc below if to_part is reverse
                        else:
                            # find max arc height index
                            current_max = 1
                            for r in neg_arc_ranges:
                                if  (arcrange[0] > r[0] and arcrange[0] < r[1]):
                                    if(r[2] > current_max):
                                        current_max = r[2]
                                elif(arcrange[0] > r[1] and arcrange[0] < r[0]):
                                    if(r[2] > current_max):
                                        current_max = r[2]
                                elif(arcrange[1] > r[0] and arcrange[0] < r[1]):
                                    if(r[2] > current_max):
                                        current_max = r[2]
                                elif(arcrange[1] > r[1] and arcrange[0] < r[0]):
                                    if(r[2] > current_max):
                                        current_max = r[2]
                            
                            # if arcs cross over, increment the arc height index
                            for r in neg_arc_ranges:
                                if  (arcrange[0] > r[0] and arcrange[0] < r[1]):
                                    reg['arc_height_index'] = current_max + 1
                                    arcrange[2] = reg['arc_height_index']
                                elif(arcrange[0] > r[1] and arcrange[0] < r[0]):
                                    reg['arc_height_index'] = current_max + 1
                                    arcrange[2] = reg['arc_height_index']
                                elif(arcrange[1] > r[0] and arcrange[0] < r[1]):
                                    reg['arc_height_index'] = current_max + 1
                                    arcrange[2] = reg['arc_height_index']
                                elif(arcrange[1] > r[1] and arcrange[0] < r[0]):
                                    reg['arc_height_index'] = current_max + 1
                                    arcrange[2] = reg['arc_height_index']
                            neg_arc_ranges.append(arcrange)
                        ##############################################################################
                        reg_renderers[reg['type']](ax, reg['type'], 
                                       reg_num, reg['from_part'], 
                                       reg['to_part'], self.scale, 
                                       self.linewidth, reg['arc_height_index'], opts=reg_opts)
                reg_num += 1
        # Plot the backbone (z=1)
        if plot_backbone == True:
            l1 = Line2D([first_start-self.backbone_pad_left,prev_end+self.backbone_pad_right],[0,0], 
                        linewidth=self.linewidth, color=self.linecolor, zorder=10)
            ax.add_line(l1)
        return first_start, prev_end





###############################################################################
# Testing
###############################################################################

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
































