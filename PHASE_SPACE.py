import pylab as pl
import numpy as np
import sys
import os
import math
import pydicom as dicom

def PHITS(input_path, output_path):
    f1 = open(input_path, 'r')
    neutron = []
    gamma = []

    #TODO Photon, neutron dose case should be added
    while 1:
        cur_line = f1.readline().split()
        if f1.tell() == os.fstat(f1.fileno()).st_size:
            break

        #D를 E로 바꾸어줘야함!
        if len(cur_line) > 0 and cur_line[0] == "2.112000000000000E+03":
            #neutron.append(cur_line[7]) # Energy
            #neutron.append(math.sqrt(pow(float(cur_line[1]), 2) + pow(float(cur_line[2]), 2))) # Distance from origin
            neutron.append(cur_line[6]) # Directionality
        #elif len(cur_line) > 0 and cur_line[0] == "2.200000000000000E+01":
            #gamma.append(cur_line[7]) # Energy
            #gamma.append(math.sqrt(pow(float(cur_line[1]), 2) + pow(float(cur_line[2]), 2)))  # Distance from origin
            #gamma.append(cur_line[6]) # Directionality
    f1.close()

    #n, bins, patches = pl.hist(np.float32(np.array(neutron)), bins=np.logspace(np.log10(1E-9), np.log10(10.0), 201))
    #n, bins, patches = pl.hist(np.float32(np.array(gamma)), bins=np.linspace(0, 5, 51))
    n, bins, patches = pl.hist(np.float32(np.array(neutron)), bins=np.linspace(-1, 1, 101))
    #pl.gca().set_xscale("log")
    pl.gca().set_xscale("linear")
    pl.show()

    f2 = open(output_path, 'w')
    for a in range(len(n)):
        f2.write(str(n[a]))
        f2.write("\n")
    f2.close()

def MCNP(input_path, output_path):

    f1 = open(input_path, 'r')
    neutron = []
    gamma = []

    #TODO Photon, neutron dose case should be added
    while 1:
        cur_line = f1.readline().split()
        if f1.tell() == os.fstat(f1.fileno()).st_size:
            break
        if len(cur_line) > 2 and cur_line[1] == "2112": #and (pow(float(cur_line[3]), 2) + pow(float(cur_line[4]), 2)) <= 7.5*7.5:
            #neutron.append(cur_line[2]) # Energy
            #neutron.append(math.sqrt(pow(float(cur_line[3]), 2) + pow(float(cur_line[4]), 2))) # Distance from origin
            neutron.append(cur_line[8]) # Directionality
        if len(cur_line) > 2 and cur_line[1] == "2112" and  cur_line[5] =="102.5":
            print(cur_line[3], cur_line[4], cur_line[5], " ", cur_line[8])
        #elif len(cur_line) > 2 and cur_line[1] == "22" and (pow(float(cur_line[3]), 2) + pow(float(cur_line[4]), 2)) <= 7.5*7.5:
            #gamma.append(cur_line[2])  # Energy
            #gamma.append(math.sqrt(pow(float(cur_line[3]), 2) + pow(float(cur_line[4]), 2)))  # Distance from origin
            #gamma.append(cur_line[8]) # Directionality
    f1.close()

    #n, bins, patches = pl.hist(np.float32(np.array(neutron)), bins=np.logspace(np.log10(1E-9), np.log10(10.0), 201))
    #n, bins, patches = pl.hist(np.float32(np.array(gamma)), bins=np.linspace(0, 5, 51))
    n, bins, patches = pl.hist(np.float32(np.array(neutron)), bins=np.linspace(-1, 1, 101))
    #pl.gca().set_xscale("log")
    pl.gca().set_xscale("linear")
    pl.show()

    f2 = open(output_path, 'w')
    for a in range(len(n)):
        f2.write(str(n[a]))
        f2.write("\n")
    f2.close()

def GEANT(input_path, output_path):
    f1 = open(input_path, 'r')
    neutron = []
    gamma = []

    #TODO Photon, neutron dose case should be added
    while 1:
        cur_line = f1.readline().split()
        if f1.tell() == os.fstat(f1.fileno()).st_size:
            break

        if len(cur_line) > 5 and cur_line[7] == "neutron":
            #neutron.append(cur_line[6]) # Energy
            #neutron.append(math.sqrt(pow(float(cur_line[0]), 2) + pow(float(cur_line[1]), 2)))  # Distance from origin, unit: mm
            neutron.append(cur_line[5]) # Directionality
        #elif len(cur_line) > 5 and cur_line[7] == "gamma":
            #gamma.append(cur_line[6]) # Energy
            #gamma.append(math.sqrt(pow(float(cur_line[0]), 2) + pow(float(cur_line[1]), 2)))  # Distance from origin, unit: mm
            #gamma.append(cur_line[5]) # Directionality
    f1.close()

    #n, bins, patches = pl.hist(np.float32(np.array(neutron)), bins=np.logspace(np.log10(1E-9), np.log10(10.0), 201))
    #n, bins, patches = pl.hist(np.float32(np.array(gamma)), bins=np.linspace(0, 5, 51))
    n, bins, patches = pl.hist(np.float32(np.array(neutron)), bins=np.linspace(-1, 1, 101))
    #pl.gca().set_xscale("log")
    pl.gca().set_xscale("linear")
    pl.show()

    f2 = open(output_path, 'w')
    for a in range(len(n)):
        f2.write(str(n[a]))
        f2.write("\n")
    f2.close()

def main():

    # Energy spectrum
    # Directionality (-1 ~ +1)
    #
    #PHITS("/Users/sangmin/Step1_phsp_dmp.out.total", "/Users/sangmin/PHITS_STEP1_Directionality.out")
    #PHITS("/Users/sangmin/Step2_phsp_dmp.out.total", "/Users/sangmin/PHITS_STEP2_Directionality.out")
    #PHITS("/Users/sangmin/Step3_phsp_dmp.out.total", "/Users/sangmin/PHITS_STEP3_Directionality.out")
    MCNP("/Users/sangmin/STEP1_wssa.txt", "/Users/sangmin/MCNP6_STEP1_Directionality.out")
    MCNP("/Users/sangmin/STEP2_wssa.txt", "/Users/sangmin/MCNP6_STEP2_Directionality.out")
    MCNP("/Users/sangmin/STEP3_wssa.txt", "/Users/sangmin/MCNP6_STEP3_Directionality.out")
    #GEANT("/Users/sangmin/181119_phsp_New_Step_1.txt", "/Users/sangmin/GEANT4_STEP1_Directionality.out")
    #GEANT("/Users/sangmin/181119_phsp_New_Step_2.txt", "/Users/sangmin/GEANT4_STEP2_Directionality.out")
    #GEANT("/Users/sangmin/181119_phsp_New_Step_3.txt", "/Users/sangmin/GEANT4_STEP3_Directionality.out")


if __name__ == "__main__":
    main()
