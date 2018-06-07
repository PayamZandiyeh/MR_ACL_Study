#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed May 30 11:23:54 2018

@author: Payam

This script will order all the DICOM images in <input_dicom_directory>
    into an image stack and write the data out as another image type as
    specified by the extension of <output_file_name>.

    If the flag <force> is set, the script does not check if the output exists.
    Instead, it overwrites the data if it is there.

    If the flag <verbose> is set, the script will print every DICOM file it finds.

    Typically, this can be used for converting to .nii.gz.

    This script is largely based off the ITK example Read DICOM Series and Write 3D Image 
    """
#%% import the libraries

import itk
from StereoFlouroscopyRegistration.io.read_image import get_itk_image_type
import dicom_functions as dfun
import numpy as np
#%% inputs
input_dicom_mask_directory = "/Volumes/ms_orth/example_1/SegmentedVolume" # the name of directory to read the volume from
input_dicom_image_directory = "/Volumes/ms_orth/example_1/OriginalVolume_ver1" # the name of directory to read the volume from

output_file_name = "/Volumes/Storage/Payam/Desktop/seg_vol.nii" # The output image location.
force = True
verbose = True
#%% reading the dicom image
maskReader  = dfun.dicom_reader(input_dicom_directory=input_dicom_mask_directory,verbose=verbose) # get the image pointer
imageReader = dfun.dicom_reader(input_dicom_directory=input_dicom_image_directory,verbose=verbose) # get the image pointer
#%% printing the information of the image and mask
if verbose:
    print("Mask Information: \n") 
    print(maskReader)
    print("\n\n\n\n\n\n\n")
    print("Original Volume Information: \n")
    print(imageReader)
mask = maskReader.GetOutput()
image= imageReader.GetOutput()

#%% converting the mask to binary
InputImageType = itk.Image[itk.F,3] # Getting the pixel type
OutputImageType = itk.Image[itk.F,3] # Setting the output pixel type

BinaryThresholdFilterType = itk.BinaryThresholdImageFilter[InputImageType,OutputImageType]
bwfilter = BinaryThresholdFilterType.New() # Setting the binary filter.
bwfilter.SetInput(maskReader.GetOutput()) # Setting the inputs of the filter.
bwfilter.SetOutsideValue(0) # setting the value for the outside the range
bwfilter.SetInsideValue(1)
bwfilter.SetLowerThreshold(700)
bwfilter.SetUpperThreshold(800)
bwfilter.Update()
#%% Apply the mask to the image
buff = itk.GetArrayFromImage(bwfilter.GetOutput()) # Casting the image pixels to a numpy array
bwfilter_array = buff.copy() # getting the image into a matrix format. 

buff = itk.GetArrayFromImage(imageReader.GetOutput())
image_array = buff.copy() # getting a copy of the image into a matrix format. 

masked_image_array = np.multiply(image_array,bwfilter_array) # multiply the image with the mask
#%% Calculate the image statistics
data = image_array[np.nonzero(bwfilter_array)] # select the non-zero elements of the 

output_mean,output_ci_low,output_ci_up = dfun.mean_confidence_interval(data)
output_std  = np.std(data )
output_min  = np.min(data )
output_max  = np.max(data )

output = [output_mean,output_std,output_min,output_max,output_ci_low,output_ci_up] # confidence interval doesn't make sense

#%% Convert the images back to an itk image.
image2 = itk.GetImageFromArray(masked_image_array)

#%% Apply the image mask to an image. 
InputImageType = dfun.get_itk_image_type(imageReader.GetFileNames()[0])
MaskFilterType = itk.MaskImageFilter[InputImageType,InputImageType,InputImageType]
maskFilter = MaskFilterType.New()

maskFilter.SetInput(imageReader.GetOutput())
maskFilter.SetMaskImage(maskReader.GetOutput())

#%% Apply the negative image filter to see if this works

#%% Write out
final_image = maskFilter.GetOutput()# the image to be written


print('Writing to {}'.format(output_file_name))
itk.imwrite(final_image, str(output_file_name))
print('finished')