#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 22 14:51:42 2018

@author: markhigger
"""
import PreProc_MatFun_Wraps as Wrap
import os

def preProc(fileFull_input, fileDir_output):
    #get base file names and directories, currntly only works for unix dirs
    fileParts_input = fileFull_input.split('/')
    fileDir_input = '/'.join(fileParts_input[0:-1]) + '/'
    fileName_input = fileParts_input[-1] #input file with extension
    fileName_base = '.'.join(fileName_input.split('.')[0:-1]) #input file w/o extension
    
    #set output directory equal to input directory if not specified
    if fileDir_output == None:
        fileDir_output = fileDir_input
    
    #calculate file names in input directory s
    fileName_raw = fileDir_input + fileName_base + '.eeg'
    fileName_set = fileDir_input + fileName_base + '.set'
    
    #calculate file names in output file directory
    fileName_bandpass = fileDir_output + fileName_base + '_bandpass.set'
    fileName_notch = fileDir_output + fileName_base + '_notch.set'
    fileName_bcg = fileDir_output + fileName_base + '_bcg.set'
    fileName_resample = fileDir_output + fileName_base + '_resample.set'
    
    #check if files exist to compute what processing needs to be done
    FileExists_set = os.path.exists(fileName_set) 
    FileExists_bandpass = os.path.isfile(fileName_bandpass)
    FileExists_notch = os.path.isfile(fileName_notch)
    FileExists_bcg = os.path.isfile(fileName_bcg)
    FileExists_resample = os.path.isfile(fileName_resample)
    #Check which processing needs to be done, skip Processing if a file exits where
    #   Processing or any Processing after exists
    skip_resample = FileExists_resample
    skip_bcg = FileExists_bcg or skip_resample
    skip_notch = FileExists_notch or skip_bcg
    skip_bandpass = FileExists_bandpass or skip_notch
    skip_set = FileExists_set or skip_bandpass
    
    
    #initialize matlab runtime compiler with preprocessor functions
    Funs = Wrap.init()
    
    #convert brainvision data to 
    if skip_set:
        print('set file already exists, skiping creation of set file')
    else:
        Wrap.BV2Set(Funs, fileName_raw)
    
    #Run EEG through Bandpass filter - uses forward-backward butterworth iir bandpass
    if skip_bandpass:
        print('bandpass filter already appled')
    else:
        Flow = 0.5 #low cuttoff at 0.5 Hz
        Fhigh = 70 #high cutoff at 70 Hz
        N = 2 #use second order filter 
        Wrap.Bandpass_Mat(Funs, fileName_set, fileName_bandpass, Flow, Fhigh, N)
    
    #Run EEG through Notch filter - uses forward-backward butterworth iir bandstop
    if skip_notch:
        print('Notch filter already applied')
    else:
        Fn = 60 #Notch filter at 60Hz
        Fw = 4 #Notch width of 4Hz
        N = 2 #use second order bandstop
        Wrap.Notch_Mat(Funs, fileName_bandpass, fileName_notch, Fn, Fw, N)
    
    #Run EEG through PA removal 
    if skip_bcg:
    	print('bcg already removed')
    else:
    	Wrap.PA_Removal(Funs, fileName_notch, fileName_bcg)

    #Resample EEGs
    if skip_resample:
    	print('already resampled')
    else:
    	Wrap.Resample_Mat(Funs, fileName_bcg, fileName_resample)    
    #terminate matlab runtime compiler
    Wrap.term(Funs)

#fileDir_input = '/home/mhigger/Desktop/EEG_Data/20181115/Raw/'

filePaths_input = []
#filePaths_input.append(fileDir_input + 'EEG_fMRI_20181115_0001_ET12_75_75_02_02_passive.eeg')
#filePaths_input.append(fileDir_input + 'EEG_fMRI_20181115_0002_ET12_75_75_05_05_passive.eeg')
#filePaths_input.append(fileDir_input + 'EEG_fMRI_20181115_0003_ET12_75_75_10_10_passive.eeg')
#filePaths_input.append(fileDir_input + 'EEG_fMRI_20181115_0004_ET12_75_75_05_02_passive.eeg')
#filePaths_input.append(fileDir_input + 'EEG_fMRI_20181115_0006_ET12_Rest.eeg')
#filePaths_input.append(fileDir_input + 'EEG_fMRI_20181115_0005_ET12_75_75_02_05_passive.eeg')
#filePaths_input.append(fileDir_input + 'EEG_fMRI_20181115_0007_Checkerboard.eeg')

#files for 20181128 
fileDir_input = '/home/mhigger/Desktop/EEG_Data/20181128/Raw/'
filePaths_input.append(fileDir_input + 'EEG_fMRI_20181128_001_Checkerboard_Outside.eeg')
#filePaths_input.append(fileDir_input + 'EEG_fMRI_20181128_002_Checkerboard_Scanner_ON.eeg')
#filePaths_input.append(fileDir_input + 'EEG_fMRI_20181128_003_Rest.eeg')
#filePaths_input.append(fileDir_input + 'EEG_fMRI_20181128_004_ThePresent.eeg')
#filePaths_input.append(fileDir_input + 'EEG_fMRI_20181128_005_Inscapes')
#filePaths_input.append(fileDir_input + 'EEG_fMRI_20181128_006_Monkey1.eeg')
#filePaths_input.append(fileDir_input + 'EEG_fMRI_20181128_007_DespicableMe.eeg')
#filePaths_input.append(fileDir_input + 'EEG_fMRI_20181128_008_Monkey1_02.eeg')
#filePaths_input.append(fileDir_input + 'EEG_fMRI_20181128_009_Inscapes_02.eeg')
#filePaths_input.append(fileDir_input + 'EEG_fMRI_20181128_010_ThePresent_02.eeg')
#filePaths_input.append(fileDir_input + 'EEG_fMRI_20181128_011_DespicableMe_02.eeg')

#filePaths_input.append(fileDir_input +s 'EEG_fMRI_20180830_06_Checkerboard_Flash_Inside.eeg')
#fileFull_input = '/home/mhigger/Desktop/EEG_data/EEG_fMRI_20180822_0001_Checkerboard_02.eeg'
fileDir_output = '/home/mhigger/Desktop/EEG_Data/20181128/Processed/'
#fileDir_output = '/home/mhigger/Desktop/EEG_Data/20181115/Processed/'
for filepath in filePaths_input:
	print(filepath)
	preProc(filepath, fileDir_output)


