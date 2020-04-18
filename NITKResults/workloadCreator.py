import os
import sys

folder_path = "linear-algebra/kernels/2mm"
file_name = "2mm"

polybench = "tests/test-progs/polybench-c-4.2"
cmd = 'Gem5AcceleratorScheduler/{}'.format(polybench)
print cmd
os.chdir(cmd)
cwd = os.getcwd() 
print "Current director is "+cwd+"\n"

for i in range(1,4):
    cmd = "g++ -I utilities -I {}{} utilities/polybench.c {}{}/{}{}-fpga.c -o {}{}" \
        .format(folder_path, i, folder_path, i, file_name, i, file_name, i)
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
            f.write("process1.cmd = ['{}/{}1']\n\
process2 = LiveProcess()\n\
process2.pid = 1101;\n\
process2.cmd = ['{}/{}2']\n\
process3 = LiveProcess()\n\
process3.pid = 1103;\n\
process3.cmd = ['{}/{}3']\n".format(polybench, file_name, polybench, file_name, polybench, file_name))
            continue
        
        f.write(line)
        if sys.argv[1]=="new" and "system.fpga = [FpgaCPU()" in line:
            f.write("system.fpga[0].scheduler_object = FPGAScheduler(time_to_process = '1ps')\n")
        
        if line.strip("\n")=="system.cpu[0].createThreads()":
            f.write("\nif np>1:\n\
\tsystem.cpu[1].workload = process2\n\
\tsystem.cpu[1].createThreads()\n\
\n\
if np>2:\n\
\tsystem.cpu[2].workload = process3\n\
\tsystem.cpu[2].createThreads())\n\n")

print "completed the work"
