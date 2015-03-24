#! /usr/bin/python

import subprocess, argparse
import logging, sys

#Usage python generateData.py allConfigurationsFile begin_configuration_index ram_value ram_level_value resultFileWithPath iterations

def writeToFile(user, i, time_now, f1,f2,f3,f4,f5,f6,r1,f_output):
		f_output.write(user +',' + i +',' +time_now+',' + f1 + ',' + f2 + ',' + f3+ ',' + f4+ ',' + f5+ ',' + r1 + '\n')


if __name__ == "__main__":


	__doc__ = ""
	epi = ""

	parser = argparse.ArgumentParser(description=__doc__, epilog= epi)

	parser.add_argument('allConfigurationsFile', action='store', 
									help=(''))

	parser.add_argument('begin_configuration_index', action='store', 
									help=(''))
	parser.add_argument('ram_value',action='store',help=(''))
	parser.add_argument('ram_level_value',action='store',help=(''))
	
	parser.add_argument('resultFileWithPath',action='store',help=(''))
	parser.add_argument('iterations',action='store',help=(''))
	
	args = parser.parse_args()
	cpu_min_freq = "800000"
	f_output= open(args.resultFileWithPath,'w')
	f_configListFile = open(args.allConfigurationsFile,'r')

	for i in range(int(args.begin_configuration_index)-1,5):
		for line in f_configListFile:
			line = line.rstrip('\n')
			factor_values = line.split(":")[0:5]
			line =  next(f_configListFile)
			factor_levels = line.split(":")[0:5]
			
			#Usage: python configureSystem.py number_of_cores (1/3) cpu_min_freq cpu_max_freq governor io_scheduler_algo dirty_ratio
			cmd_configure = "python configureSystem.py "+ factor_values[2] +" " + cpu_min_freq + " " + factor_values[0] + " " + factor_values[1] + " " + factor_values[3] + " " + factor_values[4] 

			subprocess.call(cmd_configure,shell=True)

			cmd_user = "echo $USERNAME"
			user = subprocess.check_output(cmd_user,shell=True).rstrip('\n')
			
			for i in range(1, int(args.iterations)):
				#Run benchmark script
				cmd_benchmark = "python sysbench_benchmark.py"
				result= subprocess.check_output(cmd_benchmark,shell=True).rstrip('\n')

				cmd_date = "date"
				time_now = subprocess.check_output(cmd_date,shell=True).rstrip('\n')
				writeToFile(user, str(i), time_now, str(args.ram_level_value),factor_levels[0],factor_levels[1],factor_levels[2],factor_levels[3],factor_levels[4],str(result),f_output)

