import pydicom as dicom
import numpy as np
from PIL import Image, ImageDraw
import matplotlib.pyplot as plt
import csv
import os
import datetime


def rt_dose_changer(sample_rt_dose, dose_results, output_rt_dose):
    f = open(dose_results, 'r')
    read_all = f.read()
    f.close()

    # is it necessary ?
    read_all = read_all.replace("[", "")
    read_all = read_all.replace("]", "")
    read_all = read_all.split()

    array_dose = np.array(read_all)
    array_dose = np.reshape(array_dose, (60, 9, 9))

    ds = dicom.dcmread(sample_rt_dose)

    # TODO dose normalization 고민해봐야함.
    # Pixel data 교환.
    array_dose = np.float32(array_dose)
    ds.DoseGridScaling = np.min(array_dose)
    array_dose = array_dose / np.min(array_dose)  # dose 수치 조절.
    array_dose = np.uint32(array_dose)
    ds.PixelData = array_dose.tobytes()

    ds.Rows, ds.Columns = array_dose.shape[2], array_dose.shape[1]
    ds.NumberOfFrames = 60
    ds.GridFrameOffsetVector = []
    for i in range(ds.NumberOfFrames):
        ds.GridFrameOffsetVector.append(i * 3)
    if ds.DVHSequence:
        del ds.DVHSequence

    # only for the observation
    ds.PixelSpacing = [25, 25]

    dicom.filewriter.dcmwrite(output_rt_dose, ds, write_like_original=True)


def rt_dose_creator(ct_images, rt_plan, dose_results, output_rt_dose):
    ds_ct = dicom.dcmread(ct_images)
    ds_plan = dicom.dcmread(rt_plan)
    f = open(dose_results, 'r')
    read_all = f.read()
    f.close()

    ds_dose = rt_dose_header_setup(ds_ct, ds_plan, output_rt_dose)

    # ds_dose.save_as("test11.dcm")
    # TODO 몇몇 상수들은 dose_results(계산결과) 에서 불러오는 것이 좋을듯
    # TODO dose data 변환 후 입력.
    read_all = read_all.replace("[", "")
    read_all = read_all.replace("]", "")
    read_all = read_all.split()
    array_dose = np.array(read_all)
    array_dose = np.reshape(array_dose, (60, 9, 9))


    # TODO dose normalization 고민해봐야함.
    # Pixel data 교환.
    array_dose = np.float32(array_dose)
    ds_dose.DoseGridScaling = np.min(array_dose)
    array_dose = array_dose / np.min(array_dose)  # dose 수치 조절.
    array_dose = np.uint32(array_dose)

    ds_dose.PixelData = array_dose.tobytes()

    #ds_dose.pixel_array = array_dose

    # dicom.filewriter.dcmwrite(output_rt_dose, ds_dose, write_like_original=True)

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

    return dataset_dose


def add_private():
    pass
    # TODO private tag 넣기..


def main():
    # TODO 인풋파일 path 정리하는 함수 필요.
    CT_path = "./Brain_CT/42860819/C1/CT.1.2.840.113704.1.111.5956.1407919894.5141.dcm"
    RP_path = "./Brain_CT/42860819/C1/RP.1.2.246.352.71.5.482169467.351676.20140814101105.dcm"
    RD_path = "./Brain_CT/42860819/C1/RD.1.2.246.352.71.7.482169467.884472.20140818115809.dcm"
    output_RD_path = "./Brain_CT/42860819/C1_changed/RT_dose_changed.dcm"
    calc_results = "B_dose.txt"

    #    rt_dose_changer(RD_path, calc_results, output_RD_path)
    rt_dose_creator(CT_path, RP_path, calc_results, output_RD_path)


if __name__ == "__main__":
    main()
