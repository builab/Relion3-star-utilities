#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Eliminate microtubule having less particles than a thrreshold

"""
Created on Sat Jun  6 17:35:42 2020

@author: kbui2

"""

import os, argparse, os.path

def learnstarheader(infile):
	"""Learn which column contains which information from an already open starfile"""
	infile.seek(0) # Go to the beginning of the starfile
	doneheader = False
	doneprelabels = False
	headerlabels = []
	while not doneprelabels:
		line=infile.readline()
		if line.startswith('loop_'):
			doneprelabels = True # read until 'loop_'
	while not doneheader:
		line=infile.readline()
		if not line.startswith('_'): # read all lines the start with '_'
			doneheader = True
		else:
			headerlabels += [line] 
	infile.seek(0) # return to beginning of starfile before return
	return headerlabels

def writestarheader(outfile,headerlabels):		  
	"""With an already opened starfile write a header"""
	outfile.write('\ndata_\n\nloop_\n')
	for label in headerlabels:
		outfile.write(label)

def readstarline(infile):
	"""Read a record (line) from an already open starfile and return XXX"""
	line=infile.readline()
	records = line.split()
	return records

def writestarline(outfile,records):
	"""Write a record (line) to an already open starfile"""
	for item in records:
		outfile.write(item+'  ')
	outfile.write('\n')

def starcol_exact_label(starlabels, label):
	"""New function to do exact match of relion label such as _rlnImageCol"""
	for i, s in enumerate(starlabels):
		record=s.split()
		if label == record[0]:
			return i
	return -1

def writestarblock(outfile,recordblock):
	"""Write a record (line) to an already open starfile"""
	for record in recordblock:
		writestarline(outfile, record)

	
if __name__=='__main__':
	# get name of input starfile, output starfile, output stack file
	print('WARNING: Only compatible with Relion 3.0 star file')
	
	parser = argparse.ArgumentParser(description='Plot coordinate of star file')
	parser.add_argument('--istar', help='Input particle star file',required=True)
	parser.add_argument('--ostar', help='Output particle star file',required=True)
	parser.add_argument('--minpart', help='Minimum number of particles for fitting',required=False,default=5)


	#parser.add_argument('--nomicro', help='Test mode for only this number of micrographs',required=False)

	args = parser.parse_args()
	
	
	instar = open(args.istar, 'r')
	outstar= open(args.ostar, 'w')
	minpart = float(args.minpart)
			
	
	starlabels = learnstarheader(instar)
	# This might be redundant but left here	
	coordxcol = starcol_exact_label(starlabels, '_rlnCoordinateX')
	coordycol = starcol_exact_label(starlabels, '_rlnCoordinateY')
	originxcol = starcol_exact_label(starlabels, '_rlnOriginX')
	originycol = starcol_exact_label(starlabels, '_rlnOriginY')
	microcol = starcol_exact_label(starlabels, '_rlnMicrographName')
	imagecol = starcol_exact_label(starlabels, '_rlnImageName')
	helicalidcol = starcol_exact_label(starlabels, '_rlnHelicalTubeID')
	helicaltracklengthcol = starcol_exact_label(starlabels, '_rlnHelicalTrackLength')
	psicol = starcol_exact_label(starlabels, '_rlnAnglePsi')
	psiflipratiocol = starcol_exact_label(starlabels, '_rlnAnglePsiFlipRatio')
	psipriorcol = starcol_exact_label(starlabels, '_rlnAnglePsiPrior')
	tiltpriorcol = starcol_exact_label(starlabels, '_rlnAngleTiltPrior')
	tiltcol = starcol_exact_label(starlabels, '_rlnAngleTilt')
	rotcol = starcol_exact_label(starlabels, '_rlnAngleRot')
	dfucol = starcol_exact_label(starlabels, '_rlnDefocusU')
	dfvcol = starcol_exact_label(starlabels, '_rlnDefocusV')
	dfacol = starcol_exact_label(starlabels, '_rlnDefocusAngle')
	magcol = starcol_exact_label(starlabels, '_rlnMagnification')
	detpixelsizecol = starcol_exact_label(starlabels, '_rlnDetectorPixelSize')

	writestarheader(outstar, starlabels)
	

	helicalid = 0
	microlist ={}
	prevhelicalid = 0
	micronum = 1
	helicalrecord = []
	totalpart = 0
	totalpartafter = 0;
	for line in instar:
		record = line.split()
		if len(record)==len(starlabels): # if line looks valid
			microname=record[microcol]
			microname = os.path.basename(microname)
			# Create a dictionary, if microname not exist as key, insert
			# Parsing each helicaid into a block of record
			if microlist.get(microname):
				if prevhelicalid != record[helicalidcol]:
					if len(helicalrecord) >= minpart:
						totalpartafter = totalpartafter + len(helicalrecord)
						writestarblock(outstar, helicalrecord)
					else:
						print ('Eliminate MT{:s} of {:s} with {:d} particles'.format(prevhelicalid, microname, len(helicalrecord)))
						
					totalpart = totalpart + len(helicalrecord)
					helicalid += 1
					prevhelicalid = record[helicalidcol]
					helicalrecord = []
					helicalrecord.append(record)
				else:
					helicalrecord.append(record)

			else:
				microlist[microname] = micronum
				#print(" microname ", micronum)
				if micronum > 1:
					if len(helicalrecord) >= minpart:
						writestarblock(outstar, helicalrecord)
					else:
						print ('Eliminate MT{:s} of {:s} with {:d} particles'.format(prevhelicalid, microname, len(helicalrecord)))
 
					# Write out
					helicalrecord = []
					
				micronum += 1
				helicalid += 1
				prevhelicalid = record[helicalidcol]
				helicalrecord.append(record)

			#if helicalid > 5:
			#	break
	print("Done!!!!")
	print("Total number of particles before: {:d}".format(totalpart))
	print("Total number of particles after filtering MT less than {:d} particles: {:d}".format(int(minpart), totalpartafter))			
	instar.close()
	outstar.close()
