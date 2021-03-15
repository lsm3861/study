import sys
import os
import numpy as np
from ssw2txt import mcpl

#f1 = open(sys.argv[1], 'r')
#f2 = open(sys.argv[2], 'w')


#flux2 = []
#err2 = []

#for x in range(1024):
#    flux2.append(0)
#    err2.append(0)

myfile = mcpl.MCPLFile
mcpl.convert2ascii()

f1 = open("/Users/sangmin/Downloads/STEP3_n.txt", 'r')

tally_number = 0
data_output_600_air = np.zeros((7, 400))
data_rel_error_600_air = np.zeros((7, 400))
directionality = np.array([])

while 1:
    cur_line = f1.readline().split()
    #print(cur_line[0])
    if f1.tell() == os.fstat(f1.fileno()).st_size:
        break

    if len(cur_line) != 0:
        if cur_line[0] == 'index':
            while 1:
                data_line = f1.readline().split()
                directionality = np.append(directionality, np.array(data_line[8]))
                if len(directionality)%10000 == 0:
                    #print(directionality)
                    print(len(directionality))
                    print(np.mean(directionality.astype(np.float64)))
                if f1.tell() == os.fstat(f1.fileno()).st_size:
                    break

print(np.mean(directionality.astype(np.float64)))




f1.close


sys.exit()
