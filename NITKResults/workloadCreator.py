import os

folder_path = "linear-algebra/kernels/2mm"
file_name = "2mm"

os.chdir('Gem5AcceleratorScheduler/tests/test-progs/polybench-c-4.2')  
cwd = os.getcwd() 
print "Current director is "+cwd+"\n"

for i in range(1,4):
    cmd = "g++ -I utilities -I {}{} utilities/polybench.c {}{}/{}{}.c -o {}{}" \
        .format(folder_path, i, folder_path, i, file_name, i, file_name, i)
    print cmd+"\n"
    os.system(cmd)
print "Done"
