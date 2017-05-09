#!/usr/bin/env python

import matplotlib
matplotlib.use('Agg')
import bisect
import pandas as pd
import numpy as np
import os
from decimal import *
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

def main(probability, verbose, lp, hydrology, odir, afile, sname, smo=1, sda=1, emo=1, eda=1, duration=1):

    head, tail = os.path.split(hydrology)
    hname = tail.split('.')[0]
    sep = os.path.sep

    # read log Pearson distribution file into data frame object
    #input_file = odir + sep + hname + '_'  + str(duration) + '_day_' + str(smo) + '_' + str(sda) + '_to_' + str(emo) + '_' + str(eda) + '_lp.csv'
    #lp = pd.read_csv(input_file, sep=',', names=["Klow","Khigh","slope","Kint","logQ","Q"], header=0)

    # determine number of flow to area column pairs
    fta_file = pd.read_csv(afile, sep=',', index_col=0, header=0, dtype=float)
    fta_length = len(fta_file.columns)
    # print "FTA_LENGTH IS " + str(fta_length)
    if fta_length%2!=1:
         print "ERROR:  flow to area file should have even number of columns"
         return 0
   
    # process each flow to area pair
    for i in xrange(0, fta_length+1, 2):
         fta = pd.read_csv(afile, sep=',', index_col=0, header=0, dtype=float, usecols =[i, i+1])
         fta = fta.dropna()
         # fta_columns = range(0, len(fta.columns))
    
         # add zero flow to flow to area table if it does not exist
         if 0 not in list(fta.index):
              #print fta.index
              fta.loc[0] = 0
    
         # determine maximum flow values in both flow to area table and log Pearson tables.  add the highest log Pearson flow value to flow to area table 
         max_fta_flow = max(fta.index)
         max_logP_flow = lp['Q'].max()
         #print max_logP_flow

         if max_fta_flow < max_logP_flow:
              max_flow = max_logP_flow
              fta.ix[max_flow, [0]] = fta.ix[max_fta_flow, [0]]
         else:
              max_flow = max_fta_flow
              
         #print "MAX FLOW IS "
         #print max_flow

         # create new flow to area table with interpolated values (flow is incremented by units of 1)
         fta_x = list(fta.index)
         fta_intp_x = list(np.arange(0, max_flow, 1.0)) 
         fta_intp_x = list(set(fta_intp_x + fta_x))
         fta_intp_x.sort()
         fta_intp = fta.reindex(fta_intp_x)
         fta_intp.iloc[:,0] = fta_intp.iloc[:,0].interpolate(method='linear')

         # create new flow table with interpolated values 

         if probability == True:
              lp_intp = lp.astype(float)
              lp_intp_x = list(lp_intp.index.values)
              #mini = min(lp.index)
              #maxi = max(lp.index) 
              #zero = lp[lp['Q'] == 0.0]
              #nonzero = lp[lp['Q'] > 0.0]
              #mini = min(nonzero.index)
              #maxi = max(lp.index)
              #minf = float(Decimal(mini).quantize(Decimal('.1'), rounding=ROUND_DOWN))
              #maxf = round(maxi,1)
              #minc = find_ge(eah_constants.eah_interval_float, mini)
              #maxc = find_le(eah_constants.eah_interval_float, maxi)
              #minindex = eah_constants.eah_interval_float.index(minc)
              #maxindex = eah_constants.eah_interval_float.index(maxc)
              #lp_float_x = eah_constants.eah_interval_float[minindex:maxindex+1]
              #lp_int_x = eah_constants.eah_interval_int[minindex:maxindex+1]
              #incr = 0.1 
              #lp_intp_x = list(np.arange(minf,maxf,incr))
              #lp_intp_x = [round(elem,1) for elem in lp_intp_x]
              #lp_intp_x = list(set(lp_intp_x + lp_float_x ))
              #lp_intp_x.sort()
              #print lp_intp_x
              #nonzero_intp = nonzero.reindex(lp_intp_x)
              #nonzero_intp.Q = nonzero_intp.Q.interpolate(method='linear')
              #lp_intp = pd.concat([zero, nonzero_intp]) 
         else:
              #print lp
              lp_float_x = eah_constants.eah_interval_float
              lp_int_x = eah_constants.eah_interval_int 
              mi = eah_constants.maximum_interval
              lp = lp.astype(float)
              lp.reindex(lp_float_x)
              lp.index = lp.index.astype(float)
              #lp_x = list(lp.index.values)
              #print lp_x
              incr = 0.1 
              lp_intp_x = list(np.arange(1,mi,incr))
              lp_intp_x = [round(elem,1) for elem in lp_intp_x]
              lp_intp_x = list(set(lp_intp_x + lp_float_x ))
              lp_intp_x.remove(1.0)
              lp_intp_x.sort()
              #lp.reindex(lp_intp_x)
              lp_intp = lp.reindex(lp_intp_x)
              #lp.reindex(lp_intp_x, method='bfill')
              #print lp_intp
              #list_lp_intp_x = list(lp_intp.index.values)
              #print list_lp_intp_x
              lp_intp.Q = lp_intp.Q.interpolate(method='linear')
         
         
         # add scenario columns to Log Pearson table
         col_name = fta_intp.columns.values.tolist()[0]
         lp_intp[col_name] = 0

         # find closest flow in flow to area table to each element in log Pearson table
         #for x in lp_intp_x:
              #print lp_intp.ix[[x], 'Q'].values[0]
  
         # probably want index as label - seems like not getting interpolated data
         for x in lp_intp_x:
              low_index = find_le(fta_intp.index.values, lp_intp.loc[x, 'Q'])
              high_index = find_ge(fta_intp.index.values, lp_intp.loc[x, 'Q'])
              if low_index == high_index:
                   lp_intp.ix[x,[6]] = fta_intp.ix[low_index,[0]].values[0]
              else:
                   #print "X:" + str(x)
                   #print "low_index:" + str(low_index)
                   #print "high_index:" + str(high_index)
                   #print "X:" + str(x)
                   #print "low_index:" + str(low_index)
                   #print "high_index:" + str(high_index)
                   #lp_col = col + 6
                   low_val = fta_intp.ix[low_index, [0]].values[0]
                   high_val = fta_intp.ix[high_index, [0]].values[0]
                   slope = (high_val - low_val) / (high_index - low_index)
                   #print "LOW VALUE IS" + str(low_val) + "\n"
                   #print "HIGH VALUE IS" + str(high_val) + "\n"
                   #print "SLOPE IS" + str(slope) + "\n"

                   lp_intp.ix[x, [6]] = low_val + (slope * (lp_intp.loc[x,'Q']-low_index))

         # create column for probability
         lp_intp['Probability'] = 1 / lp_intp.index.values 
         result = lp_intp.sort_values(by=['Probability'])
        # lp_brief = lp_intp.iloc[:,5:8]
         
         # create summary table for key recurrence intervals
         lp_brief_columns = lp_intp.columns.values.tolist()[5:]
         lp_brief_columns.append("eah")
         lp_brief_columns.append("species")
         lp_brief = pd.DataFrame(columns=lp_brief_columns)
         if probability == True:
              mini = min(lp.index)
              maxi = max(lp.index)
              brief_interval = [mini, maxi]
              for x in eah_constants.eah_interval_float:
                  if x <= maxi and x>= mini:
                      brief_interval.append(x)
              brief_interval.sort()
              for x in brief_interval:
                   low_index = find_le(lp_intp.index.values, x)
                   high_index = find_ge(lp_intp.index.values, x)
                   strx=str(x)
                   if low_index == high_index:
                        lp_brief.ix[strx,[0]] = lp_intp.ix[low_index,5]
                        lp_brief.ix[strx,[1]] = lp_intp.ix[low_index,6]
                        lp_brief.ix[strx,[2]] = lp_intp.ix[low_index,7]
                   else:
                        low_Q_val = lp_intp.ix[low_index,5]
                        high_Q_val = lp_intp.ix[high_index, 5]                
                        slope_Q = (high_Q_val - low_Q_val) / (high_index - low_index)
                        low_A_val = lp_intp.ix[low_index,6]
                        high_A_val = lp_intp.ix[high_index, 6]               
                        slope_A = (high_A_val - low_A_val) / (high_index - low_index)
                        low_P_val = lp_intp.ix[low_index, 7]
                        high_P_val = lp_intp.ix[high_index, 7]                
                        slope_P = (high_P_val - low_P_val) / (high_index - low_index)
                        lp_brief.ix[strx,[0]] = low_Q_val + (slope_Q * (x-low_index))
                        lp_brief.ix[strx,[1]] = low_A_val + (slope_A * (x-low_index))
                        lp_brief.ix[strx,[2]] = low_P_val + (slope_P * (x-low_index))
         else:
              lp_brief_data = lp_intp.iloc[:,5:8]
              lp_brief_data = lp_brief_data.loc[lp_int_x,:]
              lp_brief = lp_brief.append(lp_brief_data, ignore_index=False)
      
         # calculate eah
         lp_brief['eah'] = np.trapz(result.iloc[:,6], result['Probability'])
         lp_brief['species'] = sname
           
         # output interpolated data
         output_lp_csv = odir + sep + hname + '_' + col_name + '_' + str(duration) + '_day_' + str(smo) + '_' + str(sda) + '_to_' + str(emo) + '_' + str(eda) + '_ilp.csv'
         output_brief_csv = odir + sep + hname + '_' + col_name + '_' + str(duration) + '_day_' + str(smo) + '_' + str(sda) + '_to_' + str(emo) + '_' + str(eda) + '_blp.csv'       
         lp_brief.to_csv(output_brief_csv)
         result.to_csv(output_lp_csv)   
        
         if verbose == True:
              output_fta_csv = odir + sep + hname + '_' + col_name + '_' + str(duration) + '_day_' + str(smo) + '_' + str(sda) + '_to_' + str(emo) + '_' + str(eda) + '_ifta.csv'
              fta_intp.to_csv(output_fta_csv)
        
         


if __name__ == '__main__':
     main()
