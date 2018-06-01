#%% Libraries imported
import itk
import os
import sys
from StereoFlouroscopyRegistration.io.read_image import get_itk_image_type
import numpy as np
import scipy as sp
import scipy.stats
import dicom_functions as dfun
import numpy as np

#%% Read the dicom directory
in_dir_tstar = '/Volumes/Tashman Lab/Example Folder/Subject1/month1/Right/dicom_Tstar/'
in_dir_wats = '/Volumes/Tashman Lab/Example Folder/Subject1/month1/Right/dicom_wats/'
#%% Read the images in dicom directories
verbose = False
reader_wats = dfun.dicom_reader(in_dir_wats ,verbose) # reading the wats  dicom image
reader_tstar= dfun.dicom_reader(in_dir_tstar,verbose) # reading the tstar dicom image
#% getting the images
image_wats = reader_wats.GetOutput() # Getting the wats image
image_tstar= reader_tstar.GetOutput()# Getting the tstar image

#%% Get the details of the images.  

#%% Acquire the dictionary of the data
DictionaryType = itk.MetaDataDictionary
dictionary = image_wats.GetMetaDataDictionary()
