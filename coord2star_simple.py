#!/usr/bin/env python3
# -*- convert from plain coordinate to relion coordinate

import os, sys, argparse, os.path, glob, math
import numpy as np
import pandas as pd


def write_star_3_1(dfin, outfile):
	out = open(outfile, 'w')
	out.write("# version 30001\n\n")
	out.write("data_\n\n")
	out.write("loop_\n")
	for i in range(len(dfin.columns)):
		out.write('_{:s} #{:d}\n'.format(dfin.columns[i], i+1))
	out.write(dfin.to_string(index=False, header=False))
	out.close()		

	
if __name__=='__main__':
	# get name of input starfile, output starfile, output stack file
	print('WARNING: Only compatible with Relion 3.1 star file')
	
	parser = argparse.ArgumentParser(description='Convert plain coordinate file to Relion star 3.1 format')
	parser.add_argument('--idir', help='Input folder',required=True)
	parser.add_argument('--odir', help='Output folder',required=True)
	parser.add_argument('--ibin', help='Bin in current coordinate',required=True,default=1)


	args = parser.parse_args()
	
	binfactor = float(args.ibin)
	listCoord = glob.glob(args.idir + "/*.txt")
	header_list = ["rlnCoordinateX", "rlnCoordinateY", "rlnAutopickFigureOfMerit"]


	for file in listCoord:
		name = os.path.basename(file)
		name = name.replace('.txt', '')
		print(name)
			
		df = pd.read_csv(file, delim_whitespace=True, names=header_list, index_col=False)
		# Delete first row
		df = df.iloc[1: , :]
		#print(df)
		# Processing & write star file
		df['rlnClassNumber'] = np.ones(len(df), dtype=np.int8)
		df['rlnCoordinateX'] = pd.to_numeric(df['rlnCoordinateX'], downcast="float")*binfactor
		df['rlnCoordinateY'] = pd.to_numeric(df['rlnCoordinateY'], downcast="float")*binfactor

		write_star_3_1(df, args.odir + '/' + name + '.star')


