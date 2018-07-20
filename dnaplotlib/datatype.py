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
    def __init__(self, parent_module, name, type, orientation='+', position=None):
        """ Constructor to generate a new Part.

        Parameters
        ----------
        parent_module : Module
            Module that this part is a member of.

        name : string
            Name of part.

        type : string
            Type of part. 

        orientation : string (default: '+')
            Orientation of the part (either '+' or '-')

        position : [float, float] (default: None)
            [x, y] position of the baseline start for the part. This is often updated
            during the rendering process.
        """
        self.parent_module = parent_module
        self.name = name
        self.type = type
        self.orientation = orientation
        self.position = position
        # Bounding box of the part lower left to upper right coordinates.
        self.extent = [[0,0], [0,0]]
        # Options to tailor the rendering process
        self.options = {}


class PartList:
    def __init__(self, position=None, backbone='DNA'):
        """ Constructor to generate a new PartList. Used to hold a list of parts that
        should be rendered as a single unit with a shared backbone.

        Parameters
        ----------
        position : [float, float] (default: None)
            [x, y] position of the baseline start for the part. This is often updated
            during the rendering process.

        backbone : string (default: 'DNA')
            The backbone type, either DNA or RNA (will affect the rendering).
        """
        # Type of backbone (DNA or RNA, will affect rendering)
        self.position = position
        self.backbone = backbone
        # List of parts making up the segment
        self.parts = []
        # Bounding box of the part lower left to upper right coordinates.
        self.extent = [[0,0], [0,0]]
        # Options to be used when rendering backbone
        self.options = {}

    def add_part(self, part):
        """ Add part/parts to the part list.

        Parameters
        ----------
        part : Part
            Part to appended to the end of the part list.
        """
        if type(part) != list:
            self.parts.append(part)
        else:
            self.parts += part
        


class Interaction:
    def __init__(self, part_start, part_end, type, path=None):
        self.part_start = part_start
        self.part_end = part_end
        self.type = type # Options inclue: link, stimulation, repression, production
        self.path = path
        # Options to tailor the rendering process
        self.options = {}


class Module:
    def __init__(self, design, name, parent=None):
        self.design = design
        self.parent = parent
        self.name = name
        self.children = []
        self.part_list = None
        self.other_parts = []

    def add_module(self, name):
        child = Module(self.design, name, parent=self)
        self.children.append(child)
        return child

    def add_part(self, part):
        if self.part_list == None:
            self.part_list = PartList()
        self.part_list.add_part(part)

    def add_other_part(self, part):
        self.part_list.add_part(part)


class Design:
    def __init__(self, name):
        self.name = name
        self.modules = []
        self.interactions = []

    def add_module(self, module):
        self.modules.append(module)

    def add_interaction(self, interaction):
        self.interactions.append(interaction)

    def __print_part_list(self, part_list, indent=''):
        names = []
        for part in part_list.parts:
            names.append(part.name)
        print(indent + '  Parts: ' + ','.join(names))

    def __print_module_tree(self, starting_module, indent=''):
        # Recursive method to print tree details
        print(indent + 'Module:', starting_module.name)
        if len(starting_module.children) > 0:
            for node in starting_module.children:
                self.__print_module_tree(node, indent + '  ')
        else:
            self.__print_part_list(starting_module.part_list, indent)

    def print_design(self):
        # Generate a human-readable version of the data type
        print('Design:', self.name)
        for module in self.modules:
            self.__print_module_tree(module, indent='  ')
        for interaction in self.interactions:
            print('Interaction from part:', interaction.part_start.name, 
                  'to part:', interaction.part_end.name,
                  'of type:', interaction.type)

###############################################################################
# Testing
###############################################################################

# The basic data type at the moment works by having a Design object that holds 
# lists of the modules, interactions, and other parts making up the design. At
# the moment only the modules list is used. The other aspects will be added 
# later. The add_module method is called with a Module object to add and it will
# be appended to the list. There are also a couple private functions that the
# print_design method uses to print out the tree making up the design, drilling
# down into each module. An example of how to generate a design is shown below.
# The key detail in the datatype is that Modules can have Modules added to them 

def create_test_design ():
    # You first create a design and need to give it a name   
    design = Design('design1')
    # Create DNA module 1 (containing sub-modules)
    module1 = Module(design, 'module1')
    module1a = module1.add_module('module1a')
    part_1aCDS = Part(module1a, '1a','Promoter')
    module1a.add_part( part_1aCDS )
    module1a.add_part( Part(module1a, '1aT','Promoter') )
    module1b = module1.add_module('module1b')
    module1b.add_part( Part(module1b, '1b','Promoter') )
    module1c = module1.add_module('module1c')
    part_1cCDS = Part(module1a, '1c','Promoter')
    module1c.add_part( part_1cCDS )
    # Create DNA module 2
    module2 = Module(design, 'module2')
    part_2CDS = Part(module2, '2','Promoter')
    module2.add_part( part_2CDS )
    # Attach the different DNA segments to design
    design.add_module(module1)
    design.add_module(module2)

    # Add some other parts (e.g. molecules like a repressor)
    other_part_1Rep = Part(module2, 'R1','Promoter')
    module2.add_other_part( other_part_1Rep )

    # Add some basic interactions
    interaction1 = Interaction(part_1cCDS, part_1aCDS, 'repression')
    interaction2 = Interaction(part_1cCDS, other_part_1Rep, 'production')
    interaction3 = Interaction(other_part_1Rep, part_2CDS, 'stimulation')
    design.add_interaction(interaction1)
    design.add_interaction(interaction2)
    design.add_interaction(interaction3)
    return design

def create_test_design2 ():
    # You first create a design and need to give it a name   
    design = Design('design2')

    # Create DNA module 1 
    module1 = Module(design, 'module1')
    part_1_pro = Part(module1, '1a','Promoter')
    part_1_res = Part(module1, '1r','RibosomeEntrySite') 
    part_1_cds = Part(module1, '1c','CDS')
    part_1_ter = Part(module1, '1t','Terminator')
    module1.add_part( [part_1_pro, part_1_res, part_1_cds, part_1_ter] )
    
    # Create DNA module 2
    module2 = Module(design, 'module2')
    part_2_pro = Part(module2, '2p','Promoter')
    part_2_cds = Part(module2, '2c','CDS')
    part_2_ter = Part(module2, '2t','Terminator')
    module2.add_part( [part_2_pro, part_2_cds, part_2_ter] )
    
    # Attach the different DNA segments to design
    design.add_module(module1)
    design.add_module(module2)

    # Add some basic interactions
    interaction1 = Interaction(part_1_cds, part_2_pro, 'repression')
    design.add_interaction(interaction1)
    return design

# Let's try it out!
design = create_test_design2()
design.print_design()









