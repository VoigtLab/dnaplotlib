#!/usr/bin/env python
"""
New DNAplotlib data type for designs (extendable for hierachy)
"""

__author__  = 'Thomas E. Gorochowski <tom@chofski.co.uk>'
__license__ = 'MIT'
__version__ = '2.0'

###############################################################################
# New Data Type
###############################################################################

class Node:
    def __init__(self, design, parent, name):
        self.design = design
        self.parent = parent
        self.name = name
        self.children = []
        self.part_list = []

    def add_child(self, name):
        child = Node(self.design, self, name)
        self.children.append(child)
        return child

class Design:
    def __init__(self, name, interactions=None):
        self.name = name
        self.root = []
        self.interactions = interactions
        self.other_parts = []

    def __print_part_list__(self, part_list, indent=''):
        names = []
        for part in part_list:
            names.append(part.name)
        print(indent+'  Parts: ' + ','.join(names))

    def __print_node_tree__(self, starting_node, indent=''):
        print(indent + 'Node:', starting_node.name)
        if len(starting_node.children) > 0:
            for node in starting_node.children:
                self.__print_node_tree__(node, indent+'  ')
        else:
            self.__print_part_list__(starting_node.part_list, indent)

    def print_design(self):
        print('Design:', self.name)
        for node in self.root:
            self.__print_node_tree__(node, indent='  ')

class Part:
    def __init__ (self, parent_node, name, type, orientation='+', start_position=None, end_position=None):
        self.parent_node = parent_node
        self.name = name
        self.type = type
        self.orientation = orientation
        self.start_position = start_position
        self.end_position = end_position

###############################################################################
# Testing
###############################################################################

def create_test_design ():
    design = Design('design1')
    # Create DNA module 1 (containing sub-modules)
    module1 = Node(design, None, 'module1')
    module1a = module1.add_child('module1a')
    module1a.part_list.append( Part(module1a, '1a','CDS') )
    module1b = module1.add_child('module1b')
    module1b.part_list.append( Part(module1b, '1b','CDS') )
    module1c = module1.add_child('module1c')
    module1c.part_list.append( Part(module1c, '1c','CDS') )
    # Create DNA module 2
    module2 = Node(design, None, 'module2')
    module2.part_list.append( Part(module2, '2','CDS') )
    # Attach the different DNA segments to design
    design.root.append(module1)
    design.root.append(module2)
    return design

# Let's try it out!
design = create_test_design()
design.print_design()
































