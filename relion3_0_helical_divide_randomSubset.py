#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
v0.1
Created on April 6, 2023

Helical refinement need to be divided by filaments or by tomograms otherwise the resolution will be inflated
due to overlapping of particles. Helical refinement can take care of that if you have HelicalTubeID but by
conversion, you might not have the rlnHelicalTubeID.

This script will change the rlnRandomSubset based on rlnMicrographName so that every particles with same 
rlnMicrographName will be in the same Subset.

Only work with Relion 3.0 straight out of Warp.
Install starfile
$pip install starfile
"""

import numpy as np
import starfile
import argparse

from eulerangles import euler2matrix

if __name__=='__main__':
	print("Only work with Relion 3.0!!!")
	parser = argparse.ArgumentParser(description='Add rlnRandomSubset for helical refinement')
	parser.add_argument('--i', help='Input star file',required=True)
	parser.add_argument('--o', help='Output star file',required=True)
	
	args = parser.parse_args()
		
	# Loading Relion star file
	df = starfile.read(args.i)
		
	# added by v0.1
	microList = df['rlnMicrographName'].unique()
	
	subset = 1;
	
	# Add empty column
	df['rlnRandomSubset'] = 0
	
	for micro in microList:
		print(micro)
		#df['rlnRandomSubset'] == np.where(df['rlnMicrographName'] == micro, subset, df['rlnRandomSubset'])
		df.loc[df['rlnMicrographName'] == micro, 'rlnRandomSubset'] = subset
		if subset == 1:
			subset = 2
		else:
			subset = 1
		#print(df.loc[df['rlnMicrographName'] == micro, 'rlnRandomSubset'])
			
	# Write out new star file
	starfile.write(df, args.o, overwrite=True)	
	# echo to console
	print(f"Done! Converted '{args.i}' to '{args.o}'")

	

