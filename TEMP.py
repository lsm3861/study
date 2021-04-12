import numpy as np
import pydicom as dicom
import matplotlib.pyplot as plt

def getNucDose(DATA_PATH):
    # Getting dose from PHITS output file.
    f1 = open(DATA_PATH, 'r')
    dose = []
    #TODO Photon, neutron dose case should be added
    while 1:
        cur_line = f1.readline().split()

        # End of the dose file.
        if len(cur_line) > 0 and cur_line[0] == "#" and cur_line[1] == "rijklst=":
            break
        if len(cur_line) > 0 and cur_line[0] == "#" and cur_line[1] == "mset" and cur_line[2] == "=":
            #print(cur_line)
            # -------------------------------------------------- MANUAL#-------------------------------------------------- MANUAL
            # Skip 20 lines
            for a in range(20):
                next_line = f1.readline().split()
                #print(next_line)
            # -------------------------------------------------- MANUAL#-------------------------------------------------- MANUAL
            # Dose reading for 1639 lines.
            for b in range(1280):
                cur_line = f1.readline().split()
                for c in range(len(cur_line)):
                    dose.append(cur_line[c]) # Dose stacking.
            # print(len(dose))
        #elif len(cur_line) > 0 and cur_line[0] == "#" and cur_line[1] == "no." and cur_line[2] == "=" and cur_line[12] == ""
    f1.close()
    #print(len(dose))
    return dose

def getGDose(DATA_PATH):
    # Getting dose from PHITS output file.
    f1 = open(DATA_PATH, 'r')
    dose = []
    #TODO Photon, neutron dose case should be added
    while 1:
        cur_line = f1.readline().split()

        # End of the dose file.
        if len(cur_line) > 0 and cur_line[0] == "#" and cur_line[1] == "rijklst=":
            #print(cur_line)
            break

        if len(cur_line) > 2 and cur_line[0] == "'no." and cur_line[len(cur_line)-2] == "photon":
            #print(cur_line)
            # -------------------------------------------------- MANUAL#-------------------------------------------------- MANUAL
            # Skip 20 lines
            for a in range(18):
                next_line = f1.readline().split()
                #print(next_line)
            # -------------------------------------------------- MANUAL#-------------------------------------------------- MANUAL
            # Dose reading for 1639 lines.
            for b in range(1280):
                cur_line = f1.readline().split()
                for c in range(len(cur_line)):
                    dose.append(cur_line[c]) # Dose stacking.
            # print(len(dose))
        #elif len(cur_line) > 0 and cur_line[0] == "#" and cur_line[1] == "no." and cur_line[2] == "=" and cur_line[12] == ""
    f1.close()
    #print(len(dose))
    return dose


def rt_dose_creator(sample_ct, sample_rt_plan, DIR_PATH, output_rt_dose):

    array_dose = list(getNucDose(DIR_PATH+"BNCT_dose.out"))
    Gamma_dose = list(getGDose(DIR_PATH+"photon_dose.out"))

    Gamma_dose = np.array(Gamma_dose[:2444227])
    Gamma_dose = np.reshape(Gamma_dose, (191, 191, 67)) # Z, X, Y 순서 인 듯 !
    Gamma_dose = np.flip(Gamma_dose, axis=2)
    #Gamma_dose = np.flip(Gamma_dose, axis=1)
    Gamma_dose = np.float32(Gamma_dose)

    # MeV/cm3 to Gy, density: 1.094E-3 kg/cm3, 1 MeV = 1.60218E-13
    Gamma_dose = (Gamma_dose / 0.001094) * 1.60218E-13

    # Dose parsing into 3 components ( Boron / Nitrogen / Hydrogen )
    Boron_dose = np.array(array_dose[:2444227])
    Boron_dose = np.reshape(Boron_dose, (191, 67, 191))
    Boron_dose = np.flip(Boron_dose, axis=2)
    Boron_dose = np.flip(Boron_dose, axis=1)
    Boron_dose = np.float32(Boron_dose)

    Nitrogen_dose = np.array(array_dose[2444227:4888454])
    Nitrogen_dose = np.reshape(Nitrogen_dose, (191, 67, 191))
    Nitrogen_dose = np.flip(Nitrogen_dose, axis=2)
    Nitrogen_dose = np.flip(Nitrogen_dose, axis=1)
    Nitrogen_dose = np.float32(Nitrogen_dose)

    Hydrogen_dose = np.array(array_dose[4888454:])
    Hydrogen_dose = np.reshape(Hydrogen_dose, (191, 67, 191))
    Hydrogen_dose = np.flip(Hydrogen_dose, axis=2)
    Hydrogen_dose = np.flip(Hydrogen_dose, axis=1)
    Hydrogen_dose = np.float32(Hydrogen_dose)

    plt.imshow(Gamma_dose[90], cmap=plt.cm.gray)
    plt.show()


def main():
    PHITS_DOSE_PATH = "/Users/sangmin/Downloads/BNCT_dose.out"
    RD_SAMPLE_PATH = "./Brain_CT/44254984/C1/RD.1.2.246.352.71.7.482169467.721183.20140127155500.dcm"
    CT_SAMPLE_PATH = "./Brain_CT/44254984/C1/CT.1.2.840.113704.1.111.428.1390280577.191.dcm"
    RD_OUTPUT_PATH = "/Users/sangmin/Boron.dcm"
    RP_SAMPLE_PATH = "./Brain_CT/44254984/C1/RP.1.2.246.352.71.5.482169467.300863.20140127145445.dcm"
    PHITS_VOXEL_INPUT = "./PHITS2DICOM/voxel.inp"
    DIR_PATH = "/Users/sangmin/PHITS2DICOM_test/"

    '''
    for a in range(10):
        plt.subplot(3,4,a+1)
        plt.imshow(ds_flipped[a,], cmap=plt.cm.bone)
    plt.show()
    '''
    #rt_dose_changer(RD_SAMPLE_PATH,CT_SAMPLE_PATH, PHITS_DOSE_PATH, RD_OUTPUT_PATH)
    rt_dose_creator(CT_SAMPLE_PATH,RP_SAMPLE_PATH, DIR_PATH, RD_OUTPUT_PATH)
    #np.fromfile()

if __name__ == "__main__":
    main()