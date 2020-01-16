import pydicom as dicom
import numpy as np
from PIL import Image, ImageDraw
import matplotlib.pyplot as plt
import csv

CT_path = "./Brain_CT/42860819/C1/CT.1.2.840.113704.1.111.5956.1407919894.5141.dcm"
RP_path = "./Brain_CT/42860819/C1/RP.1.2.246.352.71.5.482169467.351676.20140814101105.dcm"
RS_path = "./Brain_CT/42860819/C1/RS.1.2.246.352.71.4.482169467.88444.20140818133058.dcm"
RD_path = "./Brain_CT/42860819/C1/RD.1.2.246.352.71.7.482169467.884472.20140818115809.dcm"

#TODO Dose 결과들을 위치들을 계산해주는 함수 필요함. N,B,H 는 9*9*60 voxels rin, rex는 61*61*60 voxels

def header_info(file_path):
    if "CT." in file_path:
        output_file = "CT"
    elif "RP." in file_path:
        output_file = "RP"
    elif "RS." in file_path:
        output_file = "RS"
    elif "RD." in file_path:
        output_file = "RD"

    f = open(output_file + ".txt", 'w')
    f.write(str(dicom.dcmread(file_path)))
    f.close()
    print(output_file+".txt is generated !")

    f = open(output_file + "_keys.txt", 'w')
    listified = list(dicom.dcmread(file_path).keys())
    for i in range(0, len(listified)):
        f.write( str( listified[i] ) )
        f.write("\n")
    f.close()
    print(output_file + "_keys.txt is generated !")

header_info(CT_path)
header_info(RP_path)
header_info(RS_path)
header_info(RD_path)