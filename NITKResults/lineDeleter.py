
filename = raw_input("File name plz \n")

with open(filename, "r") as f:

    lines = f.readlines()

with open(filename, "w") as f:

    for line in lines:

        if line.strip("\n") != "system.fpga[0].scheduler_object = FPGAScheduler(time_to_process = '1ps')":

            f.write(line)

import os
cmd = "mv "+filename+" Gem5AcceleratorScheduler/configs/tuturial/" 
os.system(cmd)
