#!/usr/bin/env python

import pandas as pd
import numpy as np
import os


# EFM function based on script by Paul Frank, PE and and Elizabeth Caudill 2/5/2013

def main(verbose, hydrology, odir, smo=1, sda=1, emo=1, eda=1, duration=1):

    # read input csv file into data frame object
    df = pd.read_csv(hydrology, sep=',', index_col=0,names=["date","flow"], header=0, parse_dates=True)
 
    #remove all NA values
    df = df.dropna()

    # create data frame object for annual peaks
    peak_columns = ['start_date', 'end_date', 'peak_cfs']
    ann_peak = pd.DataFrame(columns=peak_columns) 
    ann_peak = ann_peak.fillna(0)
    ann_peak['peak_cfs'] = ann_peak['peak_cfs'].astype(int)

    # determine date boundaries
    first_date = min(df.index)
    last_date = max(df.index)
    first_year = min(df.index).year
    last_year = max(df.index).year

    # remove years with incomplete data
    groupyear = df.groupby(lambda x: x.year)
    year_entries = groupyear.agg('count')
    missing_years = list(year_entries[year_entries['flow'] < 365].index)
    
    
    if first_year in missing_years:
          start_date = pd.datetime(first_year, smo, sda)
          start_date_64 = np.datetime64(start_date)
          # check number of days correct
          if first_date <= start_date_64:
              year_end_date = pd.datetime(first_year, 12, 31)
              expect_delta = year_end_date - start_date
              expect_days = expect_delta.days
              actual_days = df.ix[start_date:year_end_date].count().values[0]
              #print expect_days
              #print actual_days
              if actual_days >= expect_days:                          
                   missing_years.remove(first_year)
              

    if last_year in missing_years:
          end_date = pd.datetime(last_year, emo, eda)
          end_date_64 = np.datetime64(end_date)
          # check number of days correct
          if last_date >= end_date_64:
              missing_years.remove(last_year)
              
    record_years= list(set(year_entries.index) - set(missing_years))

    for year in missing_years:
         del_ix = df[(df.index.year==year)].index
         df = df.drop(del_ix)
    print "LISTING OF YEARS WITH INCOMPLETE RECORDS", missing_years
    for year in record_years:
         start_season = pd.datetime(year, smo, sda)
         end_season = pd.datetime(year, emo, eda) 
         if start_season > end_season:
            end_season = pd.datetime(year + 1, emo, eda)
         season = pd.date_range(start_season, end_season)
         annual = df.index.intersection(season)
         if not (annual.tolist()):
             continue
         annual_last_date = max(annual)
         start_window = min(annual)
         end_window = start_window + pd.DateOffset(days=duration-1)
         my_date1 = start_window
         my_date2 = end_window
         if end_window > annual_last_date:
             continue
         
         annual_max = 0
 
         while ((end_window - annual_last_date).days <= 0):
             window = pd.date_range(start_window, end_window)
             period = annual & window
             df_p = df.ix[period]
             period_min = df_p.min().values[0]
             min_days = df_p[df_p['flow'].isin([period_min])]
             last_min_day = min_days.last_valid_index()

             if period_min > annual_max:
                 annual_max = period_min
                 my_date1 = start_window
                 my_date2 = end_window

             start_window = last_min_day + pd.DateOffset(days=1)
             end_window = start_window + pd.DateOffset(days=duration-1)
   
         ann_peak.loc[year,'start_date']= my_date1
         ann_peak.loc[year,'end_date'] = my_date2
         ann_peak.loc[year,'peak_cfs'] = annual_max
    

    if verbose == True:
         head,tail = os.path.split(hydrology)
         hname = tail.split('.')[0]
         sep = os.path.sep
         output_csv = odir + sep + hname + '_' + str(duration) + '_day_' + str(smo) + '_' + str(sda) + '_to_' + str(emo) + '_' + str(eda) + '_peaks.csv' 
         ann_peak.to_csv(output_csv)
         
    return ann_peak
 
if __name__ == '__main__':
     main()
