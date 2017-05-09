# -*- coding: utf-8 -*-
"""
Created on Tue Aug 26 08:57:54 2014

@author: SLALONDE
"""
import pandas as pd
import numpy as np
import os
import eah_constants

def main(verbose, ann_peak, hydrology, odir, smo=1, sda=1, emo=1, eda=1, duration=1):

    head, tail = os.path.split(hydrology)
    hname = tail.split('.')[0]
    sep = os.path.sep

   # sort peak flows in descending order
    flow = ann_peak.sort_values(by=['peak_cfs'], ascending=False)
    fgroup = flow.groupby('peak_cfs').size()
    zero_count = 0
    if 0.0 in fgroup.index:
        zero_count = fgroup.loc[0.0]
    print "COUNT OF NUMBER OF YEARS WITH ZERO FLOW (cfs)", zero_count    
    
    # create column for log of each peak flow
    flow['log_q'] = np.log10(flow['peak_cfs'])

    # create column for rank
    flow['rank'] = flow['peak_cfs'].rank(method='first', ascending=False)
    #lp['rank'] = lp['peak_cfs'].rank(method='average', ascending=False)

    # calculate number of records
    num_records = len(flow.index)
 
    # create column for return period (Tr)
    flow['tr'] = (num_records + 1) / flow['rank'] 
    tr = flow['tr'].values
    
    period = [round(elem, 5) for elem in tr]
    nflow = flow.set_index([period])
    prob_columns = eah_constants.dist_columns
    prob = pd.DataFrame(columns=prob_columns)
    prob = prob.fillna(0)
    prob['logQ'] = nflow['log_q']
    prob['Q'] = nflow['peak_cfs']
    prob.sort_index(axis=0, ascending=True, inplace=True)
    
    
    if verbose == True:
        output_dist_csv = odir + sep + hname + '_' + str(duration) + '_day_' + str(smo) + '_' + str(sda) + '_to_' + str(emo) + '_' + str(eda) + '_prob.csv'
        prob.to_csv(output_dist_csv)

    return prob