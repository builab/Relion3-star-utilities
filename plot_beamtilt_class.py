#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Created on Sat Jun  6 17:35:42 2020

Plot beam tilt data to visualize the classification

@author: kbui2
"""

import sys, re
import matplotlib.pyplot as plt

def parse_beamtilt_value(infile):		  
	"""With an already opened beam tilt class file, parse beam tilt x & y"""
	dict = {}
	for line in infile:
		record = line.strip().split("=")
		#print(record[1])
		dict[record[0].strip()] = record[1]
		
		
	return [float(dict["beamtilt_x"]), float(dict["beamtilt_y"])]


if __name__=='__main__':
	# get name of input starfile, output starfile, output stack file	
	if len(sys.argv) < 2:
		sys.exit("Usage: python relion3_plot_beamtilt_class.py beamtilt_iter-fit_class_*.txt")
	
	list = sys.argv[1:]
	
	plt.figure()
	for file in list:
		m = re.search("(class_[0-9]+).txt$", file, re.I)
		beamtiltclass = m.group(1)
		infile = open(file, 'r')
		val = parse_beamtilt_value(infile)
		infile.close()
		plt.scatter(val[0], val[1], label=beamtiltclass)
		plt.ylabel("Beam tilt X")
		plt.xlabel("Beam tilt Y")
		plt.title("Beam Tilt Class")
		plt.legend(loc='upper right', shadow=True, fontsize='small')
		plt.axis("equal")
		plt.show
		
	plt.savefig("beamtilt_class.png")
