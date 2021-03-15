import sys
import os
import numpy as np

'''
tally 라는 글자를 만나면 여태 까지 읽은 tally 개수를 + 1
vals 라는 글자를 만나면 다음줄부터 data 시작
data를 한줄씩 읽어오는데 짝수번째 칸은 output, 홀수번째 칸은 rel_error
한줄씩 읽어오면서 output과 rel_error 한번씩 처리할 때마다 energy bin 개수를 + 1
TLD 600의 output들을 다 평균내기. rel_error 은 값들을 제곱해서 더하고 제곱근 씌우기
값들은 같은 energy bin 끼리 더하거나 rel_error 값 도출 하기.
'''


#f1 = open(sys.argv[1], 'r')
#f2 = open(sys.argv[2], 'w')


#flux2 = []
#err2 = []

#for x in range(1024):
#    flux2.append(0)
#    err2.append(0)

f1 = open("/Users/sangmin/Downloads/mctap", 'r')

tally_number = 0
data_output_600_air = np.zeros((7, 400))
data_rel_error_600_air = np.zeros((7, 400))
data_output_600_covered = np.zeros((7, 400))
data_rel_error_600_covered = np.zeros((7, 400))
data_output_600_back = np.zeros((7, 400))
data_rel_error_600_back = np.zeros((7, 400))
data_output_700_air = np.zeros((7, 400))
data_rel_error_700_air = np.zeros((7, 400))
data_output_700_covered = np.zeros((7, 400))
data_rel_error_700_covered = np.zeros((7, 400))
data_output_700_back = np.zeros((7, 400))
data_rel_error_700_back = np.zeros((7, 400))

while 1:
    cur_line = f1.readline().split()
    #print(cur_line[0])
    if f1.tell() == os.fstat(f1.fileno()).st_size:
        break

    if len(cur_line) != 0:
        if cur_line[0] == 'vals':
            energy_bin_num = 0

            while 1:
                data_line = f1.readline().split()
                if data_line[0] == 'tfc':
                    break
                for i in range(int(len(data_line)/2)):
                    if tally_number > 34:
                        data_output_700_back[tally_number-35][energy_bin_num] = float(data_line[i*2])
                        data_rel_error_700_back[tally_number-35][energy_bin_num] = float(data_line[i*2+1])
                        energy_bin_num += 1
                    elif tally_number > 27:
                        data_output_700_covered[tally_number-28][energy_bin_num] = float(data_line[i*2])
                        data_rel_error_700_covered[tally_number-28][energy_bin_num] = float(data_line[i*2+1])
                        energy_bin_num += 1
                    elif tally_number > 20:
                        data_output_700_air[tally_number-21][energy_bin_num] = float(data_line[i*2])
                        data_rel_error_700_air[tally_number-21][energy_bin_num] = float(data_line[i*2+1])
                        energy_bin_num += 1
                    elif tally_number > 13:
                        data_output_600_back[tally_number-14][energy_bin_num] = float(data_line[i*2])
                        data_rel_error_600_back[tally_number-14][energy_bin_num] = float(data_line[i*2+1])
                        energy_bin_num += 1
                    elif tally_number > 6:
                        data_output_600_covered[tally_number-7][energy_bin_num] = float(data_line[i*2])
                        data_rel_error_600_covered[tally_number-7][energy_bin_num] = float(data_line[i*2+1])
                        energy_bin_num += 1
                    else:
                        data_output_600_air[tally_number][energy_bin_num] = float(data_line[i*2])
                        data_rel_error_600_air[tally_number][energy_bin_num] = float(data_line[i*2+1])
                        energy_bin_num += 1
            tally_number += 1

f2 = open("/Users/sangmin/Downloads/600_air.txt", 'w')
f3 = open("/Users/sangmin/Downloads/600_covered.txt", 'w')
f4 = open("/Users/sangmin/Downloads/600_back.txt", 'w')
f5 = open("/Users/sangmin/Downloads/700_air.txt", 'w')
f6 = open("/Users/sangmin/Downloads/700_covered.txt", 'w')
f7 = open("/Users/sangmin/Downloads/700_back.txt", 'w')
f8 = open("/Users/sangmin/Downloads/600_air_err.txt", 'w')
f9 = open("/Users/sangmin/Downloads/600_covered_err.txt", 'w')
f10 = open("/Users/sangmin/Downloads/600_back_err.txt", 'w')
f11 = open("/Users/sangmin/Downloads/700_air_err.txt", 'w')
f12 = open("/Users/sangmin/Downloads/700_covered_err.txt", 'w')
f13 = open("/Users/sangmin/Downloads/700_back_err.txt", 'w')

for i in range(385):
    tmp_array = data_output_600_air[:, i]
    f2.write(str(tmp_array[tmp_array!=0].mean()))
    f2.write('\n')
    tmp_array = data_output_600_covered[:, i]
    f3.write(str(tmp_array[tmp_array!=0].mean()))
    f3.write('\n')
    tmp_array = data_output_600_back[:, i]
    f4.write(str(tmp_array[tmp_array!=0].mean()))
    f4.write('\n')
    tmp_array = data_output_700_air[:, i]
    f5.write(str(tmp_array[tmp_array!=0].mean()))
    f5.write('\n')
    tmp_array = data_output_700_covered[:, i]
    f6.write(str(tmp_array[tmp_array!=0].mean()))
    f6.write('\n')
    tmp_array = data_output_700_back[:, i]
    f7.write(str(tmp_array[tmp_array!=0].mean()))
    f7.write('\n')
    tmp_array = data_rel_error_600_air[:, i]
    tmp_array[1 == tmp_array] = 0
    f8.write(str(np.sqrt(np.sum(np.square(tmp_array)))))
    #f8.write(str(tmp_array[tmp_array!=0].mean()))
    f8.write('\n')

    tmp_array = data_rel_error_600_covered[:, i]
    tmp_array[1 == tmp_array] = 0
    f9.write(str(np.sqrt(np.sum(np.square(tmp_array)))))
    #f9.write(str(tmp_array[tmp_array!=0].mean()))
    f9.write('\n')

    tmp_array = data_rel_error_600_back[:, i]
    tmp_array[1 == tmp_array] = 0
    f10.write(str(np.sqrt(np.sum(np.square(tmp_array)))))
    #f10.write(str(tmp_array[tmp_array!=0].mean()))
    f10.write('\n')

    tmp_array = data_rel_error_700_air[:, i]
    tmp_array[1 == tmp_array] = 0
    f11.write(str(np.sqrt(np.sum(np.square(tmp_array)))))
    #f11.write(str(tmp_array[tmp_array!=0].mean()))
    f11.write('\n')

    tmp_array = data_rel_error_700_covered[:, i]
    tmp_array[1 == tmp_array] = 0
    f12.write(str(np.sqrt(np.sum(np.square(tmp_array)))))
    #f12.write(str(tmp_array[tmp_array!=0].mean()))
    f12.write('\n')

    tmp_array = data_rel_error_700_back[:, i]
    tmp_array[1 == tmp_array] = 0
    f13.write(str(np.sqrt(np.sum(np.square(tmp_array)))))
    #f13.write(str(tmp_array[tmp_array!=0].mean()))
    f13.write('\n')


                #if data_line[0] == '6.8000E-02':
                #flux2[cur_pos][i] = data_line[1]
                #err2[cur_pos] = data_line[2]
                #z = str(flux2)
                #f2.write('\t')
                #f2.write(str(data_line[1]))
                #if data_line[0] == 'total':
                #    f2.write('\n')
                #    break
                #f2.write('\t')

'''
for x in range(1024):
    z = str(flux2)
    #q = str(err2)
    cur_pos = str(cur_pos+1)
    f2.write(cur_pos)
    f2.write('\t')
    f2.write(z)
    f2.write('\t')
    #f2.write('\t')
    #f2.write(q)
    f2.write('\n')
'''

f1.close
f2.close
f3.close
f4.close
f5.close
f6.close
f7.close
f8.close
f9.close
f10.close
f11.close
f12.close
f13.close

sys.exit()
