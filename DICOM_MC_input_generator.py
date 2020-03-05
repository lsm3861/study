
# import pydicom as dicom
# import numpy as np
# from PIL import Image, ImageDraw
# import matplotlib.pyplot as plt
# import csv
#
# def header_info(file_path):
#     if "CT." in file_path:
#         output_file = "CT"
#     elif "RP." in file_path:
#         output_file = "RP"
#     elif "RS." in file_path:
#         output_file = "RS"
#     elif "RD." in file_path:
#         output_file = "RD"
#
#     f = open(output_file + ".txt", 'w')
#     f.write(str(dicom.dcmread(file_path)))
#     f.close()
#     print(output_file+".txt is generated !")
#
#     f = open(output_file + "_keys.txt", 'w')
#     listified = list(dicom.dcmread(file_path).keys())
#     for i in range(0, len(listified)):
#         f.write( str( listified[i] ) )
#         f.write("\n")
#     f.close()
#     print(output_file + "_keys.txt is generated !")


import pydicom as dicom
import numpy as np
import matplotlib.pyplot as plt
import sys
import glob
import mcpl
from scipy.io import FortranFile
import os
from subprocess import Popen, PIPE


    # # load the DICOM files
    # files = []
    # print('glob: {}'.format(sys.argv[1]))
    # for fname in glob.glob(sys.argv[1], recursive=False):
    #     print("loading: {}".format(fname))
    #     files.append(dicom.dcmread(fname))
    #
    # print("file count: {}".format(len(files)))
    #
    # # skip files with no SliceLocation (eg scout views)
    # slices = []
    # skipcount = 0
    # for f in files:
    #     if hasattr(f, 'SliceLocation'):
    #         slices.append(f)
    #     else:
    #         skipcount = skipcount + 1
    #
    # print("skipped, no SliceLocation: {}".format(skipcount))
    #
    # # ensure they are in the correct order
    # slices = sorted(slices, key=lambda s: s.SliceLocation)
    #
    # # pixel aspects, assuming all slices are the same
    # ps = slices[0].PixelSpacing
    # ss = slices[0].SliceThickness
    # ax_aspect = ps[1]/ps[0]
    # sag_aspect = ps[1]/ss
    # cor_aspect = ss/ps[0]
    #
    # # create 3D array
    # img_shape = list(slices[0].pixel_array.shape)
    # img_shape.append(len(slices))
    # img3d = np.zeros(img_shape)
    #
    # # fill 3D array with the images from the files
    # for i, s in enumerate(slices):
    #     img2d = s.pixel_array
    #     img3d[:, :, i] = img2d
    #
    # # HU to material index
    #
    # # Index based on RS_mask
    #
    #
    # # plot 3 orthogonal slices
    # a1 = plt.subplot(2, 2, 1)
    # plt.imshow(img3d[:, :, img_shape[2]//2])
    # a1.set_aspect(ax_aspect)
    #
    # a2 = plt.subplot(2, 2, 2)
    # plt.imshow(img3d[:, img_shape[1]//2, :])
    # a2.set_aspect(sag_aspect)
    #
    # a3 = plt.subplot(2, 2, 3)
    # plt.imshow(img3d[img_shape[0]//2, :, :].T)
    # a3.set_aspect(cor_aspect)
    #
    # plt.show()


def make3D():

    files = []
    for fname in glob.glob(sys.argv[1], recursive=False):
        print("loading: {}".format(fname))
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
    slices.reverse()

    img3D = np.stack([img2d.pixel_array for img2d in slices], axis=0)

    # plt.figure()
    # for i in range(1, 112):
    #     plt.subplot(11,11,i)
    #     plt.title("i = {}".format(i))
    #     plt.imshow(img3D[i-1], cmap=plt.cm.bone )
    # plt.show()
    return img3D

def hu2mcnp_mat():
    hu3D = make3D()

    # 원본 3D array를 유지하면서, 각각의 material array로 복사 후, 각 material array에 threshold를 이용해서
    # material index의 정보를 가진 마스크를 만든뒤 모두 합치기
    material_num = 3
    #mat1
    mat = []
    for i in range(1, material_num):
        mat[i] =[]
        mat

    for i in range(1, material_num):
        mat[[ (10 < mat1) & ( mat1< 100) ] = 1


    #Hounsfield Unit from CT images to Material Index of MCNP

def main():
    # TODO 인풋파일 path 정리하는 함수 필요.
    CT_path = "./Brain_CT/42860819/C1/CT.1.2.840.113704.1.111.5956.1407919894.5141.dcm"
    RP_path = "./Brain_CT/42860819/C1/RP.1.2.246.352.71.5.482169467.351676.20140814101105.dcm"
    RD_path = "./Brain_CT/42860819/C1/RD.1.2.246.352.71.7.482169467.884472.20140818115809.dcm"
    output_RD_path = "./Brain_CT/42860819/C1_changed/RT_dose_changed.dcm"
    calc_results = "B_dose.txt"
    MCNP_input = "MCNP_input"
    MCNP_data = "MCNP_data"

    # Parameters
    pixel_spacing_x = dicom.dcmread(CT_path).PixelSpacing[0]
    pixel_spacing_y = dicom.dcmread(CT_path).PixelSpacing[1]
    slice_thickness = dicom.dcmread(CT_path).SliceThickness   # 1:1 resolution
    voxel_x = 512 #dicom.dcmread().Rows  # int
    voxel_y = 512 #dicom.dcmread().Columns # int
    voxel_z = 60  #dicom.dcmread().? 슬라이스 개수 파악하는 함수 필요.

    f = open(MCNP_input + ".txt", 'w')
    #f.write(str(dicom.dcmread(file_path)))
    f.write("MCNP DICOM input by RPLab MC Input Generator v1\n")
    f.write("c Voxel size:\t\t") + f.write("%.3f * %.3f * %.3f * mm3\n" % (pixel_spacing_x, pixel_spacing_y, slice_thickness))
    f.write("c Voxel numbers:\t") + f.write("%d * %d * %d\n" % (voxel_x, voxel_y, voxel_z))
    f.write("c ") + f.write("=" * 78) + f.write("\n")
    f.write("c ") + f.write("*" * 78) + f.write("\n")
    f.write("c ") + f.write("{0:^78}".format("CELL CARDS")) + f.write("\n")
    f.write("c ") + f.write("*" * 78) + f.write("\n")
    f.write("read file=%s noecho\n" %MCNP_data)
    f.write("c ") + f.write("=" * 78) + f.write("\n")

    # UNIVERSE card start! material 개수 지정하여 작성 필요.
    # 1 0 -99 imp:p,e= 1 u=1 vol = 173142.990 $Air(void)
    # 10 10 -1.03 -99 imp:p,e=1 u=10 vol=1050.767   $rbm

    f.close()

    #os.sys
    #os.system("/Users/sangmin/GRIDCONV/gridconv")

    # p = Popen(['/Users/sangmin/GRIDCONV/gridconv'], stdout=PIPE, stderr=PIPE, stdin=PIPE)
    # p.stdout.read()
    #output = p.stdout.read()

    # p = Popen([r'/Users/sangmin/GRIDCONV/gridconv', 'and'], stdout=PIPE, stdin=PIPE)
    #output = p.stdout.read()
    #p.stdin.write()


    # f.close()
    # print(output_file+".txt is generated !")
    #
    # rt_dose_creator(CT_path, RP_path, calc_results, output_RD_path)

if __name__ == "__main__":
    main()
