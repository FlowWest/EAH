#!/usr/bin/env python
import bisect
import pandas as pd
import numpy as np
import os
import eah_constants

def find_ge(a, x):
    'Find leftmost item greater than or equal to x'
    i = bisect.bisect_left(a, x)
    if i != len(a):
        return a[i]
    raise ValueError

def find_le(a, x):
    'Find rightmost value less than or equal to x'
    i = bisect.bisect_right(a, x)
    if i:
        return a[i-1]
    raise ValueError
    
def find_nearest(a, x):
    i = (np.abs(a-x)).argmin()
    return a[i]

def main(verbose, ann_peak, hydrology, odir, smo=1, sda=1, emo=1, eda=1, duration=1):

    head, tail = os.path.split(hydrology)
    hname = tail.split('.')[0]
    sep = os.path.sep

    # read input file into data frame object
    #input_file = odir + sep + hname + '_'  + str(duration) + '_day_' + str(smo) + '_' + str(sda) + '_to_' + str(emo) + '_' + str(eda) + '_peaks.csv'
    #ann_peak = pd.read_csv(input_file, sep=',', names=["year","start_date","end_date","peak_cfs"], header=0, parse_dates=True)
    
    # create log pearson distribution

    # sort peak flows in descending order
    lp = ann_peak.sort_values(by=['peak_cfs'], ascending=False)
    lpgroup = lp.groupby('peak_cfs').size()
    zero_count = 0
    if 0.0 in lpgroup.index:
        zero_count = lpgroup.loc[0.0]
    print "COUNT OF NUMBER OF YEARS WITH ZERO FLOW (cfs)", zero_count
    
    # drop any rows with zero values 
    # NOTE TAKING OUT FOR YOLO BYPASS STUDIES, would like to keep years with no flow
    lp = lp[(lp.peak_cfs != 0)] 
    if len(lp.index) < 10:
        print "ERROR: INSUFFICIENT DATA RECORD TO CREATE LOG PEARSON DISTRIBUTION FOR DURATION OF " + str(duration) + " days\n" 

    # create column for log of each peak flow
    lp['log_q'] = np.log10(lp['peak_cfs'])

    # calculate average of peak flows
    average_q = lp['peak_cfs'].mean()

    # calculate average of log of peak flows
    average_log_q = lp['log_q'].mean()
    
    # create column for {{log q - avg(log q))^2}    
    lp['square_dif'] = ((lp['log_q'] - average_log_q)**2)      

    # create column for {{log q - avg(log q))^3}
    lp['cube_dif'] = ((lp['log_q'] - average_log_q)**3)

    # create column for rank
    lp['rank'] = lp['peak_cfs'].rank(method='first', ascending=False)
    #lp['rank'] = lp['peak_cfs'].rank(method='average', ascending=False)

    # calculate number of records
    num_records = len(lp.index)
 
    # create column for return period (Tr)
    lp['tr'] = (num_records + 1) / lp['rank'] 

    # create column for exceedance probability {1/Tr}
    lp['exceed_pr'] = 1 / lp['tr']

    # calculate sum of {{log q - avg(log q))^2} column   
    sum_square_dif = lp['square_dif'].sum()

    # calculate sum of {{log q - avg(log q))^3} column
    sum_cube_dif = lp['cube_dif'].sum()

    # calculate variance of log of peak flows
    var_log_q = lp['log_q'].var()

    # calculate standard deviation of log of peak flows
    std_log_q = lp['log_q'].std()
    
    # calculate skew of log of peak flows
    skew_log_q = lp['log_q'].skew()

    #     regional skew coefficient 
    cm = 0.3
   
    #     variance of regional skewness
    var_cm = 0.302
 
    #     A
    A = 0.33 + (0.08 * skew_log_q)

    #     B
    B = 0.94 - (0.26 * skew_log_q)

    #     variance of station skewness
    var_cs = 10 ** (A - B * (np.log (num_records / 10)))

    #     weighting factor 
    W = var_cm / (var_cm + var_cs)

    # calculate weighted skewness
    cw = W * skew_log_q + (1 - W) * cm
    
    # read frequency factor table into data frame object
    #freq = pd.read_csv('frequency.csv', sep=',', index_col=0, names=["Cs","1.0101","2","5","10","25","50","100","200"], header=0)
    findex = [3.0,2.9,2.8,2.7,2.6,2.5,2.4,2.3,2.2,2.1,2.0,1.9,1.8,1.7,1.6,1.5,1.4,1.3,1.2,1.1,1.0,0.9,0.8,0.7,0.6,0.5,0.4,0.3,0.2,0.1,0,-0.1,-0.2,-0.3,-0.4,-0.5,-0.6,-0.7,-0.8,-0.9,-1.0,-1.1,-1.2,-1.3,-1.4,-1.5,-1.6,-1.7,-1.8,-1.9,-2.0,-2.1,-2.2,-2.3,-2.4,-2.5,-2.6,-2.7,-2.8,-2.9,-3.0]
    fnames = eah_constants.eah_interval_string
    fdata = {'1.0101': [-0.667,-0.69,-0.714,-0.74,-0.769,-0.799,-0.832,-0.867,-0.905,-0.946,-0.99,-1.037,-1.087,-1.14,-1.197,-1.256,-1.318,-1.383,-1.449,-1.518,-1.588,-1.66,-1.733,-1.806,-1.88,-1.955,-2.029,-2.104,-2.178,-2.252,-2.326,-2.4,-2.472,-2.544,-2.615,-2.686,-2.755,-2.824,-2.891,-2.957,-3.022,-3.087,-3.149,-3.211,-3.271,-3.33,-3.88,-3.444,-3.499,-3.553,-3.605,-3.656,-3.705,-3.753,-3.8,-3.845,-3.899,-3.932,-3.973,-4.013,-4.051
],
             '2.0': [-0.396,-0.39,-0.384,-0.376,-0.368,-0.36,-0.351,-0.341,-0.33,-0.319,-0.307,-0.294,-0.282,-0.268,-0.254,-0.24,-0.225,-0.21,-0.195,-0.18,-0.164,-0.148,-0.132,-0.116,-0.099,-0.083,-0.066,-0.05,-0.033,-0.017,0,0.017,0.033,0.05,0.066,0.083,0.099,0.116,0.132,0.148,0.164,0.18,0.195,0.21,0.225,0.24,0.254,0.268,0.282,0.294,0.307,0.319,0.33,0.341,0.351,0.36,0.368,0.376,0.384,0.39,0.396
],
             '5.0': [0.42,0.44,0.46,0.479,0.499,0.518,0.537,0.555,0.574,0.592,0.609,0.627,0.643,0.66,0.675,0.69,0.705,0.719,0.732,0.745,0.758,0.769,0.78,0.79,0.8,0.808,0.816,0.824,0.83,0.836,0.842,0.846,0.85,0.853,0.855,0.856,0.857,0.857,0.856,0.854,0.852,0.848,0.844,0.838,0.832,0.825,0.817,0.808,0.799,0.788,0.777,0.765,0.752,0.739,0.725,0.711,0.696,0.681,0.666,0.651,0.636
],
             '10.0': [1.18,1.195,1.21,1.224,1.238,1.25,1.262,1.274,1.284,1.294,1.302,1.31,1.318,1.324,1.329,1.333,1.337,1.339,1.34,1.341,1.34,1.339,1.336,1.333,1.328,1.323,1.317,1.309,1.301,1.292,1.282,1.27,1.258,1.245,1.231,1.216,1.2,1.183,1.166,1.147,1.128,1.107,1.086,1.064,1.041,1.018,0.994,0.97,0.945,0.92,0.895,0.869,0.844,0.819,0.795,0.711,0.747,0.724,0.702,0.681,0.66
],
             '25.0': [2.278,2.277,2.275,2.272,2.267,2.262,2.256,2.248,2.24,2.23,2.219,2.207,2.193,2.179,2.163,2.146,2.128,2.108,2.087,2.066,2.043,2.018,1.993,1.967,1.939,1.91,1.88,1.849,1.818,1.785,1.751,1.716,1.68,1.643,1.606,1.567,1.528,1.488,1.448,1.407,1.366,1.324,1.282,1.24,1.198,1.157,1.116,1.075,1.035,0.996,0.959,0.923,0.888,0.855,0.823,0.793,0.764,0.738,0.712,0.683,0.666
],
             '50.0': [3.152,3.134,3.114,3.093,3.071,3.048,3.023,2.997,2.97,2.942,2.912,2.881,2.848,2.815,2.78,2.743,2.706,2.666,2.626,2.585,2.542,2.498,2.453,2.407,2.359,2.311,2.261,2.211,2.159,2.107,2.054,2,1.945,1.89,1.834,1.777,1.72,1.663,1.606,1.549,1.492,1.435,1.379,1.324,1.27,1.217,1.166,1.116,1.069,1.023,0.98,0.939,0.9,0.864,0.83,0.798,0.768,0.74,0.714,0.689,0.666
],
             '100.0':[4.051,4.013,3.973,3.932,3.889,3.845,3.8,3.753,3.705,3.656,3.605,3.553,3.499,3.444,3.388,3.33,3.271,3.211,3.149,3.087,3.022,2.957,2.891,2.824,2.755,2.686,2.615,2.544,2.472,2.4,2.326,2.252,2.178,2.104,2.029,1.955,1.88,1.806,1.733,1.66,1.588,1.518,1.449,1.383,1.318,1.256,1.197,1.14,1.087,1.037,0.99,0.946,0.905,0.867,0.832,0.799,0.769,0.74,0.714,0.69,0.667
],
             '200.0':[4.97,4.904,4.847,4.783,4.718,4.652,4.584,4.515,4.444,4.372,4.298,4.223,4.147,4.069,3.99,3.91,3.828,3.745,3.661,3.575,3.489,3.401,3.312,3.223,3.132,3.041,2.949,2.856,2.763,2.67,2.576,2.482,2.388,2.294,2.201,2.108,2.016,1.926,1.837,1.749,1.664,1.581,1.501,1.424,1.351,1.282,1.216,1.155,1.097,1.044,0.995,0.949,0.907,0.869,0.833,0.8,0.769,0.741,0.714,0.69,0.667
]}    

    freq = pd.DataFrame(fdata, findex, fnames)
    #freq = freq.dropna()
    keys = findex
    keys.sort()

    dist_columns = eah_constants.dist_columns
    logP_dist = pd.DataFrame(columns=dist_columns)
    logP_dist = logP_dist.fillna(0)

    Tr = eah_constants.eah_interval_string
    # find lower and upper K values based on station skew coefficient value
    
    # 10/16/14 WARNING may need to revise binary search g beyond boundary skew_log_q = round(skew_log_q,1)
    low_index = round(find_le(keys, skew_log_q),2)
    high_index = round(find_ge(keys, skew_log_q),2)

    
    # populate log Pearson distribution table
    for interval in Tr:
         logP_dist.ix[interval,'Klow'] = freq.loc[low_index][interval]
         logP_dist.ix[interval,'Khigh'] = freq.loc[high_index][interval]
         logP_dist.ix[interval,'slope'] = (logP_dist.loc[interval,'Khigh'] - logP_dist.loc[interval,'Klow']) / (high_index - low_index) 
         logP_dist.ix[interval,'Kint'] = logP_dist.loc[interval,'Klow'] + (logP_dist.loc[interval,'slope'] * (skew_log_q - low_index))
         # logP_dist.loc[interval,'Kint'] = logP_dist.loc[interval,'Klow'] + ((logP_dist.loc[interval,'slope']/(high_index - low_index)) * skew_log_q)
         logP_dist.ix[interval,'logQ'] = average_log_q + logP_dist.loc[interval, 'Kint'] * std_log_q
         logP_dist.ix[interval,'Q'] = 10 ** logP_dist.loc[interval,'logQ']
  
    if verbose == True:
         output_lp_csv = odir + sep + hname + '_' + str(duration) + '_day_' + str(smo) + '_' + str(sda) + '_to_' + str(emo) + '_' + str(eda) + '_rank.csv'
         output_dist_csv = odir + sep + hname + '_' + str(duration) + '_day_' + str(smo) + '_' + str(sda) + '_to_' + str(emo) + '_' + str(eda) + '_lp.csv'
         lp.to_csv(output_lp_csv)
         logP_dist.to_csv(output_dist_csv)
     
    return logP_dist


if __name__ == '__main__':
     main()
