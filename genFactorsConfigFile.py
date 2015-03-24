#! /usr/bin/python

import subprocess, argparse
import itertools

parser = argparse.ArgumentParser()
parser.add_argument('configureSystemFile', action='store', 
								help=(''))

parser.add_argument('allConfigurationsListFile', action='store', 
								help=(''))
args = parser.parse_args()

with open(args.configureSystemFile) as f:
	with open(args.allConfigurationsListFile,'w') as fwrite:

		final_list = []
		for line in f:
			line = line.rstrip('\n')
			factor_level = line.split(":")[1:3]
			
			final_list.append(factor_level)

		bits =["".join(seq) for seq in itertools.product("01", repeat=5)]

		for i in range(0,32):

			for factor in range(0,5):
				fwrite.write(final_list[factor][int(bits[i][factor])]+ ":")
			fwrite.write('\n')
			for factor in range(0,5):
				if int(bits[i][factor]) ==0:
					val = "1"
				else:
					val = "-1"	
				fwrite.write(val+ ":")
			fwrite.write('\n')

fwrite.close()