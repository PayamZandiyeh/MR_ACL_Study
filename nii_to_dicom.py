#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 15 11:54:50 2018

@author: pzandiyeh
"""
import itk,sys
verbose = True

input_dicom_directory = '/Volumes/ms_orth-4/payam/prepared_for_code_analysis/wats_mid/mask/'
output_dicom_directory= '/Users/pzandiyeh/Desktop/testDicom/'

PixelType = itk.F
Dimension = 3
ImageType = itk.Image[PixelType,Dimension]
ReaderType= itk.ImageSeriesReader[ImageType]

ImageIOType = itk.GDCMImageIO
NamesGeneratorType = itk.GDCMSeriesFileNames

gdcmIO = ImageIOType.New()
namesGenerator = NamesGeneratorType.New()
namesGenerator.SetInputDirectory(str(input_dicom_directory))
namesGenerator.SetGlobalWarningDisplay(False)
namesGenerator.SetUseSeriesDetails(True)
inputFileNames = namesGenerator.GetInputFileNames()

#%% Setting up the reader
reader = ReaderType.New()
reader.SetImageIO(gdcmIO)
reader.SetFileNames(inputFileNames)

try:
    print("in progress ... May take few seconds")
    reader.Update()
    print("Image Read Successfully")
except ValueError: 
    print("ERROR: ExceptionObject cauth! \n")
    print(ValueError)
    sys.exit()

#%% Setting up the writer
OutputPixelType = itk.F
OutputDimension = 2
OutputImageType = itk.Image[OutputPixelType,OutputDimension]
SeriesWriterType = itk.ImageSeriesWriter[ImageType,OutputImageType]

seriesWriter = SeriesWriterType.New()
seriesWriter.SetImageIO(gdcmIO)
seriesWriter.SetInput(reader.GetOutput())
namesGenerator.SetOutputDirectory(output_dicom_directory)
seriesWriter.SetFileNames(inputFileNames)

seriesWriter.SetMetaDataDictionary(reader.GetMetaDataDictionary())

try:
    print("in progress ... May take few seconds")
    seriesWriter.Update()
    print("Image wrote Successfully")
except ValueError: 
    print("ERROR: ExceptionObject cauth! \n")
    print(ValueError)
    sys.exit()