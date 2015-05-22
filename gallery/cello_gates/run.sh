#!/bin/bash

python -W ignore ../../plot_SBOL_designs.py -params plot_parameters.csv -parts part_information.csv -designs dna_designs_riboj.csv -output cello_gates_riboj.pdf -regulation reg_information.csv
python -W ignore ../../plot_SBOL_designs.py -params plot_parameters.csv -parts part_information.csv -designs dna_designs_gen1.csv -output cello_gates_gen1.pdf -regulation reg_information.csv
python -W ignore ../../plot_SBOL_designs.py -params plot_parameters.csv -parts part_information.csv -designs dna_designs_gen2.csv -output cello_gates_gen2.pdf -regulation reg_information.csv
python -W ignore ../../plot_SBOL_designs.py -params plot_parameters.csv -parts part_information.csv -designs dna_designs.csv -output cello_gates.pdf -regulation reg_information.csv

