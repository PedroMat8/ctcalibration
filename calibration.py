#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb  7 21:48:42 2021

@author: fqb11104
"""
import os
import cv2
import numpy as np
import matplotlib.pyplot as plt

from scipy import optimize

def axial_sym(input_folder1, input_folder2, save,bit32, *interval):

    file_list1 = []
    file_list2 = []
    output_folder = 'output'

    for f in os.listdir(input_folder1):
        if f.endswith('.tif'):
            file_list1.append(f)
    else:
        for f in os.listdir(input_folder1):
            if f.endswith('.tiff'):
                file_list1.append(f)
    
    for f in os.listdir(input_folder2):
        if f.endswith('.tif'):
            file_list2.append(f)
    else:
        for f in os.listdir(input_folder2):
            if f.endswith('.tiff'):
                file_list2.append(f)
    
    file_list1.sort()
    file_list2.sort()

    foo = cv2.imread(input_folder1 + '/' + file_list1[0], -1)
    data1 = np.empty([len(file_list1), foo.shape[0], foo.shape[1]])
    data2 = np.empty([len(file_list2), foo.shape[0], foo.shape[1]])
    data1_bin = np.array([])
    data2_bin =np.array([])
    for i in range(len(file_list1)):
        data_file1 = input_folder1 + '/' + file_list1[i]
        data1[i,:,:] = cv2.imread(data_file1, -1)
        data1_bin = np.append(data1_bin,np.mean(data1[i,:,:]))
        
        data_file2 = input_folder2 + '/' + file_list2[i]
        data2[i,:,:] = cv2.imread(data_file2, -1)
        data2_bin = np.append(data2_bin, np.mean(data2[i,:,:]))

    data1_cal = []
    data2_cal = []
    z_cal = []
    for i_val in interval:
        delta = 0
        delta = min((i_val[1]-i_val[0]),(i_val[3]-i_val[2]))
        data1_cal = np.append(data1_cal, data1_bin[i_val[0]:i_val[0]+delta+1])
        data2_cal = np.append(data2_cal,data2_bin[i_val[2]:i_val[2]+delta+1])

    z_cal = np.arange(len(data1_cal))
    z_bin = np.arange(len(data1_bin))


    def new_intensity(par, d2):
        d2_new = par[0]*d2+par[1]
        return d2_new
    
    def offset(par, d1, d2):
        return np.sqrt((d1-new_intensity(par,d2))*(d1-new_intensity(par,d2)))
    
    wopt = optimize.least_squares(offset, [1,1],
                                  args = (data1_cal, data2_cal), bounds=([0,0],
                                     [np.inf,np.inf]), verbose=1)

    data_output = new_intensity(wopt.x, data2)

    if save:
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        os.chdir(output_folder)
        if bit32:
            data_output = np.float32(data_output)
        else:
            I = cv2.normalize(data_output, None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)
            data_output = np.uint8(I)

        count = 0
        
        for i in data_output:
            cv2.imwrite('new' + str(count)  + '.tif',i)
            count+=1
    
        os.chdir('..')
    
    fig = plt.figure()
    
    ax1 = fig.add_subplot(221)
    ax1.set_title('z profiles')
    ax1.plot(z_bin,data1_bin, label='reference')
    ax1.plot(z_bin,data2_bin, label='input')
    ax1.plot(z_bin,new_intensity(wopt.x, data2_bin), label='calibrated input')
    ax1.legend()
    
    ax2 = fig.add_subplot(222)
    ax2.set_title('Intervals')
    ax2.plot(z_cal,data1_cal, label='reference')
    ax2.plot(z_cal,data2_cal, label='input')
    ax2.plot(z_cal,new_intensity(wopt.x, data2_cal), label='calibrated input')
    ax2.legend()

    ax3 = fig.add_subplot(223)
    ax3.set_title('reference')
    ax3.imshow(data2[int(len(file_list1)/2),:,:])
    
    ax4 = fig.add_subplot(224)
    ax4.set_title('calibrated intput')
    ax4.imshow(data_output[int(len(file_list1)/2),:,:])

    return data_output


# 100 slices: without saving data 6.199060 s
# 100 slices: saving data 8.248467
# axial_sym('s1', 's2', True, True, [1,5,50,53],[7,14,60,66],[20,30,80,90])
