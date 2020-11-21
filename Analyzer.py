import sys
import os
import numpy as np
import pydicom as dicom
import datetime
import pylab as pl


def timeParsing(oneLines):

    # 00:00, or 0:00, 형태로 생성되므로, 뒤의 쉼표와 가운데 세미콜론을 없애줘야함.

    if len(oneLines[4]) == 5:
        oneLines[4] = "0" + oneLines[4][:-1]  # 3자리면 앞에 0붙이고, 뒤에 쉼표 제거.
        oneLines[4] = oneLines[4][0:2] + oneLines[4][3:5]  # int 타입변환을 위해 가운데 콜론 제거.
    if len(oneLines[4]) == 6:
        oneLines[4] = oneLines[4][0:2] + oneLines[4][3:5] # int 타입변환을 위해 가운데 콜런제거 및 뒤에 쉼표 제거.

    # 모두 형태가 0000 으로 바뀐 상태.

    if oneLines[3] == "오전":
        if oneLines[4][0:2] == "12": # 오전 12시를 00시로 변경
            oneLines[4] = "00" + oneLines[4][2:4]

    if oneLines[3] == "오후":  # 오후면 시간에 12시간 더함.
        if oneLines[4][0:2] != "12": #오후 12시는 그대로 둠.
            oneLines[4] = str(int(oneLines[4][0:2]) + 12) + oneLines[4][2:4]

    return oneLines


def main():

    f1 = open("/Users/sangmin/Downloads/1.txt", 'r')
    #파일 끝에 "END" 를 입력해주어야함 !!!!!

    for a in range(5):
        cur_line = f1.readline().split()

    sm = []
    jy = []

    cur_line = f1.readline().split()
    while 1:

        next_line = f1.readline().split()

        if len(next_line) > 0 and next_line[0] == "END":
            break

        if len(cur_line) == 4 or len(cur_line) == 0:
            cur_line = next_line
            continue

        if len(next_line) == 4 or len(next_line) == 0:
            continue

        if cur_line[0][:-1] != "2020" and cur_line[0][:-1] != "2019":
            cur_line = next_line
            continue

        if next_line[0][:-1] != "2020" and next_line[0][:-1] != "2019":
            continue

        # 윗줄 아랫줄 보낸 사람이 다를 때!
        if len(cur_line) > 4 and len(next_line) > 4 and cur_line[5] != next_line[5]:

            cur_line_cal=cur_line.copy()
            next_line_cal=next_line.copy()

            cur_line_cal = timeParsing(cur_line_cal)
            next_line_cal = timeParsing(next_line_cal)


            cur_time = datetime.datetime(int(cur_line_cal[0][:-1]), int(cur_line_cal[1][:-1]), int(cur_line_cal[2][:-1]),
                                         int(cur_line_cal[4][0:2]), int(cur_line_cal[4][2:4]))
            next_time = datetime.datetime(int(next_line_cal[0][:-1]), int(next_line_cal[1][:-1]), int(next_line_cal[2][:-1]),
                                         int(next_line_cal[4][0:2]), int(next_line_cal[4][2:4]))

            if (next_time-cur_time).seconds == 0: #바로답장 했다면 패스
                cur_line = next_line
                continue

            if next_line[5] == "이상민" and (next_time-cur_time).seconds < 3600 and (next_time-cur_time).seconds > 300:
                print("캉캉이가 ", (next_time-cur_time).seconds, "초 만큼 늦어따")
                sm.append((next_time-cur_time).seconds/60)
            if next_line[5] == "쭈르르" and (next_time-cur_time).seconds < 3600 and (next_time-cur_time).seconds > 300:
                print("쭈르르가 ", (next_time - cur_time).seconds, "초 만큼 늦어따")
                jy.append((next_time - cur_time).seconds/60)

            cur_line = next_line

    n1, bins, patches = pl.hist(np.float32(np.array(sm)), bins=np.linspace(0, 60, 61))
    #n, bins, patches = pl.hist(np.float32(np.array(neutron)), bins=np.linspace(-1, 1, 101))
    #pl.gca().set_xscale("log")
    pl.gca().set_xscale("linear")
    pl.show()

    print('')
    print('그동안 상민이가 ', sum(sm), '분 늦었다')
    print('그동안 주연이가 ', sum(jy), '분 늦었다')

    f1.close()

if __name__ == "__main__":
    main()