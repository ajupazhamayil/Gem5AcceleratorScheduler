

import os
import sys

# Number of processors
np = 4
folder_path = "stencils/heat-3d"
file_name = "heat-3d"

cmd = "/home/gem5lab/Gem5"
os.chdir(cmd)

polybench = "tests/test-progs/polybench-c-4.2"
cmd = 'Gem5AcceleratorScheduler/{}'.format(polybench)
print cmd
os.chdir(cmd)
cwd = os.getcwd() 
print "Current director is "+cwd+"\n"

for i in range(1,np+1):
    cmd = "g++ -I utilities -I {}{} utilities/polybench.c {}{}/{}-fpga.c -o {}{}" \
        .format(folder_path, i, folder_path, i, file_name, file_name, i-1)
    print cmd+"\n"
    os.system(cmd)
print "Done making workload \n"


print "Making the python config file \n"
os.chdir("/home/gem5lab/Gem5/Gem5AcceleratorScheduler/\
configs/tuturial")  
cwd = os.getcwd() 
print "Current director is "+cwd+"\n"


with open(file_name+"-fpga.py", "r") as f:
    lines = f.readlines()

temp = file_name+"-mulCPU.py"

if os.path.exists(temp):
    os.remove(temp)
    print "Removed the existing config \n"

with open(temp, "w") as f:
    for line in lines:

        if "system.fpga[0].scheduler_object" in line:
            continue

        if "process1.cmd" in line:
            f.write("process1.cmd = ['{}/{}{}']\n".format(polybench, file_name, 0))
            for p in range(2,np+1):
                f.write("\
process{} = LiveProcess()\n\
process{}.pid = 110{};\n\
process{}.cmd = ['{}/{}{}']\n".format(p,p,p,p, polybench, file_name, p-1))
            continue
        
        f.write(line)
        if sys.argv[1]=="new" and "system.fpga = [FpgaCPU()" in line:
            f.write("system.fpga[0].scheduler_object = FPGAScheduler(policy = 1)\n")
        elif sys.argv[1]=="old" and "system.fpga = [FpgaCPU()" in line:
            f.write("system.fpga[0].scheduler_object = FPGAScheduler(policy = 0)\n")
        
        if line.strip("\n")=="system.cpu[0].createThreads()":
            for p in range(1,np):
                f.write("\nif np>{}:\n\
\tsystem.cpu[{}].workload = process{}\n\
\tsystem.cpu[{}].createThreads()\n\
\n".format(p,p,p+1,p))

print "completed the work"
