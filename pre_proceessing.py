import pydicom as dicom
import numpy as np
from PIL import Image, ImageDraw
import matplotlib.pyplot as plt
import csv


def make_mask(CP_S, organ, slice_number, ref_coor, pixel_resol):
    coor = np.array(CP_S[organ].ContourSequence[slice_number].ContourData)
    coor = coor.reshape(-1, 3)  # obtain coordinates for binary mask

    bm_coor = coor - ref_coor  # change mask coordinates into coordinates in real image
    bm_coor = bm_coor[:, :2]
    bm_coor = np.round(bm_coor / pixel_resol).astype(int)

    img = Image.new('L', (512, 512))
    draw = ImageDraw.Draw(img)
    points = []
    for i in range(0, len(bm_coor)): points.append(tuple(bm_coor[i]))
    points = tuple(points)
    draw.polygon((points), fill=1)
    img = np.array(img)
    return img


def make_data(PID, mask_list, RS_file):
    RS_file_name = PID + "/C1/" + RS_file
    RS = dicom.read_file(RS_file_name)

    num_mask = len(RS.StructureSetROISequence)  # Count number of masks
    RS.StructureSetROISequence[0]
    masks_name = []
    for it in range(0, num_mask):
        masks_name.append(RS.StructureSetROISequence[it].ROIName)

    CP_S = RS.ROIContourSequence

    mask_list -= 1  # Change the numbers of the mask into python index
    bladder = mask_list[0]
    rectum = mask_list[1]
    CTV_LF = mask_list[2]

    for organ in mask_list:  # For organs (bladder, rectum, prostate)

        ## Find real slices that matters (not inside contours)
        num_slices = len(CP_S[organ].ContourSequence)
        real_slices = np.zeros(num_slices)
        slice_looking_at = 0

        while slice_looking_at < num_slices - 1:
            coor = np.array(CP_S[organ].ContourSequence[slice_looking_at].ContourData)
            next_coor = np.array(CP_S[organ].ContourSequence[slice_looking_at + 1].ContourData)
            if coor[2] == next_coor[2]:  # The next slide is the same level as the one we are looking at
                real_slices[slice_looking_at] = 1
                real_slices[slice_looking_at + 1] = 2
                slice_looking_at += 2
            else:
                slice_looking_at += 1

        for slice_it in range(0, num_slices):  # For slices of the mask

            ### Read reference CT image of the mask and obtain useful informations ###
            UID = CP_S[organ].ContourSequence[slice_it].ContourImageSequence[0].ReferencedSOPInstanceUID
            split_string = UID.split('.')
            slice_code = split_string[-2] + "." + split_string[-1]

            file_name = PID + "/C1/CT." + UID + ".dcm"
            ref = dicom.read_file(file_name)
            pixel_resol = float(ref.PixelSpacing[0])
            ref_coor = ref.ImagePositionPatient  # obtain reference coordinate (CT image)
            ref_img = ref.pixel_array.astype(int)  # obtain reference CT image

            if real_slices[slice_it] == 0:
                img = make_mask(CP_S, organ, slice_it, ref_coor, pixel_resol)
            if real_slices[slice_it] == 1:
                img1 = make_mask(CP_S, organ, slice_it, ref_coor, pixel_resol)
                img2 = make_mask(CP_S, organ, slice_it + 1, ref_coor, pixel_resol)
                if np.max(img1 - img2) > 1:
                    img = img1 + img2
                else:
                    img = img1 - img2

            concat_img = np.concatenate((ref_img, img), axis=1)
            save_path = "files_npy/Segmentation/data/"
            save_file_name = "PID_" + PID + "_" + slice_code + "_"
            if int(PID) <= 44382269:
                save_folder = "train/"
            elif (int(PID) > 44382269) & (int(PID) <= 45141803):
                save_folder = "val/"
            else:
                save_folder = "test/"

            if organ == bladder:
                save_file_name = save_path + "bladder/" + save_folder + save_file_name + "bladder.npy"
            if organ == rectum:
                save_file_name = save_path + "rectum/" + save_folder + save_file_name + "rectum.npy"
            if organ == CTV_LF:
                save_file_name = save_path + "prostate/" + save_folder + save_file_name + "CTV_LF.npy"
            np.save(save_file_name, concat_img)


def main():
    with open('data_annotation.csv', mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            PID = row["PID"]
            RS_file = row["RS_file"]
            bladder = int(row["bladder"])
            rectum = int(row["rectum"])
            prostate = int(row["prostate"])
            mask_list = np.array([bladder, rectum, prostate])

            make_data(PID, mask_list, RS_file)
            print(PID)
            line_count += 1


if __name__ == "__main__":
    main()
