import argparse
import json
import re
from pathlib import Path

import glob
import numpy as np

from createmap.tools.np2las import make_las_file

def add_parser(subparser):
    parser = subparser.add_parser(
        "npjoin", help="Combine numpy arrays of similar shape", formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    parser.add_argument('--files', '-f', type=argparse.FileType('rb'), nargs='+', help='Files to combines')
    parser.add_argument("--las", "-l", help="Convert to las", action="store_true", default=False)
    parser.add_argument("--csv", "-c", help="Convert to csv", action="store_true", default=False)
    parser.add_argument("--csv-header", "-ch", help="Header for CSV", type=str, default="")
    parser.add_argument("--scale", "-s", type=str, default="", help="Scale axes, -s 1,1,100 scales column z axes by 100")
    parser.add_argument("--axis", "-a", type=str, default="", help="Reorder axes, -o 2,1,0 swaps x and z axes")
    parser.add_argument("--out", "-o", type=str, default="combined.npy",
                        help="path to output numpy file")

    parser.set_defaults(func=main)


def main(args):

    print("Joining numpy arrays")
    # npfiles = glob.glob(args.glob)
    # npfiles.sort()
    combined_data = None
    for file in args.files:
        data= np.load(file)
        if combined_data is not None:
            combined_data = np.vstack((combined_data, data))
        else:
            combined_data = data
    # Make modifications
    if args.scale:
        split = args.scale.split(',')
        assert len(split) == combined_data.shape[1]
        temp = combined_data.copy()
        for axis, mult_str in enumerate(split):
            mult_float = float(mult_str)
            combined_data[:, axis] = temp[:, axis] * mult_float
    
    if args.axis:
        split = args.axis.split(',')
        assert len(split) == combined_data.shape[1]
        temp = combined_data.copy()
        for orig_axis, axis_str in enumerate(split):
            axis_num = int(axis_str)   
            combined_data[:, orig_axis] = temp[:, axis_num]

    print("Final size is : {}".format(combined_data.shape))
    if args.las:
        new_filename = Path(args.out).stem + ".las"
        make_las_file(combined_data, new_filename)
    elif args.csv:
        new_filename = Path(args.out).stem + ".csv"
        np.savetxt(new_filename, combined_data, fmt='%.4f', delimiter=',', header=args.csv_header, comments='')
    else:
        np.save(args.out, combined_data)
