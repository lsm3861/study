import pylab as pl
import numpy as np
import sys
import os
import pydicom as dicom

def main():

    f1 = open("/Users/sangmin/Downloads/new_snyder/snyder_10dia_29bins/Step2_phsp_dmp.out.total", 'r')
    neutron = []
    gamma = []

    #TODO Photon, neutron dose case should be added
    while 1:
        cur_line = f1.readline().split()
        if f1.tell() == os.fstat(f1.fileno()).st_size:
            break

        #D를 E로 바꾸어줘야함!
        if len(cur_line) > 0 and cur_line[0] == "2.112000000000000E+03":
            neutron.append(cur_line[7])
        elif len(cur_line) > 0 and cur_line[0] == "2.200000000000000E+01":
            gamma.append(cur_line[7])
    f1.close()

    n, bins, patches = pl.hist(np.float32(np.array(neutron)), bins=np.logspace(np.log10(1E-9), np.log10(10.0), 201))
    #n, bins, patches = pl.hist(np.float32(np.array(gamma)), bins=np.linspace(0, 5, 101))
    pl.gca().set_xscale("log")
    #pl.gca().set_xscale("linear")
    pl.show()

    f2 = open("/Users/sangmin/Downloads/new_snyder/snyder_10dia_29bins/Step2_phsp_Anal.out", 'w')
    for a in range(len(n)):
        f2.write(str(n[a]))
        f2.write("\n")
    f2.close()

if __name__ == "__main__":
    main()
