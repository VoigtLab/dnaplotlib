"""
New DNAplotlib data type for designs (extendable for hierachy)
"""

__author__  = 'Thomas E. Gorochowski <tom@chofski.co.uk>'
__license__ = 'MIT'
__version__ = '2.0'

###############################################################################
# New Data Type
###############################################################################

class Part:
    def __init__(self, parent_node, name, type, orientation='+', 
                  start_position=None, end_position=None):
        self.parent_node = parent_node
        self.name = name
        self.type = type
        # Orientation of the part, either '+' or '-' (for reverse)
        self.orientation = orientation
        # Relative positions within the module
        self.start_position = start_position
        self.end_position = end_position
        # Options to tailor the rendering process
        self.options = {}

class PartList:
    def __init__(self, type='DNA'):
        # Type of backbone (DNA or RNA)
        self.type = type
        # List of parts making up the segment
        self.parts = []
        # Position and extent of the part list
        self.position = (0,0)
        self.extent = (0,0)
        # Options to be used when rendering backbone
        self.options = {}

    def add_part(self, part):
        self.parts.append(part)

class Module:
    def __init__(self, design, parent, name):
        self.design = design
        self.parent = parent
        self.name = name
        self.children = []
        self.part_list = PartList()

    def add_module(self, name):
        child = Module(self.design, self, name)
        self.children.append(child)
        return child

    def add_part(self, part):
        if len(self.children) > 0:
            print('Warning: Module already has children, part list is ignored:', self.name)
        self.part_list.add_part(part)

class Design:
    def __init__(self, name):
        self.name = name
        self.modules = []
        self.interactions = []
        self.other_parts = []

    def add_module(self, module):
        self.modules.append(module)

    def __print_part_list__(self, part_list, indent=''):
        names = []
        for part in part_list.parts:
            names.append(part.name)
        print(indent + '  Parts: ' + ','.join(names))

    def __print_module_tree__(self, starting_module, indent=''):
        # Recursive method to print tree details
        print(indent + 'Module:', starting_module.name)
        if len(starting_module.children) > 0:
            for node in starting_module.children:
                self.__print_module_tree__(node, indent + '  ')
        else:
            self.__print_part_list__(starting_module.part_list, indent)

    def print_design(self):
        # Generate a human-readable version of the data type
        print('Design:', self.name)
        for module in self.modules:
            self.__print_module_tree__(module, indent='  ')

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
































