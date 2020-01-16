import pydicom as dicom
from pydicom.dataset import Dataset, FileDataset
import os
import numpy as np
from PIL import Image


def copyCTtoRTDose(self, path, ds, doseData, imageRow, imageCol, sliceCount, dgs):

    # Create a RTDose file for broadcasting.
    file_meta = Dataset()
    file_meta.MediaStorageSOPClassUID = '1.2.840.10008.5.1.4.1.1.481.2' # RT Dose Storage
    # Needs valid UID
    file_meta.MediaStorageSOPInstanceUID = ds.file_meta.MediaStorageSOPInstanceUID
    file_meta.ImplementationClassUID = ds.file_meta.ImplementationClassUID

    #create DICOM RT-Dose object.
    rtdose = FileDataset(path + '/rtdose.dcm', {}, file_meta=file_meta, preamble="\0"*128)

    #No DICOM object standard. Use only required to avoid errors with viewers.
    rtdose.SOPInstanceUID = ds.SOPInstanceUID
    rtdose.SOPClassUID = '1.2.840.10008.5.1.4.1.1.481.2'
    rtdose.file_meta.TransferSyntaxUID = ds.file_meta.TransferSyntaxUID
    rtdose.PatientsName = ds.PatientsName
    rtdose.PatientID = ds.PatientID
    rtdose.PatientsBirthDate = ds.PatientsBirthDate
    #Crashed caused if no sex.
    try:
        rtdose.PatientsSex = ds.PatientsSex
    except:
        rtdose.PatientsSex, ds.PatientsSex = 'O', 'O'
        self.data.update({'images':ds})

    rtdose.StudyDate                  = ds.StudyDate
    rtdose.StudyTime                  = ds.StudyTime
    rtdose.StudyInstanceUID           = ds.StudyInstanceUID
    rtdose.SeriesInstanceUID          = ds.SeriesInstanceUID
    rtdose.StudyID                    = ds.StudyID
    rtdose.SeriesNumber               = ds.SeriesNumber
    rtdose.Modality                   = 'RTDOSE'
    rtdose.ImagePositionPatient       = ds.ImagePositionPatient
    rtdose.ImageOrientationPatient    = ds.ImageOrientationPatient
    rtdose.FrameofReferenceUID        = ds.FrameofReferenceUID
    rtdose.PositionReferenceIndicator = ds.PositionReferenceIndicator
    rtdose.PixelSpacing               = ds.PixelSpacing
    rtdose.SamplesperPixel            = 1
    rtdose.PhotometricInterpretation  = 'MONOCHROME2'
    rtdose.NumberofFrames             = sliceCount
    rtdose.Rows                       =  imageRow
    rtdose.Columns                    = imageCol
    rtdose.BitsAllocated              = 32
    rtdose.BitsStored                 = 32
    rtdose.HighBit                    = 31
    rtdose.PixelRepresentation        = 0
    rtdose.DoseUnits                  = 'GY'
    rtdose.DoseType                   = 'PHYSICAL'
    rtdose.DoseSummationType          = 'FRACTION'
    #In case spaceing tag is missing.
    if not ds.has_key('SpacingBetweenSlices'):
        ds.SpacingBetweenSlices = ds.SliceThickness
    #Ensure patient pos is on "Last slice".
    if fnmatch.fnmatch(ds.PatientPosition, 'FF*'):
        #For compliance with dicompyler update r57d9155cc415 which uses a reverssed slice ordering.
        doseData = doseData[::-1]
        rtdose.ImagePositionPatient[2] = ds.ImagePositionPatient[2]
    elif fnmatch.fnmatch(ds.PatientPosition, 'HF*'):
        rtdose.ImagePositionPatient[2] = ds.ImagePositionPatient[2] - (sliceCount-1)*ds.SpacingBetweenSlices
    #Create Type A(Relative) GFOV.
    rtdose.GridFrameOffsetVector = list(np.arange(0., sliceCount*ds.SpacingBetweenSlices,ds.SpacingBetweenSlices))
    #Scaling from int to physical dose
    rtdose.DoseGridScaling = dgs

    #Store images in pixel_array(int) & Pixel Data(raw).
    rtdose.pixel_array = doseData
    rtdose.PixelData   = doseData.tostring()

    #Tag required by dicompyler.
    plan_meta = Dataset()
    rtdose.ReferencedRTPlans = []
    rtdose.ReferencedRTPlans.append([])
    rtdose.ReferencedRTPlans[0] = plan_meta
    rtdose.ReferencedRTPlans[0].ReferencedSOPClassUID = 'RT Plan Storage'
    rtdose.ReferencedRTPlans[0].ReferencedSOPInstanceUID = ds.SOPInstanceUID


    return rtdose