#!/usr/bin/env python

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import glob
import os
import itertools
from time import strftime

def main(hydrology, odir, afile, smo=1, sda=1, emo=1, eda=1, durations=[1]):

    sep = os.path.sep
    head,tail = os.path.split(hydrology)
    h = [(tail.split('.')[0])]
    durations.sort()
    d = [str(x) for x in durations]
    season = str(smo) + "_" + str(sda) + "_to_" + str(emo) + "_" + str(eda)
    s = [season]
    f = []
    fta_file = pd.read_csv(afile, sep=',', index_col=0, header=0, dtype=float)
    fta_length = len(fta_file.columns)
    fta_columns = fta_file.columns.values.tolist()
    for i in xrange(0, fta_length+1, 2):
         f.append(fta_columns[i]) 
  
    combo = list(itertools.product(h, f, d, s))    #print combo
    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)

    for c in combo:
        h = c[0]
        f = c[1]
        d = c[2]
        s = c[3]
        ilp_file = odir + sep + h + '_' + f + '_' + d + '_day_' + s +  '_ilp.csv'
        eah_file = odir + sep + h + '_' + f + '_' + d + '_day_' + s +  '_blp.csv'
        ilp_check = glob.glob(ilp_file)
        eah_check = glob.glob(eah_file)
        if ilp_check and eah_check:
             data = pd.read_csv(ilp_file)
             eah = pd.read_csv(eah_file)
             columns = range(7, len(data.columns)-1)
             for col in columns:
                  eah_val = eah.loc[0,'eah']
                  eah_val = round(eah_val,2)
                  species = eah.loc[0,'species']
                  #sname = species[0]
                  if type(species)  == np.float64:
                      lname = h + '_' + f + '_' + d + 'day_' + s + '; EAH= ' + str(eah_val)
                  else:
                      lname = species + '_' + h + '_' + f + '_' + d + 'day_' + s + '; EAH= ' + str(eah_val)
                  ax.plot(data['Probability'],data[[col]], label = lname)
                  ax.legend(loc='upper right', prop={'size':8})

    title = "ADF Plot"
    fig.suptitle(title) 
    plt.xlabel('Probability (1/year)')
    plt.ylabel('Inundated Area (acres)')
    datestamp = strftime("%Y-%m-%d-%H-%M-%S")
    output_file = odir + sep + "EAH_graph" + datestamp
    fig.savefig(output_file)


if __name__ == '__main__':
     main()
