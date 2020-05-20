import pylab as pl
import numpy as np
import sys
import os
import pydicom as dicom

def main():

    f1 = open("/Users/sangmin/Downloads/new_snyder/snyder_10dia_29bins/track_z.out", 'r')
    neutron_flux = []

    #TODO Photon, neutron dose case should be added
    while 1:
        cur_line = f1.readline().split()
        if f1.tell() == os.fstat(f1.fileno()).st_size:
            break

        #D를 E로 바꾸어줘야함!
        if len(cur_line) > 3 and cur_line[1] == "sum" and cur_line[2] == "over":
            neutron_flux.append(cur_line[3])

    f1.close()

    f2 = open("/Users/sangmin/Downloads/new_snyder/snyder_10dia_29bins/Flux_ENDF.out", 'w')
    for a in range(len(neutron_flux)):
        f2.write(neutron_flux[a])
        f2.write('\n')

    f2.close()

if __name__ == "__main__":
    main()
