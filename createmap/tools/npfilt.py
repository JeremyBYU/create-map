import argparse
import json
import re

import numpy as np
from createmap import filter_classes


def add_parser(subparser):
    parser = subparser.add_parser(
        "npfilt", help="Filters numpy point cloud", formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    parser.add_argument("--input", "-i", type=str, required=True,
                        help="path to numpy point cloud")
    parser.add_argument("--config", "-c", type=str, help="Path to class mapping", required=True)
    parser.add_argument("--out", "-o", type=str, default="point_cloud_filtered.npy",
                        help="path to output las file")

    parser.set_defaults(func=main)


def main(args):
    numpy_pc = np.load(args.input)
    print("Filtering numpy point cloud")
    if numpy_pc.shape[1] == 4:
        with open(args.config) as f:
            filters = json.load(f)
        pc_filtered, class_labels = filter_classes(numpy_pc, filters)
        # Save Filters
        filters['filtered_classes'] = class_labels
        with open(args.config, 'w') as outfile:
            json.dump(filters, outfile, indent=2)
        # Save 
        np.save(args.out, pc_filtered)
    else:
        print("Error! Numpy file does not have class information. Except shape to be (X, 4)")
    


