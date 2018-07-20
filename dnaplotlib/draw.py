"""
draw dataype
: script for bringing datatype and render func together 
"""

import datatype as dt 
import render as rd 
import matplotlib.pyplot as plt, numpy as np 

# try render the test design 
design = dt.create_test_design2()
design.print_design()

# render them through plot 
