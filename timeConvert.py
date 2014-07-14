# -*- coding: utf-8 -*-
"""
Created on Thu Jun  5 10:54:48 2014
Simple function to convert from the given time format to epoch time and then
to find and return the minute.  If string is not of proper format, return -1.
@author: meschke
"""
from time import mktime, strptime

def get_epoch_minute(str_time):
    try:
        #Set pattern for time format.        
        pattern = '%Y-%m-%d %H:%M:%S'
        #Calculate epoch time and return.        
        epoch = int(mktime(strptime(str_time, pattern)))
        return (epoch - epoch%60)
    #Return -1 if string is not properly formatted.    
    except ValueError:
        return -1
    
