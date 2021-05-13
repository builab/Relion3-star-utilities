#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Created on Sat Jun  6 17:35:42 2020

Add rlnBeamTiltClass to the star file based on hole name pattern
for Polishing in group later.

Best to apply to micrographs_ctf.star after CtfFind step but it should
also work for any star file.

McGill Krios pattern HoleNumber_ShotNumber 

(1_1) -> Class 1
(1-4) -> Class 4
(2-3) -> Class 7

@author: kbui2
"""

import os, argparse, os.path, re

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
	parser.add_argument('--holeno', help='Number of holes used for beam shift',required=True)
	parser.add_argument('--offset', help='Add this offset to the beam tilt class',required=False, default="0")



	args = parser.parse_args()
	
	
	instar = open(args.istar, 'r')
	outstar= open(args.ostar, 'w')
	holeno = float(args.holeno)
	offset = int(args.offset)

		
	
	starlabels = learnstarheader(instar)
	microcol = starcol_exact_label(starlabels, '_rlnMicrographName')

	# Add the rlnBeamTiltClass
	lastlabel = starlabels[-1]
	searchObj = re.search('#([0-9]+)', lastlabel)
	nocol = int(searchObj.group(1))
	#print(nocol)
	starlabels.append('_rlnBeamTiltClass #' + str(nocol + 1) + '\n')
	
	writestarheader(outstar, starlabels)
	
	for line in instar:
		record = line.split()
		if len(record)==len(starlabels) - 1: # if line looks valid
			microname=record[microcol]
			microname = os.path.basename(microname)
			#print(microname)
			# Get hole number & Shot number
			m = re.search("([0-9]+)-([0-9]+).mrc$", microname, re.I)
			holeid = int(m.group(1))
			shotid = int(m.group(2))
			
			# Append the rlnBeamTiltClass
			record.append(str(holeno*(holeid - 1) + shotid + offset))
			writestarline(outstar,record)
					

			
	instar.close()
	outstar.close()
	
	print("Writing " + args.ostar " successfully")
