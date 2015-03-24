#! /usr/bin/python

import subprocess, argparse

__doc__ = ""
epi = ""

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
cpu_freq_governor = args.cpu_freq_governor

#cmd = "sudo -s"
#subprocess.call(cmd,shell=True)

min_scaling_freq_cmd = "echo "+ min_scaling_freq +" > /sys/devices/system/cpu/cpu0/cpufreq/scaling_min_freq "
max_scaling_freq_cmd = "echo "+ max_scaling_freq + " > /sys/devices/system/cpu/cpu0/cpufreq/scaling_max_freq"

#TODO :  do for all CPU's

governor_cmd = "echo " + cpu_freq_governor + "> /sys/devices/system/cpu/cpu0/cpufreq/scaling_governor"


print min_scaling_freq_cmd
print max_scaling_freq_cmd

subprocess.call("ls", shell=True) 
subprocess.call(min_scaling_freq_cmd,shell=True)
subprocess.call(max_scaling_freq_cmd,shell=True)
subprocess.call(governor_cmd,shell=True)

'''
p = subprocess.Popen(cmd,stdout= subprocess.PIPE,shell=True)
(output,err) = p.communicate()
p_status = p.wait()

print "Command Output : " , output
print "Command return status : " , p_status
'''