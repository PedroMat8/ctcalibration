#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Working example:
    
Given 2 tif sequences of at least 100 slices each.
The reference sequence is stored in a folder named: s1
The other sequence is stored in a folder named: s2
"""


import calibration as cal

# single interval, saving 32bit
data_output = cal.axial_sym('s1', 's2', True, True, [1,100,1,100])

# # single interval, saving 8bit
# data_output = cal.axial_sym('s1', 's2', True, False, [1,100,1,100])

# # single interval without saving
# data_output = cal.axial_sym('s1', 's2', False, True, [1,100,1,100])

# # multiple interval, saving 32bit
# data_output = cal.axial_sym('s1', 's2', True, True, [1,50,1,50], [70,100,70,100])
