#!/usr/bin/env python

from argparse import ArgumentParser
import efm
import lp
import area
import graph
import prob


def main():
    usage = "usage: %prog [options] arg1 arg2"
    parser = ArgumentParser(usage)
    parser.add_argument("-hfile", "--hydro_file", dest="hydro_file", help="input file with daily hydrological record")
    parser.add_argument("-afile", "--fta_file", dest="fta_file", help="input file with flow to area mapping")
    parser.add_argument("-odir", "--output_dir", dest="output_dir", help="output directory for saving results")
    parser.add_argument("-sname", "--species_name", dest="species_name", help="name of species matching duration and timing criteria")
    parser.add_argument("-smo", "--start_month", type=int, dest="start_month", help="starting month number for season of interest")
    parser.add_argument("-sda", "--start_day", type=int, dest="start_day", help="starting day number for season of interest")
    parser.add_argument("-emo", "--end_month", type=int, dest="end_month", help="ending month number for season of interest")
    parser.add_argument("-eda", "--end_day", type=int, dest="end_day", help="ending day number for season of interest")
    parser.add_argument("-durations", "--durations", type=int, dest="durations", help="the number of consecutive days the flow must occur", nargs='+')
    parser.add_argument("-verbose", "--verbose", dest="verbose", action='store_true', help="write all output to csv files")
    parser.add_argument("-probability", "--probability", dest="probability", action='store_true', help="use raw probability values instead of log Pearson distribution")
    args = parser.parse_args()

    # check that file parameters are specified in command line
    mandatories = ['hydro_file', 'fta_file', 'output_dir', 'start_month','start_day','end_month','end_day','durations']
    for m in mandatories:
        if getattr(args, m) == None:
            parser.error("option -" + m + " is mandatory.")
    if args.species_name == None:
        args.species_name = ""

    for dur in args.durations:
        efm_data = efm.main(args.verbose, args.hydro_file, args.output_dir, args.start_month, args.start_day, args.end_month, args.end_day, dur)
        if args.probability == True:
             lp_data = prob.main(args.verbose, efm_data, args.hydro_file, args.output_dir, args.start_month, args.start_day, args.end_month, args.end_day, dur)
        else:
             lp_data = lp.main(args.verbose, efm_data, args.hydro_file, args.output_dir, args.start_month, args.start_day, args.end_month, args.end_day, dur)
        area_data = area.main(args.probability, args.verbose, lp_data, args.hydro_file, args.output_dir, args.fta_file, args.species_name, args.start_month, args.start_day, args.end_month, args.end_day, dur)

    result = graph.main(args.hydro_file, args.output_dir, args.fta_file, args.start_month, args.start_day, args.end_month, args.end_day, args.durations)


if __name__ == '__main__':
     main()
