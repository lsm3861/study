import sys
import os
import numpy as np
import pydicom as dicom

def rt_dose_changer(sample_rt_dose, sample_ct, PHITS_DOSE_PATH, output_rt_dose):

    array_dose = list(get_dose(PHITS_DOSE_PATH))
    Boron_dose = np.array(array_dose[:901120])
    Boron_dose = np.reshape(Boron_dose, (55, 128, 128))
    Boron_dose = np.flip(Boron_dose, axis=1)
    Boron_dose = np.float32(Boron_dose)
    Nitrogen_dose = np.array(array_dose[901120:1802240])
    Nitrogen_dose = np.reshape(Nitrogen_dose, (55, 128, 128))
    Nitrogen_dose = np.flip(Nitrogen_dose, axis=1)
    Nitrogen_dose = np.float32(Nitrogen_dose)
    Hydrogen_dose = np.array(array_dose[1802240:])
    Hydrogen_dose = np.reshape(Hydrogen_dose, (55, 128, 128))
    Hydrogen_dose = np.flip(Hydrogen_dose, axis=1)
    Hydrogen_dose = np.float32(Hydrogen_dose)

    ################# MANUAL ##############
    array_dose = Boron_dose
    #print(array_dose.shape)
#    array_dose = np.array(Boron_dose)
    #print(len(Hydrogen_dose))
    #print(len(Boron_dose))
    #print(len(Nitrogen_dose))
#    array_dose = np.reshape(array_dose, (55, 128, 128))

    ds = dicom.dcmread(sample_rt_dose)
    ds_ct = dicom.dcmread(sample_ct)

    # TODO dose normalization 고민해봐야함.
    # Pixel data 교환.
    #array_dose = np.float32(array_dose)

    # Density dividing
    #array_dose = array_dose / get_voxel(PHITS_VOXEL_INPUT)
    # -------------------------------------------------- MANUAL#-------------------------------------------------- MANUAL
    # RBE or Q-value multiplying
    #Q_value = 2.34
    #array_dose = array_dose * Q_value

    #꼭 unit32로 바꾸어야만 들어가나..? Pixel Data를 바로 바꾸면 안되나? 도전!
    ds.DoseGridScaling = np.min(array_dose[array_dose > 0])
    #ds.DoseGridScaling = "5E-5"
    # print(ds.DoseGridScaling)
    array_dose = array_dose / ds.DoseGridScaling  # dose 수치 조절.
    #array_dose = np.uint32(array_dose)
    ds.PixelData = array_dose.tobytes()

    ds.Rows, ds.Columns = array_dose.shape[2], array_dose.shape[1]
    ds.NumberOfFrames = array_dose.shape[0]

    ds.GridFrameOffsetVector = []
    for i in range(ds.NumberOfFrames):
        ds.GridFrameOffsetVector.append(i * 3)
    if ds.DVHSequence:
        del ds.DVHSequence

    # only for the observation
    ds.PixelSpacing = [ds_ct.PixelSpacing[0]*(512/ds.Rows), ds_ct.PixelSpacing[1]*(512/ds.Rows)]

    #-------------------------------------------------- MANUAL#-------------------------------------------------- MANUAL
    IPP = [-238, -148, -72]  # or [-238, -148, 90]
    dose_grid_start = [IPP[0] - 0.5 * ds_ct.PixelSpacing[0], IPP[1] - 0.5 * ds_ct.PixelSpacing[1], IPP[2] - 0.5 * ds_ct.SliceThickness]
    ds.ImagePositionPatient = [dose_grid_start[0]+ds.PixelSpacing[0], dose_grid_start[1]+ds.PixelSpacing[1], dose_grid_start[2]+1.5 ]

    dicom.filewriter.dcmwrite(output_rt_dose, ds, write_like_original=True)

def get_dose(PHITS_DOSE_DATA):
    f1 = open(PHITS_DOSE_DATA, 'r')
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
            # print(len(dose))
        #elif len(cur_line) > 0 and cur_line[0] == "#" and cur_line[1] == "no." and cur_line[2] == "=" and cur_line[12] == ""
    f1.close()
    #print(len(dose))
    return dose

def get_voxel(PHITS_VOXEL_INPUT):
    f = open(PHITS_VOXEL_INPUT, 'r')
    read_all = f.read()
    f.close()

    read_all = read_all.split()
    voxel_index = np.array(read_all)
    voxel_index = np.reshape(voxel_index, (55, 128, 128))
    voxel_index = np.float32(voxel_index)

    #voxel_index[5001 == voxel_index] = 0.00121
    #voxel_index[5002 == voxel_index] = 1.09400
    #voxel_index[5003 == voxel_index] = 1.93500

    return voxel_index

def main():
    PHITS_DOSE_PATH = "/Users/sangmin/PHITS2DICOM_test/BNCT_dose_err.out"
    RD_SAMPLE_PATH = "./Brain_CT/44254984/C1/RD.1.2.246.352.71.7.482169467.721183.20140127155500.dcm"
    CT_SAMPLE_PATH = "./Brain_CT/44254984/C1/CT.1.2.840.113704.1.111.428.1390280577.191.dcm"
    RD_OUTPUT_PATH = "/Users/sangmin/PHITS2DICOM_test/RT_dose_changed.dcm"
    PHITS_VOXEL_INPUT = "./PHITS2DICOM/voxel.inp"

    rt_dose_changer(RD_SAMPLE_PATH,CT_SAMPLE_PATH, PHITS_DOSE_PATH, RD_OUTPUT_PATH)

if __name__ == "__main__":
    main()
