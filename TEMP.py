import pylab as pl
import numpy as np
import sys
import os
import pydicom as dicom

f1 = open("/Users/sangmin/PHITS2DICOM_test/BNCT_dose_err.out", 'r')
dose = []
#TODO Photon, neutron dose case should be added
while 1:
    cur_line = f1.readline().split()
    if len(cur_line) > 0 and cur_line[0] == "#" and cur_line[1] == "rijklst=":
        #print(cur_line)
        break
    if len(cur_line) > 0 and cur_line[0] == "#" and cur_line[1] == "mset" and cur_line[2] == "=":
        #print(cur_line)
        # -------------------------------------------------- MANUAL#-------------------------------------------------- MANUAL
        for a in range(20):
            next_line = f1.readline().split()
            #print(next_line)
        # -------------------------------------------------- MANUAL#-------------------------------------------------- MANUAL
        for b in range(1639):
            cur_line = f1.readline().split()
            for c in range(len(cur_line)):
                dose.append(cur_line[c])
f1.close()
Boron_dose = np.array(dose[:901120])
Boron_dose = np.float32(Boron_dose)
Nitrogen_dose = np.array(dose[901120:1802240])
Nitrogen_dose = np.float32(Nitrogen_dose)
Hydrogen_dose = np.array(dose[1802240:])
Hydrogen_dose = np.float32(Hydrogen_dose)

n, bins, patches = pl.hist(Boron_dose[Boron_dose > 0], bins=np.linspace(0, 0.2, 100))
pl.gca().set_xscale("linear")
pl.show()

n, bins, patches = pl.hist(Nitrogen_dose[Nitrogen_dose > 0], bins=np.linspace(0, 0.2, 100))
pl.gca().set_xscale("linear")
pl.show()

n, bins, patches = pl.hist(Hydrogen_dose[Hydrogen_dose > 0], bins=np.linspace(0, 0.2, 100))
pl.gca().set_xscale("linear")
pl.show()