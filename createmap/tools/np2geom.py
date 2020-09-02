import argparse
import json
import re
import logging

import numpy as np
from createmap import get_geometries
from shapely_geojson import dump

LOGGER = logging.getLogger('createmap')
LOGGER.setLevel(logging.INFO)


def add_parser(subparser):
    parser = subparser.add_parser(
        "np2geom", help="Convert point cloud features to a 2D geometry map", formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    parser.add_argument("--input", "-i", type=str, required=True,
                        help="path to numpy point cloud")
    parser.add_argument("--config", "-c", type=str, help="Path to JSON config", required=True)
    parser.add_argument("--out", "-o", type=str, default="point_cloud_map.json",
                        help="path to output las file")

    parser.set_defaults(func=main)


def main(args):
    numpy_pc = np.load(args.input)
    numpy_pc = numpy_pc.astype('f8')
    logging.info("Converting numpy point cloud to geometries")
    if numpy_pc.shape[1] == 4:
        with open(args.config) as f:
            config = json.load(f)
        geometries = get_geometries(numpy_pc, config['filtered_classes'], config['polylidar_kwargs'], config['config_pp'])
        with open(args.out, "w") as f:
            dump(geometries, f, indent=2)

    else:
        print("Error! Numpy file does not have class information. Except shape to be (X, 4)")
    


