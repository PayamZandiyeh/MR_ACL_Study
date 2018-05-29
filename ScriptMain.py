#%% The purpose of this code is to load an MR image: 
    # 1. Apply a mask to it.
    # 2. Take the average of the area within the mask. 

#%% Libraries
import itk
import sys

#%% Describing the details of the images and the image types

verbose = True # provides details of every step

input_filename = '' # The address of the input file. 
input_mask     = '' # The address to the desired mask. 

InputPixelType = itk.ctype("short")
DimensionIn  = 3

InputImageType  = itk.Image[InputPixelType , DimensionIn ]

ReaderType = itk.ImageFileReader[InputImageType]
reader     = ReaderType.New()

#%% Reading the original image

reader.SetFileName(input_filename)

try:
    print("Reading image: " + input_filename)
    reader.Update()
    print("Image Read Successfully")
except ValueError: 
    print("ERROR: ExceptionObject cauth! \n")
    print(ValueError)
    sys.exit()
    
inputImage = reader.GetOutput()

if verbose :
    print("The input image's details:")
    print(inputImage)

#%% Reading the mask image
reader.SetFileName(input_mask)

try:
    print("Reading image: " + input_mask)
    reader.Update()
    print("Image Read Successfully")
except ValueError: 
    print("ERROR: ExceptionObject cauth! \n")
    print(ValueError)
    sys.exit()
    
inputMask = reader.GetOutput()

if verbose :
    print("The input Mask: ")
    print(inputMask)

#%% Applying the mask to the image
MaskFilterType = itk.MaskImageFilter[InputImageType,InputImageType]
maskFilter = MaskFilterType.New()









































