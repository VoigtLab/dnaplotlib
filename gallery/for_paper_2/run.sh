#!/bin/bash

python -W ignore ../../plot_SBOL_designs.py -params plot_parameters.csv -parts part_information.csv -designs dna_designs.csv -regulation reg_information.csv -output figure_plot_parts.pdf

python -W ignore ../../plot_SBOL_designs.py -params plot_parameters_cello.csv -parts part_information_cello.csv -designs dna_designs_cello.csv -regulation reg_information_cello.csv -output figure_plot_cello.pdf

python trace_plot.py
