import argparse
import json
import re

import numpy as np

from laspy.file import File, header


def make_las_file(data, file_name=''):
    my_header = header.Header()
    outFile = File(file_name, mode='w', header=my_header)

    # outFile.header.offset = np.amin(data, axis=0)[0:3]
    outFile.header.scale = [1, 1, 1]

    outFile.x = data[:, 0]
    outFile.y = data[:, 1]
    outFile.z = data[:, 2]
    outFile.raw_classification = data[:, 3]

    outFile.close()

# def get_int_mapping(class_mapping, unassigned_int=0):
#     classes = class_mapping.get('classes')
#     mapping = class_mapping.get('mapping')
#     if not classes or not mapping:
#         raise Exception("No classes or mapping key found in JSON file")

#     int_mapping = {}

#     mapping = { key: list(map(re.compile, val)) for (key, val) in mapping.items()}
    
#     for class_label, old_int_value in classes.items():
#         # print(class_label, int_value)
#         new_int_value = unassigned_int
#         for int_value, regexes in mapping.items():
#             for regex in regexes:
#                 if regex.match(class_label):
#                     new_int_value = int_value
#                     break
#             if new_int_value != unassigned_int:
#                 break
#         if new_int_value != unassigned_int:
#             int_mapping[old_int_value] = new_int_value

#     return int_mapping
    

# def convert_classes(pc, class_mapping):
#     int_mapping = get_int_mapping(class_mapping)

#     new_ints = np.zeros((pc.shape[0],), dtype=pc.dtype)
#     old_ints = pc[:,3]
#     for old_int_value, new_int_value in int_mapping.items():
#         mask = old_ints == old_int_value
#         new_ints[mask] = new_int_value
    
#     return new_ints


def add_parser(subparser):
    parser = subparser.add_parser(
        "np2las", help="Transforms a point cloud numpy array to las file", formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    parser.add_argument("--input", "-i", type=str, required=True,
                        help="path to numpy point cloud")
    parser.add_argument("--config", "-c", type=str, help="Path to class mapping")
    parser.add_argument("--out", "-o", type=str, default="point_cloud.las",
                        help="path to output las file")

    parser.set_defaults(func=main)


def main(args):
    numpy_pc = np.load(args.input)
    print("Converting numpy point cloud")
    if args.config and numpy_pc.shape[1] == 4:
        with open(args.config) as f:
            class_mapping = json.load(f)
        new_ints = convert_classes(numpy_pc, class_mapping)
        numpy_pc[:,3] = new_ints
    
    make_las_file(numpy_pc, args.out)


