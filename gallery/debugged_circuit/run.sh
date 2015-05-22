#!/bin/bash

#python -W ignore ../../plot_SBOL_designs.py -params plot_parameters.csv -parts part_information.csv -designs dna_designs.csv -regulation reg_information.csv -output 0x58v50.pdf 

python -W ignore ../../plot_SBOL_designs.py -params plot_parameters.csv -parts part_information.csv -designs dna_designs.csv -output 0x58v50.pdf 
python -W ignore ../../plot_SBOL_designs.py -params plot_parameters.csv -parts part_information.csv -designs dna_designs_fix.csv -output 0x58v50_fix.pdf 
