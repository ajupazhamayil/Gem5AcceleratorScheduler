import os

folder_path = "linear-algebra/kernels/2mm"
file_name = "2mm"

polybench = "tests/test-progs/polybench-c-4.2"
cmd = 'Gem5AcceleratorScheduler/{}'.format(polybench)
print cmd
os.chdir(cmd)
cwd = os.getcwd() 
print "Current director is "+cwd+"\n"

for i in range(1,4):
    if i==1:
        k=""
    else:
        k=i
        cmd = "g++ -I utilities -I {}{} utilities/polybench.c {}{}/{}{}.c -o {}{}" \
            .format(folder_path, i, folder_path, i, file_name, i, file_name, k)
    print cmd+"\n"
    os.system(cmd)
print "Done making workload \n"


print "Making the python config file \n"
os.chdir("/home/gem5lab/Gem5/Gem5AcceleratorScheduler/\
configs/tuturial")  
cwd = os.getcwd() 
print "Current director is "+cwd+"\n"


with open(file_name+".py", "r") as f:
    lines = f.readlines()

with open(file_name+"-mulCPU.py", "w") as f:
    for line in lines:
        f.write(line)
        if line.strip("\n")=="system.cpu[0].createThreads()":
            f.write("\n if np>1:\n \
                \tsystem.cpu[1].workload = process2\n \
                \tsystem.cpu[1].createThreads()\n \
            \n \
            if np>2:\n \
                \tsystem.cpu[2].workload = process3\n \
                \tsystem.cpu[2].createThreads())\n")

        if line.strip("\n")=="process1.cmd = ['{}/{}']".format(polybench, file_name):
            f.write("\n process2 = LiveProcess()\n \
                \tprocess2.pid = 1101;\n \
                \tprocess2.cmd = ['{}/{}2']\n \
                \n \
                \tprocess3 = LiveProcess()\n \
                \tprocess3.pid = 1103;\n \
                \tprocess3.cmd = ['{}/{}3']\n".format(polybench, file_name))
