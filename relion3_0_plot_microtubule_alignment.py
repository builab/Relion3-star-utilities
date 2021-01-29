#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Eliminate microtubule having less particles than a thrreshold

"""
Created on Sat Jun  6 17:35:42 2020

@author: kbui2

"""

import os, argparse, os.path
import matplotlib.pyplot as plt
import numpy as np


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

def plot_MT(helicalrecord, output):
	""" Plot the alignment parameter from microtubule """
	npart = len(helicalrecord)
	
	tilt = np.array([])
	rot = np.array([])
	psi = np.array([])
	shiftX = np.array([])
	shiftY = np.array([])


	
	for i in range(npart):
		tilt = np.append(tilt, [float(helicalrecord[i][tiltcol])])
		rot = np.append(rot, [float(helicalrecord[i][rotcol])])
		psi = np.append(psi, [float(helicalrecord[i][psicol])])
		shiftX = np.append(shiftX, float(helicalrecord[i][originxcol])*binfactor)
		shiftY = np.append(shiftY, float(helicalrecord[i][originycol])*binfactor)
		# Not using this yet
		if i == 0:
			origin = np.array([float(helicalrecord[i][coordxcol]), float(helicalrecord[i][coordycol])])
		else:
			origin = np.vstack((origin, [float(helicalrecord[i][coordxcol]), float(helicalrecord[i][coordycol])]))

	
	fig, axs = plt.subplots(2, 2)
	fig.set_size_inches(11, 10)
	partlist = np.linspace(1, npart, npart)
	axs[0, 0].scatter(partlist, rot)
	axs[0, 0].set_title('Rot (Phi)')
	axs[0, 0].set_ylim([-180, 180])
	axs[0, 1].set(xlabel='Particles', ylabel='Rot')

	axs[0, 1].scatter(partlist, psi)
	axs[0, 1].set_title('Psi')
	axs[0, 1].set_ylim([-180, 180])
	axs[0, 1].set(xlabel='Particles', ylabel='Psi')

	axs[1, 0].scatter(partlist, tilt)
	axs[1, 0].set_title('Tilt (Theta)')
	axs[1, 0].set_ylim([0, 180])
	axs[1, 0].set(xlabel='Particles', ylabel='Tilt')

	axs[1, 1].scatter(partlist, shiftX, color='lightgreen', label='ShiftX')
	axs[1, 1].scatter(partlist, shiftY, color='orange', label='ShiftY')
	axs[1, 1].set_title('Shift')
	axs[1, 1].set(xlabel='Particles', ylabel='Shift')
	axs[1, 1].legend(loc='upper right', shadow=True, fontsize='x-large')

	plt.savefig(output)
	plt.close()
		

	
if __name__=='__main__':
	# get name of input starfile, output starfile, output stack file
	print('WARNING: Only compatible with Relion 3.0 star file')
	
	parser = argparse.ArgumentParser(description='Plot coordinate of star file')
	parser.add_argument('--istar', help='Input particle star file',required=True)
	parser.add_argument('--ibin', help='Bin in current star file',required=True,default=4)
	parser.add_argument('--minpart', help='Minimum number of particles for fitting',required=False,default=5)
	parser.add_argument('--im', help='Directory for output fitted image',required=False,default="")

	args = parser.parse_args()
	
	
	instar = open(args.istar, 'r')
	minpart = float(args.minpart)
	binfactor = float(args.ibin)

			
	starlabels = learnstarheader(instar)
	# This might be redundant but left here	
	coordxcol = starcol_exact_label(starlabels, '_rlnCoordinateX')
	coordycol = starcol_exact_label(starlabels, '_rlnCoordinateY')
	originxcol = starcol_exact_label(starlabels, '_rlnOriginX')
	originycol = starcol_exact_label(starlabels, '_rlnOriginY')
	microcol = starcol_exact_label(starlabels, '_rlnMicrographName')
	imagecol = starcol_exact_label(starlabels, '_rlnImageName')
	helicalidcol = starcol_exact_label(starlabels, '_rlnHelicalTubeID')
	tiltcol = starcol_exact_label(starlabels, '_rlnAngleTilt')
	rotcol = starcol_exact_label(starlabels, '_rlnAngleRot')
	psicol = starcol_exact_label(starlabels, '_rlnAnglePsi')

	magcol = starcol_exact_label(starlabels, '_rlnMagnification')
	detpixelsizecol = starcol_exact_label(starlabels, '_rlnDetectorPixelSize')
	

	helicalid = 0
	microlist ={}
	prevhelicalid = 0
	micronum = 1
	helicalrecord = []

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
						output = args.im + '/' + 	str.replace(microname, ".mrc", "_MT") + prevhelicalid + ".png"
						print ("Writing " + output)
						plot_MT(helicalrecord, output);	
					else:
						print ('Ignore MT{:s} of {:s} with {:d} particles'.format(prevhelicalid, microname, len(helicalrecord)))
						
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
						output = args.im + '/' + 	str.replace(microname, ".mrc", "_MT") + prevhelicalid + ".png"
						print ("Writing " + output)
						plot_MT(helicalrecord, output);	
					else:
						print ('Ignore MT{:s} of {:s} with {:d} particles'.format(prevhelicalid, microname, len(helicalrecord)))
 
					# Write out
					helicalrecord = []
					
				micronum += 1
				helicalid += 1
				prevhelicalid = record[helicalidcol]
				helicalrecord.append(record)

			#if helicalid > 5:
			#	break
	print("Done!!!!")
		
	instar.close()
