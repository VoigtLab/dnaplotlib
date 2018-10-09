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
    def __init__(self, parent_module, name, type, orientation='+', frame=None):
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

        frame : (width=float, height=float, origin=float) (default: None)
            Often updated during the rendering process.
        """
        self.parent_module = parent_module
        self.name = name
        self.type = type
        self.orientation = orientation
        self.frame = frame
        self.options = {} # Options to tailor the rendering process


class PartList:
    def __init__(self, position=None, backbone='DNA'):
        """ Constructor to generate a new PartList. Used to hold a list of parts that
        should be rendered as a single unit with a shared backbone. Note that PartList 
        does not hold all parts in a module.

        Parameters
        ----------
        position : [float, float] (default: None)
            [x, y] position of the baseline start for the part. This is often updated
            during the rendering process.

        backbone : string (default: 'DNA')
            Currently, only support DNA rendering. 
            Later could be updated to include RNA backbone (will affect the rendering).

        parts: [Part]

        options: dictionary 
            parts or backbone rendering options currently not supported

        """
        self.position = position
        self.backbone = backbone
        self.parts = [] # List of parts making up the segment
        self.options = {} 

    def add_part(self, part):
        if type(part) != list:
            self.parts.append(part)
        else:
            self.parts += part
        


class Interaction:
    """ Constructor to generate Interaction. 

        Parameters
        ----------
        
        part_start : Part 
            specifies the start part of interaction 

        part_end : Part
            specifies the end part of interaction 

        coordinates : [[float, float]]
            specifies the list of coordinates for the interaction arrow 
            updated during rendering 

        type : string 
            Options inclue: control, degradation, inhibition, process, stimulation

        option: dict
            Options to tailor the rendering process
        """
    def __init__(self, interaction_type, part_start, part_end=None, path=None):
        self.part_start = part_start
        self.part_end = part_end
        self.coordinates = []
        self.type = interaction_type 
        self.options = {}


class Module:
    """ Constructor to generate Module. 

        Parameters
        ----------
        
        design : Constructor 

        name : String
            name of the module

        level : Int [0, 2]
            module hierarchy level / updated during rendering

        frame : (width=float, height=float, origin=float) (default: None)
            Often updated during the rendering process.

        children : [Module]
            list of submodules contained within the module

        part_list: Part_list
            list of parts contained on DNA backbone 

        other_parts: [Part]
            list of parts not contained on DNA backbone 
    """
    def __init__(self, design, name, parent=None):
        self.design = design
        self.name = name
        self.level = 0 
        self.frame = None
        self.children = []
        self.part_list = None # parts on strand
        self.other_parts = [] # parts off strand

    def add_module(self, name):
        child = Module(self.design, name, parent=self)
        self.children.append(child)
        return child

    def add_strand_part(self, part):
        if self.part_list is None:
            self.part_list = PartList()
        self.part_list.add_part(part)

    def add_non_strand_part(self, part):
        if type(part) == list:
            self.other_parts += part
        else: self.other_parts.append(part)


class Design:
    """ Constructor to generate Module. 

        Parameters
        ----------
        name : String
            name of the module

        modules: [Module]
            list of modules contained in the design (only level 0)

        interactions: [Interactions]
            list of interactions within design
    """
    def __init__(self, name):
        self.name = name
        self.modules = []
        self.interactions = []

    def rename_design(self, name):
        self.name = name

    def add_module(self, module):
        if type(module) != list:
            self.modules.append(module)
        else:
            self.modules += module

    def add_interaction(self, interaction):
        if type(interaction) != list:
            self.interactions.append(interaction)
        else:
            self.interactions += interaction

    def __print_part_list(self, part_list, indent=''):
        if part_list == None or len(part_list.parts) == 0: return
        names = []
        for part in part_list.parts:
            names.append(part.name)
        print(indent + '  Parts: ' + ','.join(names))

    def __print_other_parts(self, other_part_list, indent=''):
    	if len(other_part_list) == 0: return
    	names = []
    	for op in other_part_list:
            names.append(op.name)
        print(indent + '  Other parts: ' + ','.join(names))

    def __print_module_tree(self, starting_module, indent=''):
        # Recursive method to print tree details
        print(indent + 'Module:', starting_module.name)
        self.__print_part_list(starting_module.part_list, indent)
        self.__print_other_parts(starting_module.other_parts, indent)

        if len(starting_module.children) > 0:
            for node in starting_module.children:
                self.__print_module_tree(node, indent + '  ')
            
    def print_design(self):
        # Generate a human-readable version of the data type
        print('Design:', self.name)
        for module in self.modules:
            self.__print_module_tree(module, indent='  ')
        for interaction in self.interactions:
            if interaction.part_end != None:
                print('Interaction from part:', interaction.part_start.name, 
                  'to part:', interaction.part_end.name,
                  'of type:', interaction.type)
            else:
                print('Interaction from part:', interaction.part_start.name, 
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
    module1a.add_strand_part( part_1aCDS )
    module1a.add_strand_part( Part(module1a, '1aT','Promoter') )
    module1b = module1.add_module('module1b')
    module1b.add_strand_part( Part(module1b, '1b','Promoter') )
    module1c = module1.add_module('module1c')
    part_1cCDS = Part(module1a, '1c','Promoter')
    module1c.add_strand_part( part_1cCDS )
    # Create DNA module 2
    module2 = Module(design, 'module2')
    part_2CDS = Part(module2, '2','Promoter')
    module2.add_strand_part( part_2CDS )
    # Attach the different DNA segments to design
    design.add_module(module1)
    design.add_module(module2)

    # Add some other parts (e.g. molecules like a repressor)
    other_part_1Rep = Part(module2, 'R1','Unspecified')
    module2.add_non_strand_part( other_part_1Rep )

    # Add some basic interactions
    interaction1 = Interaction('inhibition', part_1cCDS, part_1aCDS)
    interaction2 = Interaction('process', part_1cCDS, other_part_1Rep)
    interaction3 = Interaction('stimulation', other_part_1Rep, part_2CDS)
    design.add_interaction(interaction1)
    design.add_interaction(interaction2)
    design.add_interaction(interaction3)
    return design

# for rendering degradation
def create_test_design1_1 ():
    design = Design('design1_1')
    module = Module(design, module)
    part1_p = Part(module, '1p', 'Promoter')
    module.add_part(part1_p)
    design.add_module(module)

    interaction1 = Interaction()


def create_test_design2 ():
    # You first create a design and need to give it a name   
    design = Design('design2')

    # Create DNA module 1 
    module1 = Module(design, 'module1')
    part_1_pro = Part(module1, 'p1a','Promoter')
    part_1_res = Part(module1, 'p1r','RibosomeEntrySite') 
    part_1_cds = Part(module1, 'p1c','CDS')
    part_1_ter = Part(module1, 'p1t','Terminator')
    module1.add_strand_part( [part_1_pro, part_1_res, part_1_cds, part_1_ter] )
    
    # Create DNA module 2
    module2 = Module(design, 'module2')
    part_2_pro = Part(module2, 'p2p','Promoter')
    part_2_cds = Part(module2, 'p2c','CDS')
    part_2_ter = Part(module2, 'p2t','Terminator')
    module2.add_strand_part( [part_2_pro, part_2_cds, part_2_ter])

    # module 3
    module3 = Module(design, 'module3')
    part_3_pro = Part(module3, 'p3p', 'Promoter')
    part_3_ins = Part(module3, 'p3i', 'Insulator')
    part_3_ter = Part(module3, 'p3t', 'Terminator')
    module3.add_strand_part( [part_3_pro, part_3_ins, part_3_ter] )

    # module 4
    module4 = Module(design, 'module4')
    part_4_pro = Part(module4, 'p4p', 'Promoter')
    part_4_ori = Part(module4, 'p4o', 'OriginOfReplication')
    part_4_ter = Part(module4, 'p4t', 'Terminator')
    module4.add_strand_part( [part_4_pro, part_4_ori, part_4_ter] )

    # module 5
    module5 = Module(design, 'module5')
    part_5_pro = Part(module5, 'p5p', 'Promoter')
    part_5_ter = Part(module5, 'p5t', 'Terminator')
    module5.add_strand_part( [part_5_pro, part_5_ter] )

    # module 6
    module6 = Module(design, 'module6')
    part_6_pro = Part(module6, 'p6a','Promoter')
    part_6_apt = Part(module6, 'p6apt', 'Aptamer')
    part_6_res = Part(module6, 'p6r','RibosomeEntrySite') 
    part_6_ter = Part(module1, 'p6t','Terminator')
    module6.add_strand_part( [part_6_pro, part_6_apt, part_6_res, part_6_ter] )

    # module 7
    module7 = Module(design, 'module7')
    part_7_pro = Part(module7, 'p7p', 'Promoter')
    part_7_res = Part(module7, 'p7r', 'RibosomeEntrySite')
    part_7_ter = Part(module7, 'p7t', 'Terminator')
    module7.add_strand_part( [part_7_pro, part_7_res, part_7_ter] )

    # module 8
    module8 = Module(design, 'module8')
    part_8_pro = Part(module8, 'p8p', 'Promoter')
    part_8_res = Part(module8, 'p8r', 'RibosomeEntrySite')
    part_8_ter = Part(module8, 'p8t', 'Terminator')
    module8.add_strand_part( [part_8_pro, part_8_res, part_8_ter] )
    
    # Attach the different DNA segments to design
    design.add_module( [module1, module2, module3, module4, module5, module6, module7, module8] )

    # Add some basic interactions
    interaction1 = Interaction('control', part_1_cds, part_4_pro)
    int2 = Interaction('degradation', part_1_pro, part_3_pro)
    int3 = Interaction('process', part_2_cds, part_4_ori)
    int4 = Interaction('inhibition', part_5_pro, part_2_pro)
    int5 = Interaction('stimulation', part_7_pro, part_8_res)
    design.add_interaction( [interaction1, int2, int3, int4, int5] )
    return design

# hierarchical submodule rendering
def create_test_design3 ():
    # You first create a design and need to give it a name   
    design = Design('design3')

    # Create DNA module 1 
    module1 = Module(design, 'module1')
    module1a = module1.add_module('module1a')
    module1a_1 = module1a.add_module('module1a_1')
    part1a_1_p = Part(module1a_1, '1a_1_p', 'Promoter')
    module1a_1.add_strand_part( part1a_1_p )
    module1a_1.add_strand_part( Part(module1a_1, '1a_1_c', 'CDS'))
    module1a_1.add_strand_part( Part(module1a_1, '1a_1_t', 'Terminator'))

    module2 = Module(design, 'module2')
    part_2_p = Part(module2, '2p', 'Promoter')
    module2.add_strand_part(part_2_p)

    design.add_module( [module1, module2] )

    interaction = Interaction('inhibition', part1a_1_p, part_2_p)
    design.add_interaction(interaction)

    return design

# hierarchical submodule rendering
def create_test_design3_1 ():
    # You first create a design and need to give it a name   
    design = Design('design3')

    # Create DNA module 1 
    module1 = Module(design, 'module1')
    module1a = module1.add_module('module1a')
    module1a_1 = module1a.add_module('module1a_1')
    part1a_1_p = Part(module1a, '1a_1_p', 'Promoter')
    part1a_1_c = Part(module1a, '1a_1_c', 'CDS')
    module1a_1.add_strand_part( [part1a_1_p, part1a_1_c ])
    module1a_1.add_strand_part( Part(module1a_1, '1a_1_t', 'Terminator'))

    module1b = module1.add_module('module1b')
    part1b_p = Part(module1b, '1b_p', 'Promoter')
    part1b_i = Part(module1b, '1b_i', 'Insulator')
    part1b_o = Part(module1b, '1b_o', 'OriginOfReplication')
    module1b.add_strand_part([part1b_p, part1b_i, part1b_o])

    design.add_module( module1 )

    return design

# hierarchical submodule rendering
def create_test_design3_2 ():
    # You first create a design and need to give it a name   
    design = Design('design3')

    # Create DNA module 1 
    module1 = Module(design, 'module1')
    module1a = module1.add_module('module1a')
    part1a_1_p = Part(module1, 'promoter_1a', 'Promoter')
    part1a_1_c = Part(module1, 'cds_1a', 'CDS')
    module1a.add_strand_part( [part1a_1_p, part1a_1_c ])
    #module1a_1.add_part( Part(module1a_1, '1a_1_t', 'Terminator'))

    module1b = module1.add_module('module1b')
    part1b_p = Part(module1b, 'promoter_1b', 'Promoter')
    part1b_i = Part(module1b, 'insulator_1b', 'Insulator')
    part1b_o = Part(module1b, 'ori_1b', 'OriginOfReplication')
    module1b.add_strand_part([part1b_p, part1b_i, part1b_o])

    design.add_module( module1 )

    return design

# hierarchical submodule rendering
def create_test_design3_3 ():
    # You first create a design and need to give it a name   
    design = Design('design3')

    # Create DNA module 1 
    module1 = Module(design, 'module1')
    module1a = module1.add_module('module1a')
    module1a_1 = module1a.add_module('module1a_1')
    part1a_1_p = Part(module1a, '1a_1_p', 'Promoter')
    part1a_1_c = Part(module1a, '1a_1_c', 'CDS')
    module1a_1.add_strand_part( [part1a_1_p, part1a_1_c ])
    module1a_1.add_strand_part( Part(module1a_1, '1a_1_t', 'Terminator'))

    module1b = module1.add_module('module1b')
    module1b.add_strand_part(Part(module1b, '1b_p', 'Promoter'))

    module1c = module1.add_module('module1c')
    part1c_p = Part(module1c, '1c_p', 'Promoter')
    part1c_i = Part(module1c, '1c_i', 'Insulator')
    part1c_o = Part(module1c, '1c_o', 'OriginOfReplication')
    module1c.add_strand_part([part1c_p, part1c_i, part1c_o])

    design.add_module( module1 )

    return design

# other part rendering
def create_test_design4 ():
    # You first create a design and need to give it a name   
    design = Design('design4')

    # Create DNA module 1 
    module1 = Module(design, 'module1')
    part_1_pro = Part(module1, '1a','Promoter')
    part_1_res1 = Part(module1, '1r1','RibosomeEntrySite') 
    part_1_res2 = Part(module1, '1r2','RibosomeEntrySite') 
    part_1_res3 = Part(module1, '1r3','RibosomeEntrySite') 
    part_1_res4 = Part(module1, '1r4','RibosomeEntrySite') 
    part_1_res5 = Part(module1, '1r5','RibosomeEntrySite') 
    part_1_cds1 = Part(module1, '1c1','CDS')
    part_1_cds2 = Part(module1, '1c2','CDS')
    part_1_cds3 = Part(module1, '1c3','CDS')
    part_1_cds4 = Part(module1, '1c4','CDS')
    part_1_ter = Part(module1, '1t','Terminator')
    # Add some other parts (e.g. molecules like a repressor)
    other_part_1Rep1 = Part(module1, 'R1','Unspecified')
    other_part_1Rep2 = Part(module1, 'R2','Macromolecule')
    other_part_1RNA = Part(module1, 'R3', 'RNA')
    module1.add_non_strand_part( [other_part_1Rep1, other_part_1Rep2, other_part_1RNA])
    module1.add_strand_part( [part_1_pro, part_1_res1, part_1_cds1, part_1_res2, part_1_res3, 
        part_1_cds2, part_1_res4, part_1_cds3, part_1_res5, part_1_cds4, part_1_ter] )
    
    # Create DNA module 2
    module2 = Module(design, 'module2')
    part_2_pro = Part(module2, '2p','Promoter')
    part_2_cds = Part(module2, '2c','CDS')
    part_2_ter = Part(module2, '2t','Terminator')
    module2.add_strand_part( [part_2_pro, part_2_cds, part_2_ter])

    # module 3
    module3 = Module(design, 'module3')
    part_3_pro = Part(module3, '3p', 'Promoter')
    part_3_ins = Part(module3, '3i', 'Insulator')
    part_3_ter = Part(module3, '3t', 'Terminator')
    module3.add_strand_part( [part_3_pro, part_3_ins, part_3_ter] )

    # module 4
    module4 = Module(design, 'module4')
    part_4_pro = Part(module4, '4p', 'Promoter')
    part_4_ori = Part(module4, '4o', 'OriginOfReplication')
    part_4_ter = Part(module4, '4t', 'Terminator')
    module4.add_strand_part( [part_4_pro, part_4_ori, part_4_ter] )
    
    # Attach the different DNA segments to design
    design.add_module( [module1, module2, module3, module4] )

    # Add some basic interactions
    interaction1 = Interaction('control', part_1_cds1, part_4_pro)
    int2 = Interaction('degradation', part_1_pro, part_3_pro)
    int3 = Interaction('process', part_2_cds, part_4_ori)
    int4 = Interaction('inhibition', part_2_pro, part_3_ins)
    design.add_interaction( [interaction1, int2, int3, int4] )
    return design

    
def create_test_design5():
    # You first create a design and need to give it a name   
    design = Design('design5')

    # Create DNA module 1 
    module1 = Module(design, 'module1')
    p1 = Part(module1, 'p1p', 'Promoter')
    part_1_cds_1 = Part(module1, 'p1c', 'CDS')
    t1 = Part(module1, 'p1t', 'Terminator')
    module1.add_strand_part( [p1, part_1_cds_1, t1])
    aptamer1 = Part(module1, 'apt1', 'Aptamer')
    module1.add_non_strand_part( [aptamer1] )

    # Create module 2 containing only other part 
    module2 = Module(design, 'module2')
    other_part_2 = Part(module2, 'p','Macromolecule')
    module2.add_strand_part(other_part_2)

    # Create module 3 containing only other part 
    module3 = Module(design, 'module3')
    other_part_3 = Part(module3, 'rna3','RNA')
    module3.add_strand_part(other_part_3)

    # module 6
    module6 = Module(design, 'module6')
    part_6_pro = Part(module6, 'p6a','Promoter')
    part_6_res = Part(module6, 'p6r','RibosomeEntrySite') 
    part_6_cds = Part(module6, 'p6c', 'CDS')
    part_6_ter = Part(module6, 'p6t','Terminator')
    other_part_6 = Part(module6, 'm6', 'Macromolecule')
    module6.add_strand_part([other_part_6])
    module6.add_strand_part( [part_6_pro, part_6_res, part_6_cds, part_6_ter] )

    # module 7
    module7 = Module(design, 'module7')
    part_7_pro = Part(module7, 'p7p', 'Promoter')
    part_7_c1 = Part(module7, 'p7c1', 'CDS')
    part_7_c2 = Part(module7, 'p7c2', 'CDS')
    part_7_ter = Part(module7, 'p7t', 'Terminator')
    module7.add_strand_part( [part_7_pro, part_7_c1, part_7_c2, part_7_ter] )

    # module 8
    module8 = Module(design, 'module8')
    part_8_pro = Part(module8, 'p8p', 'Promoter')
    part_8_cds_1 = Part(module8, 'p8c1', 'CDS')
    part_8_ori = Part(module8, 'p8o', 'OriginOfReplication')
    part_8_ter = Part(module8, 'p8t', 'Terminator')
    other_part_8 = Part(module8, 'rna8','RNA')
    module8.add_non_strand_part(other_part_8)
    module8.add_strand_part( [part_8_pro, part_8_cds_1, part_8_ori, part_8_ter] )

    design.add_interaction( [Interaction('inhibition', aptamer1, other_part_2),
        Interaction('inhibition', other_part_6, part_7_pro),
        Interaction('control', part_7_c2, part_8_pro),
        Interaction('stimulation', other_part_8, p1)])

    design.add_module([module1, module6, module7, module8, module2])

    return design

def create_test_design6 ():
    design = Design('design6')
    module1 = Module(design, 'module1')
    part_1_pro = Part(module1, 'p1p', 'Promoter')
    module1.add_strand_part(part_1_pro)

    design.add_interaction([Interaction('degradation', part_1_pro)])
    design.add_module([module1])

    return design

def create_test_design6_1 ():
    design = Design('design6_1')
    module1 = Module(design, 'module1')
    module1a = module1.add_module('module1a')
    module1b = module1.add_module('module1b')
    module2 = Module(design, 'module2')

    part_1a_p = Part(module1a, 'p1ap', 'Promoter')
    part_1a_t = Part(module1a, 'p1at', 'Terminator')
    part_1b_o = Part(module1b, 'p1bo', 'OriginOfReplication')
    part_1b_i = Part(module1b, 'p1bi', 'Insulator')
    module1a.add_strand_part([part_1a_p, part_1a_t])
    module1b.add_strand_part([part_1b_o, part_1b_i])

    part_2_p = Part(module2, 'p2p', 'Promoter')
    part_2_a = Part(module2, 'p2a', 'Aptamer')
    part_2_r = Part(module2, 'p2r', 'RibosomeEntrySite')
    module2.add_strand_part([part_2_p, part_2_a, part_2_r])

    other_part_2Mac = Part(module2, 'M1', 'Macromolecule')
    module2.add_non_strand_part( other_part_2Mac )

    design.add_module([module1, module2])
    interaction1 = Interaction('degradation', part_1b_o)
    int2 = Interaction('inhibition', other_part_2Mac, part_2_p)
    design.add_interaction( [interaction1, int2] )
    return design

def create_test_design6_2 ():
    design = Design('design6_1')
    module1 = Module(design, 'module1')
    module1a = module1.add_module('module1a')
    module1b = module1.add_module('module1b')
    module2 = Module(design, 'module2')

    part_1a_p = Part(module1a, 'p1ap', 'Promoter')
    part_1a_t = Part(module1a, 'p1at', 'Terminator')
    part_1b_o = Part(module1b, 'p1bo', 'OriginOfReplication')
    part_1b_i = Part(module1b, 'p1bi', 'Insulator')
    module1a.add_strand_part([part_1a_p, part_1a_t])
    module1b.add_strand_part([part_1b_o, part_1b_i])

    part_2_p = Part(module2, 'p2p', 'Promoter')
    part_2_a = Part(module2, 'p2a', 'Aptamer')
    part_2_r = Part(module2, 'p2r', 'RibosomeEntrySite')
    module2.add_strand_part([part_2_p, part_2_a, part_2_r])

    other_part_1aRep = Part(module1a, 'R1','Unspecified')
    other_part_2Mac = Part(module2, 'M1', 'Macromolecule')
    module1a.add_non_strand_part( other_part_1aRep )
    module2.add_non_strand_part( other_part_2Mac )

    design.add_module([module1, module2])
    interaction1 = Interaction('control', part_1a_p, part_1b_o)
    int2 = Interaction('degradation', other_part_2Mac)
    int3 = Interaction('process', part_2_r, part_1b_i)
    design.add_interaction([interaction1, int2, int3] )
    return design

def create_test_design7():
    # create design 
    design = Design('design7')

    # create modules & parts
    module1 = Module(design, 'module1')
    part_1_p = Part(module1, 'promoter1', 'Promoter')
    part_1_c = Part(module1, 'fnr_gene', 'CDS')
    part_1_t = Part(module1, 'terminator', 'Terminator')
    other_part_p = Part(module1, 'fnr', 'Macromolecule')
    
    module1.add_strand_part([part_1_p, part_1_c, part_1_t])   
    module1.add_non_strand_part(other_part_p) # non-dna onto other parts!
    design.add_module(module1)

    # create interaction
    design.add_interaction(Interaction('inhibition', other_part_p, part_1_p))

    return design

def create_test_design7_1():
    design = Design('design7')
    module1 = Module(design, 'module1')
    part_1_p = Part(module1, 'promoter', 'Promoter')
    part_1_c = Part(module1, 'p1c', 'CDS')
    part_1_o = Part(module1, 'p1o', 'OriginOfReplication')
    part_1_i = Part(module1, 'p1i', 'Insulator')
    part_1_t = Part(module1, 'p1t', 'Terminator')
    module1.add_strand_part([part_1_p, part_1_c, part_1_o, part_1_i, part_1_t])
    other_part_p = Part(module1, 'M1', 'Macromolecule')
    module1.add_non_strand_part(other_part_p)
    design.add_module(module1)

    design.add_interaction(Interaction('inhibition', other_part_p, part_1_p))

    return design

def create_test_design8():
    design = Design('design8')
    module1 = Module(design, 'module1')
    module1a = module1.add_module('module1a')
    module1b = module1.add_module('module1b')

    part1p = Part(module1a, 'p1a', 'Promoter')
    part1c = Part(module1a, 'p1c', 'CDS')
    part1t = Part(module1a, 'p1t', 'Terminator')
    mop_1 = Part(module1a, 'mRNA1', 'RNA')
    module1a.add_strand_part([part1p, part1c, part1t])
    module1a.add_non_strand_part(op_1)

    part2p = Part(module1b, 'p2a', 'Promoter')
    part2c = Part(module1b, 'p2c', 'CDS')
    part2t = Part(module1b, 'p2t', 'Terminator')
    op_2 = Part(module1a, 'mRNA2', 'RNA')
    module1b.add_strand_part([part2p, part2c, part2t])
    module1b.add_non_strand_part(op_2)

    rep1 = Part(module1, 'r1', 'Macromolecule')
    rep2 = Part(module1, 'r2', 'Macromolecule')
    module1.add_non_strand_part([rep1, rep2])

    design.add_interaction([
        Interaction('process', op_1, rep1),
        Interaction('inhibition', part1c, part2p),
        Interaction('process', op_2, rep2),
        Interaction('inhibition', part2c, part1p)
    ])


    design.add_module(module1)
    return design

