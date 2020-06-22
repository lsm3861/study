import sys
import os
import numpy as np
import pydicom as dicom
import datetime

def rt_dose_changer(sample_rt_dose, sample_ct, PHITS_DOSE_PATH, output_rt_dose):

    array_dose = list(get_dose(PHITS_DOSE_PATH))
    # Dose parsing into 3 components ( Boron / Nitrogen / Hydrogen )
    Boron_dose = np.array(array_dose[:901120])
    Boron_dose = np.reshape(Boron_dose, (55, 128, 128))
    Boron_dose = np.flip(Boron_dose, axis=1)
    Boron_dose = np.float32(Boron_dose)
    print(Boron_dose.max())
    Nitrogen_dose = np.array(array_dose[901120:1802240])
    Nitrogen_dose = np.reshape(Nitrogen_dose, (55, 128, 128))
    Nitrogen_dose = np.flip(Nitrogen_dose, axis=1)
    Nitrogen_dose = np.float32(Nitrogen_dose)
    print(Nitrogen_dose.max())
    Hydrogen_dose = np.array(array_dose[1802240:])
    Hydrogen_dose = np.reshape(Hydrogen_dose, (55, 128, 128))
    Hydrogen_dose = np.flip(Hydrogen_dose, axis=1)

    Hydrogen_dose = np.float32(Hydrogen_dose)
    print(Hydrogen_dose.max())

    ################# MANUAL ##############
    array_dose = Hydrogen_dose

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
    #ds.DoseGridScaling = np.min(array_dose[array_dose > 0])
    ds.DoseGridScaling = "1"
    #ds.DoseGridScaling = array_dose.max()
    # print(ds.DoseGridScaling)
    #array_dose = array_dose / ds.DoseGridScaling  # dose 수치 조절.
    #array_dose = np.uint32(array_dose)
    array_dose[array_dose < np.max(array_dose) * 0.00001] = 0
    ds.PixelData = array_dose.tobytes()

    # test = np.frombuffer(ds.PixelData, dtype=np.float32)
    # print('Here !')
    # print(test.max())

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

    dicom.filewriter.dcmwrite(output_rt_dose, ds, write_like_original=False)

    # Pixel data 교환.
    '''
    array_dose = np.float32(array_dose)
    array_dose = np.uint32(array_dose)
    '''


def get_dose(PHITS_DOSE_DATA):
    # Getting dose from PHITS output file.
    f1 = open(PHITS_DOSE_DATA, 'r')
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
            for b in range(1639):
                cur_line = f1.readline().split()
                for c in range(len(cur_line)):
                    dose.append(cur_line[c]) # Dose stacking.
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

def rt_dose_creator(sample_ct, sample_rt_plan, PHITS_DOSE_PATH, output_rt_dose):
    ds_ct = dicom.dcmread(sample_ct)
    ds_plan = dicom.dcmread(sample_rt_plan)

    array_dose = list(get_dose(PHITS_DOSE_PATH))
    # Dose parsing into 3 components ( Boron / Nitrogen / Hydrogen )
    Boron_dose = np.array(array_dose[:901120])
    Boron_dose = np.reshape(Boron_dose, (55, 128, 128))
    Boron_dose = np.flip(Boron_dose, axis=1)
    Boron_dose = np.float32(Boron_dose)
    print(Boron_dose.max())
    Nitrogen_dose = np.array(array_dose[901120:1802240])
    Nitrogen_dose = np.reshape(Nitrogen_dose, (55, 128, 128))
    Nitrogen_dose = np.flip(Nitrogen_dose, axis=1)
    Nitrogen_dose = np.float32(Nitrogen_dose)
    print(Nitrogen_dose.max())
    Hydrogen_dose = np.array(array_dose[1802240:])
    Hydrogen_dose = np.reshape(Hydrogen_dose, (55, 128, 128))
    Hydrogen_dose = np.flip(Hydrogen_dose, axis=1)

    Hydrogen_dose = np.float32(Hydrogen_dose)
    print(Hydrogen_dose.max())

    ################# MANUAL ##############
    array_dose = Boron_dose

    ds_dose = rt_dose_header_setup(ds_ct, ds_plan, output_rt_dose)

    # TODO 몇몇 상수들은 dose_results(계산결과) 에서 불러오는 것이 좋을듯
    # TODO dose data 변환 후 입력.
    # TODO dose normalization 고민해봐야함.
    # Pixel data 교환.
    #array_dose = np.float32(array_dose)
    #ds_dose.DoseGridScaling = np.max(array_dose)
    ds_dose.DoseGridScaling = "1"


    #array_dose = array_dose / np.min(array_dose)  # dose 수치 조절.
    #array_dose = np.uint32(array_dose)

    array_dose[ array_dose < np.max(array_dose)*0.00001] = 0
    ds_dose.PixelData = array_dose.tobytes()

    #ds_dose.pixel_array = array_dose

    # dicom.filewriter.dcmwrite(output_rt_dose, ds_dose, write_like_original=True)

    ds_dose.Rows, ds_dose.Columns = array_dose.shape[2], array_dose.shape[1]
    ds_dose.NumberOfFrames = array_dose.shape[0]

    ds_dose.GridFrameOffsetVector = []
    for i in range(ds_dose.NumberOfFrames):
        ds_dose.GridFrameOffsetVector.append(i * 3)
    #if ds_dose.DVHSequence:
    #    del ds_dose.DVHSequence

    # only for the observation
    ds_dose.PixelSpacing = [ds_ct.PixelSpacing[0]*(512/ds_dose.Rows), ds_ct.PixelSpacing[1]*(512/ds_dose.Rows)]

    #-------------------------------------------------- MANUAL#-------------------------------------------------- MANUAL
    IPP = [-238, -148, -72]  # or [-238, -148, 90]
    dose_grid_start = [IPP[0] - 0.5 * ds_ct.PixelSpacing[0], IPP[1] - 0.5 * ds_ct.PixelSpacing[1], IPP[2] - 0.5 * ds_ct.SliceThickness]
    ds_dose.ImagePositionPatient = [dose_grid_start[0]+ds_dose.PixelSpacing[0], dose_grid_start[1]+ds_dose.PixelSpacing[1], dose_grid_start[2]+1.5 ]


    ds_dose.is_little_endian = True # True is default
    ds_dose.is_implicit_VR = False # True is default
    ds_dose.save_as(output_rt_dose)


def rt_dose_header_setup(dataset_ct, dataset_plan, output_rt_dose):
    # Header setup
    dataset_dose_meta = dicom.dataset.Dataset()
    dataset_dose_meta.MediaStorageSOPClassUID = '1.2.840.10008.5.1.4.1.1.481.2'
    dataset_dose_meta.MediaStorageSOPInstanceUID = "1.2.3"
    dataset_dose_meta.ImplementationClassUID = "1.2.3.4"
    dataset_dose = dicom.dataset.FileDataset(output_rt_dose, {}, file_meta=dataset_dose_meta, preamble=b"\0" * 128)
    dataset_dose.SpecificCharacterSet = dataset_ct.SpecificCharacterSet
    dataset_dose.InstanceCreationDate = datetime.datetime.now().strftime('%Y%m%d')
    dataset_dose.InstanceCreationTime = datetime.datetime.now().strftime('%H%M%S.%f')

    # TODO UID 파악 다시 해야함.
    # 얘네들 원리와 구조를 잘 모르겠음..
    # 다원메닥스 or 인피니티 와 협의해야할 항목.
    # Rule을 정해야함.
    # TEST VALUE 들로 채워둠.
    dataset_dose.Manufacturer = '123'
    dataset_dose.StationName = '123'
    dataset_dose.ManufacturerModelName = '123'
    dataset_dose.DeviceSerialNumber = '123'
    dataset_dose.SoftwareVersions = '1.0'
    dataset_dose.SeriesInstanceUID = '1.2.3'
    dataset_dose.SeriesNumber = '9'
    dataset_dose.FrameOfReferenceUID = dataset_plan.FrameOfReferenceUID
    dataset_dose.SOPInstanceUID = '1.2.3'
    dataset_dose.InstanceNumber = '123'

    dataset_dose.SOPClassUID = '1.2.840.10008.5.1.4.1.1.481.2'  # RT Dose Storage

    dataset_dose.StudyDate = dataset_ct.StudyDate
    dataset_dose.StudyTime = dataset_ct.StudyTime
    dataset_dose.AccessionNumber = dataset_ct.AccessionNumber
    dataset_dose.Modality = 'RTDOSE'
    dataset_dose.ReferringPhysicianName = dataset_ct.ReferringPhysicianName
    dataset_dose.StudyDescription = dataset_ct.StudyDescription
    dataset_dose.SeriesDescription = 'Doses from SNU_Dose_Engine'
    dataset_dose.PatientName = dataset_ct.PatientName
    dataset_dose.PatientID = dataset_ct.PatientID
    dataset_dose.PatientBirthDate = dataset_ct.PatientBirthDate
    dataset_dose.PatientBirthTime = dataset_ct.PatientBirthTime
    dataset_dose.PatientSex = dataset_ct.PatientSex
    dataset_dose.OtherPatientIDs = dataset_ct.OtherPatientIDs
    dataset_dose.StudyInstanceUID = dataset_ct.StudyInstanceUID
    dataset_dose.StudyID = dataset_ct.StudyID
    dataset_dose.BitsAllocated = 32
    dataset_dose.BitsStored = 32
    dataset_dose.HighBit = 31
    dataset_dose.SamplesPerPixel = 1
    dataset_dose.PhotometricInterpretation = 'MONOCHROME2'
    dataset_dose.PositionReferenceIndicator = ''
    dataset_dose.PixelRepresentation = 0

    # From Dose_Engine
    dataset_dose.DoseUnits = 'GY'
    dataset_dose.DoseType = 'EFFECTIVE'
    dataset_dose.DoseSummationType = 'BEAM'  # 'BEAM' 으로 하기로 함.
    dataset_dose.TissueHeterogeneityCorrection = 'IMAGE'
    dataset_dose.FrameIncrementPointer = dicom.values.convert_ATvalue(b'0\x04\x00\x0c', False)
    dataset_dose.ImageOrientationPatient = dataset_ct.ImageOrientationPatient

    # TEST VALUE 들로 채워둠.
    dataset_dose.ImagePositionPatient = [-80, -110, 66]  # float
    dataset_dose.SliceThickness = 3  # float
    dataset_dose.Rows = 9  # int
    dataset_dose.Columns = 9  # int
    dataset_dose.PixelSpacing = [25, 25]  # float
    dataset_dose.NumberOfFrames = 60  # int
    dataset_dose.GridFrameOffsetVector = []
    for i in range(dataset_dose.NumberOfFrames):
        dataset_dose.GridFrameOffsetVector.append(-i * float(dataset_dose.SliceThickness))
    dataset_dose.DoseGridScaling = 1000  # float

    dataset_dose.ReferencedRTPlanSequence = dicom.sequence.Sequence([dicom.dataset.Dataset()])
    dataset_dose.ReferencedRTPlanSequence[0].ReferencedSOPClassUID = dataset_plan.SOPClassUID
    dataset_dose.ReferencedRTPlanSequence[0].ReferencedSOPInstanceUID = dataset_plan.SOPInstanceUID
    dataset_dose.ReferencedStructureSetSequence = dataset_plan.ReferencedStructureSetSequence

    # Refereced Beam number 추가 해야함
    dataset_dose.ReferencedRTPlanSequence[0].ReferencedBeamSequence = dicom.sequence.Sequence([dicom.dataset.Dataset()])
    dataset_dose.ReferencedRTPlanSequence[0].ReferencedBeamSequence = dataset_plan.BeamSequence
    # dataset_plan.BeamNumber = dataset_plan.BeamSequence[0].BeamNumber

    block = dataset_dose.private_block(0x2819, "BNCTCOMPONENT", create=True)
    block.add_new(0x00, "CS", "BORONDOSE")
    block.add_new(0x01, "CS", "NORMAL")


    return dataset_dose



def main():
    PHITS_DOSE_PATH = "./PHITS2DICOM/BNCT_dose.out"
    RD_SAMPLE_PATH = "./Brain_CT/44254984/C1/RD.1.2.246.352.71.7.482169467.721183.20140127155500.dcm"
    CT_SAMPLE_PATH = "./Brain_CT/44254984/C1/CT.1.2.840.113704.1.111.428.1390280577.191.dcm"
    RD_OUTPUT_PATH = "./PHITS2DICOM/Boron.dcm"
    RP_SAMPLE_PATH = "./Brain_CT/44254984/C1/RP.1.2.246.352.71.5.482169467.300863.20140127145445.dcm"
    PHITS_VOXEL_INPUT = "./PHITS2DICOM/voxel.inp"

    '''
    for a in range(10):
        plt.subplot(3,4,a+1)
        plt.imshow(ds_flipped[a,], cmap=plt.cm.bone)
    plt.show()
    '''

    #rt_dose_changer(RD_SAMPLE_PATH,CT_SAMPLE_PATH, PHITS_DOSE_PATH, RD_OUTPUT_PATH)
    rt_dose_creator(CT_SAMPLE_PATH,RP_SAMPLE_PATH, PHITS_DOSE_PATH, RD_OUTPUT_PATH)

if __name__ == "__main__":
    main()
