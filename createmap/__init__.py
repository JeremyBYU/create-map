"""Generates Map environment

This module will generate a map database of buildings from a lidar point cloud
Data sources:
    - Lidar point cloud

"""


import re
import numpy as np
import polylidar
from shapely_geojson import dumps, Feature, FeatureCollection

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


def get_planes(lidar_building, class_id, class_label, **kwargs):
    plane_patches, tri, _ = polylidar.extract_planes(lidar_building, **kwargs)
    geometries = polylidar.plane_meshes_to_polygons(tri, plane_patches, lidar_building, **kwargs)
    features = []
    for geom in geometries:
        features.append(Feature(geom['geometry'], {'class_id': class_id, 'class_label': class_label, 'height': geom['height']}))
    return features

def get_geometries(pc, class_labels, **kwargs):
    classes = pc[:, 3]
    unique_classes = np.unique(classes)
    geometries = []
    for class_id in unique_classes:
        building = pc[classes == class_id]
        print(building.shape)
        class_label = class_labels[int(class_id)]
        geometries.extend(get_planes(building, class_id, class_label, **kwargs))
    return FeatureCollection(geometries)

