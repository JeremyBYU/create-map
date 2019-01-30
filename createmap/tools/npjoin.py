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

    print("Final size is : {}".format(combined_data.shape))
    if args.las:
        new_filename = Path(args.out).stem + ".las"
        make_las_file(combined_data, new_filename)
    else:
        np.save(args.out, combined_data)
