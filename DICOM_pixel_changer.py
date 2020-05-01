import pydicom as dicom
import numpy as np
from PIL import Image, ImageDraw
import matplotlib.pyplot as plt
import csv
import os
import datetime
import sys
import glob

def ct_pixel_changer(CT_image, output_CT):

    ds = dicom.dcmread(CT_image)

    # Pixel data
    pixel_air = np.zeros_like(ds.pixel_array).copy()
    pixel_water = np.ones_like(ds.pixel_array).copy()*1024

    # Pixel data 교환.
    #array_dose = np.uint32(pixel_value)
    ds.PixelData = pixel_water.tobytes()

    dicom.filewriter.dcmwrite(output_CT, ds, write_like_original=True)


def main():
    # TODO 인풋파일 path 정리하는 함수 필요.

    files = []
    file_list =[]
    for fname in glob.glob("./CT_for_pixel_changer/CT.*", recursive=False):
        print("loading: {}".format(fname))
        file_list.append(fname)
        files.append(dicom.dcmread(fname))
    print("file count: {}".format(len(files)))

    # skip files with no SliceLocation (eg scout views)
    slices = []
    skipcount = 0
    for f in files:
        if hasattr(f, 'SliceLocation'):
            slices.append(f)
        else:
            skipcount = skipcount + 1
    print("skipped, no SliceLocation: {}".format(skipcount))

    # ensure they are in the correct order
    slices = sorted(slices, key=lambda s: s.SliceLocation)

    for CT_path in file_list:
        output_CT_path = CT_path[:-4] + "_changed.dcm"
        ct_pixel_changer(CT_path, output_CT_path)

    CT_path = "./Brain_CT/42860819/C1/CT.1.2.840.113704.1.111.5956.1407919894.5141.dcm"
    output_CT_path =""
    RP_path = "./Brain_CT/42860819/C1/RP.1.2.246.352.71.5.482169467.351676.20140814101105.dcm"
    RD_path = "./Brain_CT/42860819/C1/RD.1.2.246.352.71.7.482169467.884472.20140818115809.dcm"
    output_RD_path = "./Brain_CT/42860819/C1_changed/RT_dose_changed.dcm"





if __name__ == "__main__":
    main()
