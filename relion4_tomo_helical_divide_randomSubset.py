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

Only work with Relion 3.1 and up.
"""

import numpy as np
import starfile
import argparse

from eulerangles import euler2matrix

if __name__=='__main__':
	print("Only work with Relion 4.0 tomo!!!")
	parser = argparse.ArgumentParser(description='Change rlnRandomSubset for helical refinement')
	parser.add_argument('--i', help='Input star file',required=True)
	parser.add_argument('--o', help='Output star file',required=True)
	parser.add_argument('--relion31', help='Star file from Relion 3.1 (1 or 0)',required=False, default=0)
	
	args = parser.parse_args()
		
	# Loading Relion star file
	stardict = starfile.read(args.i)
	
	df_optics = stardict['optics']	
	
	df = stardict['particles']
	
	# added by v0.1
	microList = df['rlnTomoName'].unique()
	
	subset = 1;
	
	for micro in microList:
		print(micro)
		#df['rlnRandomSubset'] == np.where(df['rlnMicrographName'] == micro, subset, df['rlnRandomSubset'])
		df.loc[df['rlnTomoName'] == micro, 'rlnRandomSubset'] = subset
		if subset == 1:
			subset = 2
		else:
			subset = 1
		#print(df.loc[df['rlnTomoName'] == micro, 'rlnRandomSubset'])
			
	# Write out new star file
	starfile.write(stardict, args.o, overwrite=True)	
	# echo to console
	print(f"Done! Converted '{args.i}' to '{args.o}'")

	

