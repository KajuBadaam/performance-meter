#! /usr/bin/python

import subprocess, argparse
import logging


def setScalingFreq(min_scaling_freq, max_scaling_freq, no_of_cores):

	for i in range(no_of_cores):
		for attempt in range(5):
			try:
				min_scaling_freq_path =  "/sys/devices/system/cpu/cpu"+str(i)+"/cpufreq/scaling_min_freq"		
				max_scaling_freq_path =  "/sys/devices/system/cpu/cpu"+str(i)+"/cpufreq/scaling_max_freq"	
				subprocess.call("echo "+ min_scaling_freq +" > " +min_scaling_freq_path, shell=True)
				subprocess.call("echo "+ max_scaling_freq +" > " +max_scaling_freq_path, shell=True)
				
				out1 = (subprocess.check_output("cat " + min_scaling_freq_path,shell=True).rstrip('\n')) 
				logging.info(out1)
				if out1!=min_scaling_freq:
					continue
				out2 = (subprocess.check_output("cat " + max_scaling_freq_path,shell=True).rstrip('\n')) 
				logging.info(out2)
				if out2!=max_scaling_freq:
					continue
				
			except:
			  	continue
			else:
				print ("CPU Freq " + str(i) + " set to " + out1 + ", " + out2)
			  	break
		else:
			print ("Failed, have to log")
			# we failed all the attempts - deal with the consequences.
		
		
def setGovernor(governor, no_of_cores):

	for i in range(no_of_cores):
		for attempt in range(5):
			try:
				governor_path =  "/sys/devices/system/cpu/cpu"+str(i)+"/cpufreq/scaling_governor"		
				
				subprocess.call("echo "+ governor +" > " +governor_path, shell=True)
				
				
				out1 = (subprocess.check_output("cat " + governor_path,shell=True).rstrip('\n')) 
				logging.info(out1)
				if out1!=governor:
					continue
				
				
			except:
			  	continue
			else:
				print ("CPU " + str(i) + "Governor set to " + out1)
			  	break
		else:
			print ("Failed, have to log")
			# we failed all the attempts - deal with the consequences.
		

		




if __name__ == "__main__":


	__doc__ = ""
	epi = ""

	NUMBER_OF_CORES=3
	parser = argparse.ArgumentParser(description=__doc__, epilog=epi)

	parser.add_argument('min_scaling_freq', action='store', 
									help=('Mininum scaling frequency'))


	parser.add_argument('max_scaling_freq', action='store', 
									help=(''))

	parser.add_argument('cpu_freq_governor', action='store', 
	                                 help=(''))

	#parser.add_argument('', action='store', 
	#                                help=(''))

	args = parser.parse_args()

	min_scaling_freq = args.min_scaling_freq
	max_scaling_freq = args.max_scaling_freq
	setScalingFreq(min_scaling_freq, max_scaling_freq, NUMBER_OF_CORES)

	cpu_freq_governor = args.cpu_freq_governor

	setGovernor(cpu_freq_governor, NUMBER_OF_CORES)

	#cmd = "sudo -s"
	#subprocess.call(cmd,shell=True)

	#min_scaling_freq_cmd = "echo "+ min_scaling_freq +" > /sys/devices/system/cpu/cpu0/cpufreq/scaling_min_freq "
	#max_scaling_freq_cmd = "echo "+ max_scaling_freq + " > /sys/devices/system/cpu/cpu0/cpufreq/scaling_max_freq"

	#TODO :  do for all CPU's

	#governor_cmd = "echo " + cpu_freq_governor + "> /sys/devices/system/cpu/cpu0/cpufreq/scaling_governor"


	#print min_scaling_freq_cmd
	#print max_scaling_freq_cmd

	#subprocess.call("ls", shell=True) 

	#subprocess.call(governor_cmd,shell=True)

	'''
	p = subprocess.Popen(cmd,stdout= subprocess.PIPE,shell=True)
	(output,err) = p.communicate()
	p_status = p.wait()

	print "Command Output : " , output
	print "Command return status : " , p_status
	'''