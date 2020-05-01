import sys
import os
import numpy as np
import pydicom as dicom

def rt_dose_changer(sample_rt_dose, PHITS_DOSE_PATH, output_rt_dose):

    array_dose = np.array(get_dose(PHITS_DOSE_PATH))
    array_dose = np.reshape(array_dose, (55, 128, 128))

    ds = dicom.dcmread(sample_rt_dose)

    # TODO dose normalization 고민해봐야함.
    # Pixel data 교환.
    array_dose = np.float32(array_dose)
    #ds.DoseGridScaling = np.min(array_dose)
    #array_dose = array_dose / np.min(array_dose)  # dose 수치 조절.
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
    ds.PixelSpacing = [ds.PixelSpacing[0]*4, ds.PixelSpacing[1]*4]

    dicom.filewriter.dcmwrite(output_rt_dose, ds, write_like_original=True)

def get_dose(PHITS_DOSE_DATA):
    f1 = open(PHITS_DOSE_DATA, 'r')
    dose = []

    while 1:
        cur_line = f1.readline().split()
        if f1.tell() == os.fstat(f1.fileno()).st_size:
            break
        if len(cur_line) > 0 and cur_line[0] == "#" and cur_line[1] == "no." and cur_line[2] == "=":
            # print(cur_line[3])
            for a in range(22):
                next_line = f1.readline().split()
                #print(next_line)
            for b in range(1639):
                cur_line = f1.readline().split()
                for c in range(len(cur_line)):
                    dose.append(cur_line[c])
            # print(len(dose))
    f1.close()
    return dose

def main():
    PHITS_DOSE_PATH = "./PHITS2DICOM/Boron_nuc_depth.out"
    RD_SAMPLE_PATH = "./Brain_CT/42860819/C1/RD.1.2.246.352.71.7.482169467.884472.20140818115809.dcm"
    RD_OUTPUT_PATH = "./PHITS2DICOM/RT_dose_changed.dcm"

    rt_dose_changer(RD_SAMPLE_PATH,PHITS_DOSE_PATH,RD_OUTPUT_PATH)
    array_dose = np.array(get_dose("./PHITS2DICOM/Boron_nuc_depth.out"))
    array_dose = np.reshape(array_dose, (55, 128, 128))

if __name__ == "__main__":
    main()
