"""Generates Map environment

This module will generate a map database of buildings from a lidar point cloud
Data sources:
    - Lidar point cloud

"""


import re
import logging
import numpy as np
import polylidar
from polylidar.polylidarutil.plane_filtering import filter_planes
from shapely_geojson import dumps, Feature, FeatureCollection
from shapely.geometry.multipolygon import MultiPolygon

def get_allowed_classes(class_mapping):
    classes = class_mapping.get('classes')
    filters = class_mapping.get('filters')
    if not classes or not filters:
        raise Exception("No classes or filters key found in filter JSON file")

    filters = [re.compile(filter_) for filter_ in filters]
    keep_classes = []
    class_labels = []
    
    for old_int_value, class_label in enumerate(classes):
        for regex in filters:
            if regex.match(class_label):
                keep_classes.append(old_int_value)
                class_labels.append(class_label)
                break

    return keep_classes, class_labels
    

def filter_classes(pc, filters):
    keep_classes, class_labels = get_allowed_classes(filters)

    classes = pc[:, 3]
    mask = np.isin(classes, keep_classes)
    pc_filtered = pc[mask, :]

    pc_filtered_ = pc_filtered.copy()
    for i, old_class in enumerate(keep_classes):
        pc_filtered_[pc_filtered == old_class] = i

    return pc_filtered_, class_labels


def get_planes(pl: polylidar.Polylidar3D, lidar_building, class_id, class_label, config_pp, **kwargs):
    np_mat = polylidar.MatrixDouble(lidar_building)
    mesh, planes, polygons = pl.extract_planes_and_polygons(np_mat)
    planes = filter_planes(polygons, lidar_building, config_pp)
    features = []
    for plane in planes:
        features.append(Feature(plane[0], {'class_id': class_id, 'class_label': class_label, 'height': plane[1]}))
    return features

def get_geometries(pc, class_labels, polylidar_kwargs, config_pp, **kwargs):
    classes = pc[:, 3]
    xyz = pc[:, :3]
    unique_classes = np.unique(classes)
    geometries = []
    pl = polylidar.Polylidar3D(**polylidar_kwargs)
    for class_id in unique_classes:
        building = np.copy(xyz[classes == class_id])
        class_label = class_labels[int(class_id)]
        geometries.extend(get_planes(pl, building, class_id, class_label, config_pp, **kwargs))

    logging.info("Extracted %r geometries", len(geometries))
    return FeatureCollection(geometries)

