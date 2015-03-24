#! /usr/bin/python

import subprocess, argparse
import logging

#Usage: python configureSystem.py number_of_cores (1/3) cpu_min_freq cpu_max_freq governor io_scheduler_algo dirty_ratio
#Code will throw an exception if a particular setting change fails. It will exit with code 4 if that happens.

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
			logging.warning("CPU " + str(i)+ " Frequency change failed")
			exit(4)
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
				print ("CPU " + str(i) + " Governor set to " + out1)
			  	break
		else:
			logging.warning("CPU " + str(i)+ " Governor change failed")
			exit(4)
		

def setIOScheduler(algo):

	
	for attempt in range(5):
		try:
			scheduler_path =  "/sys/block/sda/queue/scheduler"		
			
			subprocess.call("echo "+ algo +" > " + scheduler_path, shell=True)
			
			
			out1 = (subprocess.check_output("cat " + scheduler_path,shell=True).rstrip('\n'))
			current_algo=""
			flag = False
			for c in out1:
				if c=="]":
					flag=False

				if flag:
					current_algo+=c
				
				if c=="[":
					flag = True

				
			logging.info(current_algo)
			if current_algo!=algo:
				continue
				
			
		except:
		  	continue
		else:
			print ("IO Scheduler Algo set to " + current_algo)
		  	break
	else:
		logging.warning("IO Scheduler Algo change failed")
		exit(4)

		
def setDirtyRatio(dr_value):

	
	for attempt in range(5):
		try:
			f1=open("/etc/sysctl.conf", "r")
			data=f1.readlines()
			f1.close()
			for i in range(0, len(data)):
				
				if "dirty_ratio" in data[i]:
					data[i]="vm.dirty_ratio = " + dr_value
					break
			else:
				data.append("vm.dirty_ratio = " + dr_value)
			with open('/etc/sysctl.conf', 'w') as f1:
    				f1.writelines(data)
			
			subprocess.call("sysctl -p", shell=True)
	

			
			out1 = (subprocess.check_output("sysctl -a | grep \"vm.dirty_ratio\"", shell=True)).rstrip('\n')
			logging.info(out1)
			
			if (filter(str.isdigit, out1)) != dr_value:
				continue
			
		except Exception as e:
			logging.warning(e)
		  	continue
		else:
			print ("Dirty Ratio set to " + dr_value)
		  	break
	else:
		logging.warning("Dirty Ratio change failed.")
		exit(4)

def setNumberOfCores(no_of_cores, total_no_of_cores):

	for attempt in range(5):
		try:
			for i in range(1, total_no_of_cores):
			
				core_path =  "/sys/devices/system/cpu/cpu"+str(i)+"/online"
				if(i<no_of_cores):
					subprocess.call("echo '1' > " +core_path, shell=True)
				else:
					subprocess.call("echo '0' > " +core_path, shell=True)
				
				
			out1 = (subprocess.check_output("cat /proc/cpuinfo",shell=True).rstrip('\n')) 
			if out1.count("processor")!=no_of_cores:
				continue

				
				
		except Exception as e:
			logging.warning(e)
		  	continue
		else:
			print ("Number of cores set to " + str(no_of_cores))
		  	break
	else:
		logging.warning("Number of cores change failed")
		exit(4)	
		




if __name__ == "__main__":


	__doc__ = ""
	epi = ""

	
	parser = argparse.ArgumentParser(description=__doc__, epilog=epi)
	parser.add_argument('number_of_cores', action='store', help=('Dirty Ratio'))
	parser.add_argument('min_scaling_freq', action='store', help=('Mininum scaling frequency'))
	parser.add_argument('max_scaling_freq', action='store', help=(''))
	parser.add_argument('cpu_freq_governor', action='store', help=(''))
	parser.add_argument('io_scheduler_algo', action='store', help=('IO Scheduler Algorithm'))
	parser.add_argument('dirty_ratio', action='store', help=('Dirty Ratio'))
	
	args = parser.parse_args()

	min_scaling_freq = args.min_scaling_freq
	max_scaling_freq = args.max_scaling_freq
	cpu_freq_governor = args.cpu_freq_governor
	io_scheduler_algo = args.io_scheduler_algo
	dirty_ratio = args.dirty_ratio
	number_of_cores=int(args.number_of_cores)
	
	setNumberOfCores(number_of_cores, 3) #Should be done first otherwise the rest might fail
	setScalingFreq(min_scaling_freq, max_scaling_freq, number_of_cores)
	setGovernor(cpu_freq_governor, number_of_cores)
	setIOScheduler(io_scheduler_algo)
	setDirtyRatio(dirty_ratio)
	

	