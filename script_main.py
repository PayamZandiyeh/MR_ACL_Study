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
import dicom_functions as dfun
import numpy as np
#%% inputs
input_dicom_mask_directory = '/Volumes/ms_orth-1/payam/color_image_representation/sub_1_aclr_m6/mask_binary/' # the name of directory to read the volume from
input_dicom_image_directory = '/Volumes/ms_orth-1/payam/color_image_representation/sub_1_aclr_m6/orig_image/' # the name of directory to read the volume from
output_directory = '/Users/pzandiyeh/Desktop/bob.nii' #'/Volumes/ms_orth/payam/color_image_representation/sub_1_aclr_m6/masked_image/'
force = True
verbose = True
write_vols = True  # Write the segmented volume to nifti
write_inp  = True # Writing the input dicom to nifti
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


    
#%% finding the min and max of the mask
InputImageType = itk.Image[itk.F,3] # Getting the pixel type
OutputImageType = itk.Image[itk.F,3] # Setting the output pixel type

MinMaxFilterType = itk.MinimumMaximumImageFilter[InputImageType] # initiate min-max image filter
minmaxfilter = MinMaxFilterType.New()
minmaxfilter.SetInput(mask)
minmaxfilter.Update()

low_thresh = minmaxfilter.GetMinimum()
up_thresh  = minmaxfilter.GetMaximum()
mid_thresh = (low_thresh+up_thresh)/2.0

# visual inspection and histogram assessment of the mask indicates that the mask region is located between low threshold to mid_threshold region. 

#%% converting the mask to binary


BinaryThresholdFilterType = itk.BinaryThresholdImageFilter[InputImageType,OutputImageType]
bwfilter = BinaryThresholdFilterType.New() # Setting the binary filter.
bwfilter.SetInput(maskReader.GetOutput()) # Setting the inputs of the filter.
bwfilter.SetOutsideValue(1) # setting the value for the outside the range.
bwfilter.SetInsideValue(0)  # Setting the value for the inside the range. 
bwfilter.SetLowerThreshold(low_thresh) # Setting the lower threshold of the bwfilter
bwfilter.SetUpperThreshold(mid_thresh) # Setting the upper threshold of the bwfilter
bwfilter.Update() # Update the filter 
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
seg_vol = itk.GetImageFromArray(masked_image_array)

#%% write the masked region image 3d to the desired location. 
if write_inp:
    itk.imwrite(image,input_dicom_image_directory+'orig_image.nii') # write the original image
    itk.imwrite(mask,input_dicom_mask_directory+'mask_binary.nii') # write the binary mask
    
if write_vols:
    itk.imwrite(seg_vol,output_directory+'masked_image.nii') # Write the segmented volume inside the desired location.



