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

    # 1줄 날리기
    cur_line = f1.readline().split()

    #TODO Photon, neutron dose case should be added
    while 1:
        cur_line = f1.readline().split()
        if f1.tell() == os.fstat(f1.fileno()).st_size:
            break
        #if len(cur_line) > 2 and cur_line[1] == "2112": #and (pow(float(cur_line[3]), 2) + pow(float(cur_line[4]), 2)) <= 7.5*7.5:
        if len(cur_line) > 2:
            #neutron.append(cur_line[2]) # Energy
            #neutron.append(math.sqrt(pow(float(cur_line[3]), 2) + pow(float(cur_line[4]), 2))) # Distance from origin
            neutron.append(cur_line[7]) # Directionality
        #if len(cur_line) > 2 and cur_line[1] == "2112" and  cur_line[5] =="102.5":
        #    print(cur_line[3], cur_line[4], cur_line[5], " ", cur_line[8])
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

        #if len(cur_line) > 5 and cur_line[7] == "gamma":
        if len(cur_line) > 5:
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
    n, bins, patches = pl.hist(np.float32(np.array(neutron)), bins=np.linspace(0, 1, 101))
    #pl.gca().set_xscale("log")
    pl.gca().set_xscale("linear")
    pl.show()

    f2 = open(output_path, 'w')
    for a in range(len(n)):
        f2.write(str(n[a]))
        f2.write("\n")
    f2.close()

def gammaKnife_MCNP(input_path, output_path):

    f1 = open(input_path, 'r')
    neutron = []
    gamma_1D_1 = []
    gamma_1D_2 = []
    gamma_1D_3 = []
    gamma_1D_4 = []
    gamma_dir_1 = []
    gamma_dir_2 = []
    gamma_dir_3 = []
    gamma_dir_4 = []
    line_num=0

    #TODO Photon, neutron dose case should be added
    while 1:
        cur_line = f1.readline().split()
        if f1.tell() == os.fstat(f1.fileno()).st_size:
            break
        if len(cur_line) > 2 and cur_line[1] == "22":
            if cur_line[3] == "40":
                gamma_dir_1.append(cur_line[6])  # Directionality of X-axis
                if np.float32(cur_line[4]) < 0.0025 and np.float32(cur_line[4]) > -0.0025:
                   gamma_1D_1.append(cur_line[5])
            elif cur_line[3] == "-40":
                gamma_dir_1.append(-1*float(cur_line[6]))  # Directionality of X-axis
                if np.float32(cur_line[4]) < 0.0025 and np.float32(cur_line[4]) > -0.0025:
                   gamma_1D_1.append(cur_line[5])
            elif cur_line[4] == "40":
                gamma_dir_1.append(cur_line[7])      # Directionality of Y-axis
                if np.float32(cur_line[3]) < 0.0025 and np.float32(cur_line[3]) > -0.0025:
                   gamma_1D_1.append(cur_line[5])
            elif cur_line[4] == "-40":
                gamma_dir_1.append(-1*float(cur_line[7]))    # Directionality of Y-axis
                if np.float32(cur_line[3]) < 0.0025 and np.float32(cur_line[3]) > -0.0025:
                   gamma_1D_1.append(cur_line[5])
            elif cur_line[3] == "49":
                gamma_dir_2.append(cur_line[6])  # Directionality of X-axis
                if np.float32(cur_line[4]) < 0.0025 and np.float32(cur_line[4]) > -0.0025:
                   gamma_1D_2.append(cur_line[5])
            elif cur_line[3] == "-49":
                gamma_dir_2.append(-1*float(cur_line[6]))  # Directionality of X-axis
                if np.float32(cur_line[4]) < 0.0025 and np.float32(cur_line[4]) > -0.0025:
                   gamma_1D_2.append(cur_line[5])
            elif cur_line[4] == "49":
                gamma_dir_2.append(cur_line[7])      # Directionality of Y-axis
                if np.float32(cur_line[3]) < 0.0025 and np.float32(cur_line[3]) > -0.0025:
                   gamma_1D_2.append(cur_line[5])
            elif cur_line[4] == "-49":
                gamma_dir_2.append(-1*float(cur_line[7]))    # Directionality of Y-axis
                if np.float32(cur_line[3]) < 0.0025 and np.float32(cur_line[3]) > -0.0025:
                   gamma_1D_2.append(cur_line[5])
            elif cur_line[3] == "59":
                gamma_dir_3.append(cur_line[6])  # Directionality of X-axis
                if np.float32(cur_line[4]) < 0.0025 and np.float32(cur_line[4]) > -0.0025:
                   gamma_1D_3.append(cur_line[5])
            elif cur_line[3] == "-59":
                gamma_dir_3.append(-1*float(cur_line[6]))  # Directionality of X-axis
                if np.float32(cur_line[4]) < 0.0025 and np.float32(cur_line[4]) > -0.0025:
                   gamma_1D_3.append(cur_line[5])
            elif cur_line[4] == "59":
                gamma_dir_3.append(cur_line[7])      # Directionality of Y-axis
                if np.float32(cur_line[3]) < 0.0025 and np.float32(cur_line[3]) > -0.0025:
                   gamma_1D_3.append(cur_line[5])
            elif cur_line[4] == "-59":
                gamma_dir_3.append(-1*float(cur_line[7]))    # Directionality of Y-axis
                if np.float32(cur_line[3]) < 0.0025 and np.float32(cur_line[3]) > -0.0025:
                   gamma_1D_3.append(cur_line[5])
            elif cur_line[3] == "69":
                gamma_dir_4.append(cur_line[6])  # Directionality of X-axis
                if np.float32(cur_line[4]) < 0.0025 and np.float32(cur_line[4]) > -0.0025:
                   gamma_1D_4.append(cur_line[5])
            elif cur_line[3] == "-69":
                gamma_dir_4.append(-1*float(cur_line[6]))  # Directionality of X-axis
                if np.float32(cur_line[4]) < 0.0025 and np.float32(cur_line[4]) > -0.0025:
                   gamma_1D_4.append(cur_line[5])
            elif cur_line[4] == "69":
                gamma_dir_4.append(cur_line[7])      # Directionality of Y-axis
                if np.float32(cur_line[3]) < 0.0025 and np.float32(cur_line[3]) > -0.0025:
                   gamma_1D_4.append(cur_line[5])
            elif cur_line[4] == "-69":
                gamma_dir_4.append(-1*float(cur_line[7]))    # Directionality of Y-axis
                if np.float32(cur_line[3]) < 0.0025 and np.float32(cur_line[3]) > -0.0025:
                   gamma_1D_4.append(cur_line[5])

        line_num+=1
        if line_num%1000000==0:
            print(str(int(line_num/1000000)) + "%")
    f1.close()

    #print(np.mean(np.float32(np.array(gamma))))

    #n, bins, patches = pl.hist(np.float32(np.array(neutron)), bins=np.logspace(np.log10(1E-9), np.log10(10.0), 201))
    n1, bins, patches = pl.hist(np.float32(np.array(gamma_1D_1)), bins=np.linspace(-0.5, 0.5, 201))
    #n, bins, patches = pl.hist(np.float32(np.array(neutron)), bins=np.linspace(-1, 1, 101))
    #pl.gca().set_xscale("log")
    pl.gca().set_xscale("linear")
    pl.show()

    fn1 = open(output_path+"_n1", 'w')
    for a in range(len(n1)):
        fn1.write(str(n1[a]))
        fn1.write("\n")
    fn1.close()

    n2, bins, patches = pl.hist(np.float32(np.array(gamma_1D_2)), bins=np.linspace(-0.5, 0.5, 201))
    fn2 = open(output_path+"_n2", 'w')
    for a in range(len(n2)):
        fn2.write(str(n2[a]))
        fn2.write("\n")
    fn2.close()

    n3, bins, patches = pl.hist(np.float32(np.array(gamma_1D_3)), bins=np.linspace(-0.5, 0.5, 201))
    fn3 = open(output_path+"_n3", 'w')
    for a in range(len(n3)):
        fn3.write(str(n3[a]))
        fn3.write("\n")
    fn3.close()

    n4, bins, patches = pl.hist(np.float32(np.array(gamma_1D_4)), bins=np.linspace(-0.5, 0.5, 201))
    fn4 = open(output_path+"_n4", 'w')
    for a in range(len(n4)):
        fn4.write(str(n4[a]))
        fn4.write("\n")
    fn4.close()

    gd1, bins2, patches2 = pl.hist(np.float32(np.array(gamma_dir_1)), bins=np.linspace(0, 1, 101))
    fgd1 = open(output_path+"_gd1", 'w')
    for a in range(len(gd1)):
        fgd1.write(str(gd1[a]))
        fgd1.write("\n")
    fgd1.close()

    gd2, bins2, patches2 = pl.hist(np.float32(np.array(gamma_dir_2)), bins=np.linspace(0, 1, 101))
    fgd2 = open(output_path+"_gd2", 'w')
    for a in range(len(gd2)):
        fgd2.write(str(gd2[a]))
        fgd2.write("\n")
    fgd2.close()

    gd3, bins2, patches2 = pl.hist(np.float32(np.array(gamma_dir_3)), bins=np.linspace(0, 1, 101))
    fgd3 = open(output_path+"_gd3", 'w')
    for a in range(len(gd3)):
        fgd3.write(str(gd3[a]))
        fgd3.write("\n")
    fgd3.close()

    gd4, bins2, patches2 = pl.hist(np.float32(np.array(gamma_dir_4)), bins=np.linspace(0, 1, 101))
    fgd4 = open(output_path+"_gd4", 'w')
    for a in range(len(gd4)):
        fgd4.write(str(gd4[a]))
        fgd4.write("\n")
    fgd4.close()

def main():

    # Energy spectrum
    # Directionality (-1 ~ +1)
    #
    #PHITS("/Users/sangmin/Downloads/Step1_phsp_dmp.out.total", "/Users/sangmin/Downloads/PHITS_target_10MeV_Directionality.out")
    #PHITS("/Users/sangmin/Step2_phsp_dmp.out.total", "/Users/sangmin/PHITS_STEP2_Directionality.out")
    #PHITS("/Users/sangmin/Step3_phsp_dmp.out.total", "/Users/sangmin/PHITS_STEP3_Directionality.out")
    #MCNP("/Users/sangmin/Downloads/target_10MeV_wssa.txt", "/Users/sangmin/Downloads/MCNP6_target_10MeV_Directionality.out")
    # MCNP("/Users/sangmin/STEP2_wssa.txt", "/Users/sangmin/MCNP6_STEP2_Directionality.out")
    # MCNP("/Users/sangmin/STEP3_wssa.txt", "/Users/sangmin/MCNP6_STEP3_Directionality.out")
    #gammaKnife_MCNP("/Users/sangmin/Downloads/wssa_2E11.txt", "/Users/sangmin/Downloads/2E11")
    GEANT("/Users/sangmin/Downloads/Beam_exit.txt", "/Users/sangmin/Downloads/GEANT4_Beam_exit_Directionality_v3.out")
    #GEANT("/Users/sangmin/181119_phsp_New_Step_2.txt", "/Users/sangmin/GEANT4_STEP2_Directionality.out")
    #GEANT("/Users/sangmin/Downloads/181119_phsp_New_Step_3.txt", "/Users/sangmin/Downloads/GEANT4_STEP3_Directionality(3).out")


if __name__ == "__main__":
    main()
