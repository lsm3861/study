import sys
import os
import numpy as np

#f1 = open(sys.argv[1], 'r')
#f2 = open(sys.argv[2], 'w')


#flux2 = []
#err2 = []

#for x in range(1024):
#    flux2.append(0)
#    err2.append(0)

f1 = open("/Users/sangmin/Downloads/mctao", 'r')
f2 = open("/Users/sangmin/Downloads/output.txt", 'w')

tally_number = 0
data_output_600_air = np.zeros((7, 400))
data_rel_error_600_air = np.zeros((7, 400))

while 1:
    cur_line = f1.readline().split()
    #print(cur_line[0])
    if f1.tell() == os.fstat(f1.fileno()).st_size:
        break

    if len(cur_line) != 0:
        if cur_line[0] == 'tally':
            f2.write(str(cur_line[0]) + " " + str(cur_line[1]))
            f2.write("\n")
            if cur_line[1] == 1:
                break
        if cur_line[0] == 'vals':
            data_line = f1.readline().split()
            f2.write(str(data_line[0]) + " " + str(data_line[1]))
            f2.write("\n")



f1.close
f2.close


sys.exit()
