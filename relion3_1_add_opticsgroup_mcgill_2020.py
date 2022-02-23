#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Created on Sat Jun	6 17:35:42 2020

WARNING: THis script is to parse the OpticsGroup for image from McGill Krios in 2019 and 2020. No hole information just number. Probably never 
Also, this script using the old way to parse Relion 3.1 header

Clone more OpticGroups to the star file based on hole name pattern
for Polishing in group later.


000000 -> Class 1
000001 -> Class 2
000007 -> Class 7
...
000016-> Class 16
000017-> Class 1


@author: kbui2
"""

import os, argparse, os.path, re

def learnstaropticsheader(infile):
	"""Learn which column contains which information from an already open starfile"""
	infile.seek(0) # Go to the beginning of the starfile
	doneopticsheader = False
	doneprelabels = False
	opticsheaderlabels = []
	
	donepreopticslabels = False

	while not donepreopticslabels:
		line=infile.readline()
		if line.startswith('data_optics'):
			donepreopticslabels = True # read until data_optics
	while not doneprelabels:
		line=infile.readline()
		if line.startswith('loop_'):
			doneprelabels = True # read until 'loop_'
	while not doneopticsheader:
		line=infile.readline()
		if not line.startswith('_'): # read all lines the start with '_'
			doneopticsheader = True
		else:
			opticsheaderlabels += [line] 
	infile.seek(0) # return to beginning of starfile before return
	return opticsheaderlabels

def writestaropticsheader(outfile,headerlabels):			
	"""With an already opened starfile write a header"""
	outfile.write('\ndata_optics\n\nloop_\n')
	for label in headerlabels:
		outfile.write(label)

def learnstarpartheader(infile, isMicro):
	"""Learn which column contains which information from an already open starfile"""
	infile.seek(0)
	donepartheader = False
	doneprelabels = False
	partheaderlabels = []

	doneprepartlabels = False

	while not doneprepartlabels:
		line=infile.readline()
		if isMicro < 1:
			if line.startswith('data_particles'):
				doneprepartlabels = True # read until data_optics
		else:
			if line.startswith('data_micrographs'):
				doneprepartlabels = True

	while not doneprelabels:
		line=infile.readline()
		if line.startswith('loop_'):
			doneprelabels = True # read until 'loop_'
	while not donepartheader:
		line=infile.readline()
		if not line.startswith('_'): # read all lines the start with '_'
			donepartheader = True
		else:
			partheaderlabels += [line]
	infile.seek(0) # return to beginning of starfile before return
	return partheaderlabels

def writestarpartheader(outfile,headerlabels):			
	"""With an already opened starfile write a header"""
	if isMicro < 1:
		outfile.write('\ndata_particles\n\nloop_\n')
	else:
		outfile.write('\ndata_micrographs\n\nloop_\n')
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
		outfile.write(item+'	')
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
	print('WARNING: Only compatible with Relion 3.1 star file & McGill pattern of holes')
	
	parser = argparse.ArgumentParser(description='')
	parser.add_argument('--istar', help='Input particle star file',required=True)
	parser.add_argument('--ostar', help='Output particle star file',required=True)
	parser.add_argument('--nogroup', help='Number of optic groups',required=True)
	parser.add_argument('--offset', help='Add this offset to the beam tilt class',required=False, default="0")
	parser.add_argument('--micro', help='Micrograph or particles (1 or 0), default = true',required=False, default="1")




	args = parser.parse_args()
	
	
	instar = open(args.istar, 'r')
	outstar= open(args.ostar, 'w')
	nogroup = int(args.nogroup)
	offset = int(args.offset)
	isMicro = int(args.micro)

		
	# Parse data_optics
	staropticslabels = learnstaropticsheader(instar)
	opticsgroupnamecol = starcol_exact_label(staropticslabels, '_rlnOpticsGroupName')
	opticsgroupcol = starcol_exact_label(staropticslabels, '_rlnOpticsGroup')
	#print(nocol)
	
	writestaropticsheader(outstar, staropticslabels)
	
	for line in instar:
		if line.startswith('_data_particles'):
			instar.seek(0)
			break
		record = line.split()
		#print(record)
		#print(len(record))
		if len(record)==len(staropticslabels): # if line looks valid
			# Replicate Record nogroup time 
			for groupid in range(nogroup):
				record[opticsgroupnamecol]= 'opticsGroup' + str(groupid + 1 + offset)
				record[opticsgroupcol] = str(groupid + 1 + offset)
				writestarline(outstar,record)
					
	outstar.write('\n')
	
	# Parse data_particles
	starlabels = learnstarpartheader(instar)
	microcol = starcol_exact_label(starlabels, '_rlnMicrographName')
	partopticsgroupcol = starcol_exact_label(starlabels, '_rlnOpticsGroup');

	# Write particle header
	writestarpartheader(outstar, starlabels)

	opticsgroupid = 0
	for line in instar:
		record = line.split()
		if len(record)==len(starlabels): # if line looks valid
			microname=record[microcol]
			microname = os.path.basename(microname)
			# Get hole number & Shot number
			m = re.search("([0-9][0-9][0-9][0-9][0-9]).mrc$", microname, re.I)
			microid = int(m.group(1))
			opticsgroupid = microid % nogroup + 1 + offset								 
			record[partopticsgroupcol] = str(opticsgroupid)

			writestarline(outstar,record)
																				
												
	instar.close()
	outstar.close()
	

