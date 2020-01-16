import sys
import os

if len(sys.argv) == 1:
    print("python Au1024_68.py input_file output_file")
    sys.exit()
 
f1 = open(sys.argv[1], 'r')
f2 = open(sys.argv[2], 'w')


flux2 = [] 
err2 = []

for x in range(1024): 
    flux2.append(0)
    err2.append(0)

while 1: 
    cur_line = f1.readline().split()

    if f1.tell() == os.fstat(f1.fileno()).st_size:
        break

    if len(cur_line) == 2:
        if cur_line[0] == 'cell':
            next_line = f1.readline().split()

            if len(next_line) > 0 and next_line[0] == 'energy':
                cur_pos = int(cur_line[1]) - 1

                while 1:
                    data_line = f1.readline().split()


                    if data_line[0] == '6.8000E-02':
                        flux2[cur_pos] = data_line[1]
                        err2[cur_pos] = data_line[2]

                    if data_line[0] == 'total':
                        break

for x in range(1024):
    z = str(flux2)
    q = str(err2)

f2.write(z)
f2.write('\t')
f2.write('\t')
f2.write(q)
f2.write('\n')


f1.close
f2.close
sys.exit()
