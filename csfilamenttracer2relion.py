#/usr/bin/python3
# Convert cryosparc filament tracer picking to relion
# Cryosparc uses 64 bit for rlnHelicalTubeID, we use only the last 3 number
# Relion also need rlnAnglePsiPrior, rlnAngleTiltPrior and rlnAnglePsiFlipRatio
# Coordinate swapXY?
# Still very experimental

# Huy Bui, McGill 2022

import argparse, os
import starfile



if __name__=='__main__':
   	# get name of input starfile, output starfile, output stack file
	print('Script to convert star file from csparc2star filament tracer output to Relion 3.1')
	
	parser = argparse.ArgumentParser(description='Convert star 2 star')
	parser.add_argument('--i', help='Input',required=True)
	parser.add_argument('--o', help='Output',required=True)
	# Convert Coordinate
	args = parser.parse_args()
	stardict = starfile.read(args.i)
	df_optics = stardict['optics']	
	# This only to makes compatibles with Relion 3.1.2. Very stupid
	df_optics['rlnOpticsGroupName'] = 'opticsGroup1'
	df = stardict['particles']
	# Add column
	df['rlnAngleTiltPrior'] = 90
	df['rlnAnglePsiFlipRatio'] = 0.5
	df.rename(columns = {'rlnAnglePsi':'rlnAnglePsiPrior'}, inplace = True)
	df['rlnHelicalTubeID'] = df['rlnHelicalTubeID'] % 1000 # Take last 3 number only
	# If it is particles from 2D job
	# Reset shift X & Y to zero
	starfile.write(stardict, args.o, overwrite=True)
		
