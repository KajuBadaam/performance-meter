import subprocess


subprocess.call("sysbench --test=cpu --cpu-max-prime=20000 run > output.txt", shell = True)


fp = open("output.txt")
for i, line in enumerate(fp):
    if i == 14:
        words = line.split()
        print words[2]
fp.close()
