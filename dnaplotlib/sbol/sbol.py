#!/usr/bin/env python
"""
DNAplotlib SBOL Functionality
=============================
"""
#    DNAplotlib
#    Copyright (C) 2015 by
#    Bryan Bartley <bartleyba@sbolstandard.org>
#    Thomas E. Gorochowski <tom@chofski.co.uk>
#    All rights reserved.
#    OSI Open Software License 3.0 (OSL-3.0) license.

import dnaplotlib
import sbol

matplotlib.use('TkAgg')

__author__  = 'Bryan Bartley <bartleyba@sbolstandard.org>\n\
               Thomas E. Gorochowski <tom@chofski.co.uk>, Voigt Lab, MIT'
__license__ = 'OSI OSL 3.0'
__version__ = '1.0'

class SBOLRenderer(dnaplotlib.DNARenderer):

	def SO_terms(self):
        """ Return dictionary of all standard built-in SBOL part renderers referenced by Sequence Ontology term
		"""
        return {
        'SO_0000167': 'Promoter',
        'SO_0000316': 'CDS',
        'SO_0000141': 'Terminator',
        'SO_0000552': 'RBS',
        'SO_0001953': 'Scar',
        # No SO Term : 'Spacer',
        #  No SO Term : 'EmptySpace',
        'SO_000037': 'Ribozyme',
        'SO_0001977': 'Ribonuclease',
        'SO_0001955': 'ProteinStability',
        'SO_0001956': 'Protease',
        'SO_0000057': 'Operator',
        # SO term insulator does not have same semantics : 'Insulator',
        'SO_0000296': 'Origin',
        'SO_0001932': '5Overhang',
        'SO_0001933': '3Overhang',
        'SO_0001687': 'RestrictionSite',
        'SO_0000299': 'RecombinaseSite',
        'SO_0001691': 'BluntRestrictionSite',
        'SO_0005850': 'PrimerBindingSite',
        'SO_0001694': '5StickyRestrictionSite',
        'SO_0001690': '3StickyRestrictionSite',
        'SO_0000001': 'UserDefined',
        'SO_0001978': 'Signature',
        }

        def renderSBOL(self, ax, target_component, part_renderers, opts=None):
        """
        Render a design from an SBOL DNA Component

		Parameters
	    ----------
	    ax : matplotlib.axes
	        Axes to draw the design to.

	    target_component : sbol.DNAComponent
	    	An sbol.DNAComponent that contains the design to draw. The design must contain a series of subcomponents
	    	arranged in linear order

	    Returns
	    -------
	    start : float
	    	The x-point in the axis space that drawing begins.

	    end : float
	    	The x-point in the axis space that drawing ends.
		"""
        # class InteractiveDesign:
        #      def __init__(self, dpl_design):
        #          self.parts = dpl_design
        #          print self.parts
        #
        #      def drill_down(self, event):
        #         print 'click'
        #         if event.xdata != None and event.ydata != None:
        #             print(event.xdata, event.ydata)
        #             for part in self.parts:
        #                 if event.xdata > part['start'] and event.xdata < part['end']:
        #                     print part['name']

        def drill_down(event):
            """
            drill_down is the event handler for the plot.  If a user clicks, it will
            drill down a level in the SBOL hierarchy
            """
            if event.xdata != None and event.ydata != None:
                print(event.xdata, event.ydata)
                for i_part, part in enumerate(dpl_design):
                    if event.xdata > part['start'] and event.xdata < part['end']:
                        selected_component = sbol_design[i_part]
                        # plt.close()
                        # fig = plt.figure()
                        # ax = plt.gca()
                        # start, end = self.renderSBOL(ax, selected_component, part_renderers)
                        # ax.set_xlim([start, end])
                        # ax.set_ylim([-18,18])
                        # ax.set_aspect('equal')
                        # ax.set_xticks([])
                        # ax.set_yticks([])
                        # ax.axis('off')
                        width = (part['end'] - part['start'])
                        height = 18
                        # ax.add_patch(Rectangle((event.xdata, -9), width, height, facecolor="grey"))
                        ax.add_patch(Rectangle(( part['start'], -5), 10, 10, facecolor="grey"))
                        fig = plt.gcf()
                        fig.canvas.draw()
                        print part['name']


        def _onMotion(event):
            if event.xdata != None and event.ydata != None: # mouse is inside the axes
                print(event.xdata, event.ydata)
                for i_part, part in enumerate(dpl_design):
                    if event.xdata > part['start'] and event.xdata < part['end']:
                        selected_component = sbol_design[i_part]
                        width = (part['end'] - part['start'])
                        height = 18
                        # ax.add_patch(Rectangle((event.xdata, -9), width, height, facecolor="grey"))
                        ax.add_patch(Rectangle(( part['start'], -5), 10, 10, facecolor="grey"))
                        fig = plt.gcf()
                        fig.canvas.draw()
                        print part['name']



        dpl_design = []  # The SBOL data will be converted to a list of dictionaries used by DNAPlotLib
        sbol_design = []  # Contains a list of DNA components corresponding to the items in dpl_design
        try:
            current_ann = target_component.annotations[0]
        except:
            print "Target DNAComponent does not have any SequenceAnnotations.  Cannot render SBOL."
        END_OF_DESIGN = False
        while not END_OF_DESIGN:
            try:
                subcomponent = current_ann.subcomponent
            except:
                print "DNAComponent does not have subcomponents.  Cannot render SBOL."

            # Translate from SBOL data model to DNAPlotLib dictionary specification for designs
            SO_term = subcomponent.type.split('/')[-1]
            if SO_term in self.SO_terms().keys():
                part = {}
                part['type'] = self.SO_terms()[SO_term]
                part['name'] = subcomponent.name
                part['fwd'] = True
                if opts:
                    part['opts'] = opts
                dpl_design.append(part)
                sbol_design.append(subcomponent)
            # TODO else if SO term of DNAComponent is not recognized, default to a USER_DEFINED sbol symbol
            if len(current_ann.precedes) == 0:
                END_OF_DESIGN = True
            else:
                current_ann = current_ann.precedes[0]  # Iterate to the next downstream annotation
        start, end = self.renderDNA(ax, dpl_design, part_renderers)

        # Display part labels
        # The label configuration specified here should be factored out.  However, the label needs to know the 'start' and 'end' values of each part
        # for part in dpl_design:
        #     label_center = (part['start'] + part['end']) / 2
        #     label_opts = { 'label_size' : 12, 'label_y_offset': -12 }
        #     write_label(ax, part['name'], label_center, label_opts)

        # Connect event handler
        fig = plt.gcf()
        # cid1 = fig.canvas.mpl_connect('button_press_event', drill_down)
        cid2 = fig.canvas.mpl_connect('motion_notify_event', _onMotion)

        # Return type differs from renderDNA
        return dpl_design

