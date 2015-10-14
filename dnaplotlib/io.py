#!/usr/bin/env python
"""
Input/Output functions
"""
#    DNAplotlib
#    Copyright (C) 2014 by
#    Thomas E. Gorochowski <tom@chofski.co.uk>
#    Bryan Der <bder@mit.edu>
#    Emerson Glassey <eglassey@mit.edu>
#    All rights reserved.
#    OSI Open Software License 3.0 (OSL-3.0) license.

import csv
from operator import itemgetter

__author__  = 'Thomas E. Gorochowski <tom@chofski.co.uk>, Voigt Lab, MIT\n\
               Bryan Der <bder@mit.edu>, Voigt Lab, MIT\n\
               Emerson Glassey <eglassey@mit.edu>, Voigt Lab, MIT'
__license__ = 'OSI OSL 3.0'
__version__ = '1.0'

###############################################################################
# Functions for reading designs from standard file formats
###############################################################################

def convert_attrib (attrib):
	if attrib[0] == '(' and attrib[-1] == ')' and len(attrib.split(',')) == 3:
		col_parts = attrib[1:-1].split(',')
		new_col = (float(col_parts[0]), float(col_parts[1]), float(col_parts[2]))
		return new_col
	if attrib[0] == '(' and attrib[-1] == ')' and len(attrib.split(',')) == 4:
		col_parts = attrib[1:-1].split(',')
		new_col = (float(col_parts[0]), float(col_parts[1]), float(col_parts[2]), float(col_parts[3]))
		return new_col
	try:
		# See if a number
	    return float(attrib)
	except ValueError:
	    # Must be a string
	    return attrib

dpl_default_type_map = {'gene': 'CDS', 
                        'promoter': 'Promoter', 
                        'terminator': 'Terminator',
                        'rbs': 'RBS'}

def load_design_from_gff (filename, chrom, type_map=dpl_default_type_map, region=None):
	# Load the GFF data
	gff = []
	data_reader = csv.reader(open(filename, 'rU'), delimiter='\t')
	for row in data_reader:
		if len(row) == 9:
			cur_chrom = row[0]
			part_type = row[2]
			start_bp = int(row[3])
			end_bp = int(row[4])
			part_dir = row[6]
			part_attribs = {}
			split_attribs = row[8].split(';')
			part_name = None
			for attrib in split_attribs:
				key_value = attrib.split('=')
				if len(key_value) == 2:
					if key_value[0] == 'Name':
						part_name = key_value[1]
					else:
						part_attribs[key_value[0]] = convert_attrib(key_value[1])
			if part_name != None and cur_chrom == chrom and part_type in type_map.keys():
				# Check feature start falls in region
				if region != None and (start_bp > region[0] and start_bp < region[1]):
					gff.append([part_name, type_map[part_type], part_dir, start_bp, end_bp, part_attribs])
	# Convert to DNAplotlib design (sort on start position first)
	design = []
	for gff_el in sorted(gff, key=itemgetter(3)):
		new_part = {}
		new_part['name'] = gff_el[0]
		new_part['type'] = gff_el[1]
		if gff_el[2] == '+':
			new_part['fwd'] = True
		else:
			new_part['fwd'] = False
		new_part['start'] = gff_el[3]
		new_part['end'] = gff_el[4]
		new_part['opts'] = gff_el[5]
		design.append(new_part)
	# Return the sorted design
	return design

def load_profile_from_bed (filename, chrom, region):
	region_len = region[1]-region[0]
	profile = [0]*region_len
	data_reader = csv.reader(open(filename, 'rU'), delimiter='\t')
	for row in data_reader:
		if len(row) == 5:
			cur_chrom = row[0]
			cur_start_bp = int(row[1])
			cur_end_bp = int(row[2])
			if cur_start_bp == region[0] and cur_end_bp == region[1]:
				profile[int(row[3])-1] = float(row[4])
	return profile
