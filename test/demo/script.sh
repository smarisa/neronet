#!/bin/bash
# script.sh
nerocli --addnode kosh akosh
nerocli --addnode brute abrute
nerocli --addnode mozart amozart
nerocli --addnode mahler amahler
nerocli --addnode thoth athoth

nerocli --addexp test/experiments/fibonacci
