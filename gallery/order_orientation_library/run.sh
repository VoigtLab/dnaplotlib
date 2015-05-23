#!/bin/bash

SCRIPT_PATH=../../apps

python -W ignore $SCRIPT_PATH/plot_SBOL_designs.py -params 0x40_plot_parameters.csv -parts 0x40_part_information.csv -designs 0x40_dna_designs.csv -regulation 0x40_reg_information.csv -output order_orientation_library.pdf
python -W ignore $SCRIPT_PATH/plot_SBOL_designs.py -params 0x40_plot_parameters.csv -parts 0x40_part_information.csv -designs 0x40_dna_designs.csv -regulation 0x40_reg_information.csv -output order_orientation_library.png
