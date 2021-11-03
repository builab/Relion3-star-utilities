#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Convert from plain coordinate to relion coordinate

import os, sys, argparse, os.path, glob, math
import numpy as np
import pandas as pd

def calculatepsi(x, y):
	"""Calculate the psi from the tangent"""
	xd = np.diff(x)
	yd = np.diff(y)
	psirad = np.arctan2(yd,xd)*-1
	psi = np.array(psirad)*180/math.pi
	psi = np.hstack([psi, [psi.max()]])
	return psi
	#print(psi)

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
	parser.add_argument('--rise', help='Helical rise in Angstrom',required=True,default=84)


	args = parser.parse_args()
	
	binfactor = float(args.ibin)
	riseAngstrom = float(args.rise)
	listCoord = glob.glob(args.idir + "/*.box")
	header_list = ["rlnCoordinateX", "rlnCoordinateY", "Box_X", "Box_Y", "rlnHelicalTubeID"]


	for file in listCoord:
		name = os.path.basename(file)
		name = name.replace('.box', '')
		print(name)
		if 'df_out' in globals(): 
			del(df_out)
			
		df = pd.read_csv(file, delim_whitespace=True, names=header_list)
		# Processing & write star file
		for helicalId in df.rlnHelicalTubeID.unique():
			print (helicalId)
			df2 = df[df.rlnHelicalTubeID == helicalId].copy()
			x = df2['rlnCoordinateX']
			y = df2['rlnCoordinateY']
			psi = calculatepsi(x, y)
			df2['rlnClassNumber'] = np.ones(len(df2), dtype=np.int8)
			df2['rlnAutopickFigureOfMerit'] = np.zeros(len(df2))
			df2['rlnAngleTiltPrior'] = np.ones(len(df2))*90
			df2['rlnAnglePsiPrior'] = psi
			df2['rlnHelicalTrackLengthAngst'] = np.arange(len(df2))*riseAngstrom
			df2['rlnAnglePsiFlipRatio'] = np.ones(len(df2))*0.5
			df2['rlnAngleRotFlipRatio'] = np.ones(len(df2))*0.5
			#print(df2)
			if helicalId == 1:
				df_out = df2.copy()
			else:
				df_out = df_out.append(df2)		
			del(df2)
		#print(df_out)
		df_out['rlnCoordinateX'] = df_out['rlnCoordinateX']*binfactor
		df_out['rlnCoordinateY'] = df_out['rlnCoordinateY']*binfactor

		write_star_3_1(df_out.drop(['Box_X', 'Box_Y'], axis=1), args.odir + '/' + name + '.star')
		
			
	

