#!/bin/bash

python -W ignore ../../plot_SBOL_designs.py -params plot_parameters.csv -parts part_information.csv -designs dna_designs.csv -regulation reg_information.csv -output alec_circuit.pdf 
