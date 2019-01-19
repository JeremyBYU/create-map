# Create Map



## Install

1. `pip install -e . --process-dependency-links`




## Instructions

Input should be a numpy array file with dimensions (N, 4).  The second dimension has data (x,y,z,CLASS_ID).

The CLASS_ID is a floating point like 0.0, 1.0, 2.0, etc.  It used to filter point so that the geometry extraction process can focus on only 
points that are related.

A configuration file can be provided as input to do an initial filtering  of the point cloud data.

### Configuration File

```json
{
  "classes": [
    "Floor",
    "Building_Fake_2",
    "Building_Fake_1"
  ],
  "filters": [
    "Building.*"
  ],
  "np2geom": {
    "hull_type": "concave",
    "z_thresh": 100,
    "y_thresh": 100,
    "x_thresh": 100,
    "min_area": 160000,
    "min_bbox_area": 160000,
    "negative_buffer": 0,
    "simplify_buffer": 250
  },
  # THIS IS ADDED BY np2filt and USED by NP2GEOM
  "filtered_classes": [
    "Building_Fake_2",
    "Building_Fake_1"
  ]
}
```

### NPFILT

Specify Regex filters under the filters keyword to keep only points that belong to classes you interested in.

The configuration file will be modified at the end with a "filtered_classes" key with all the filtered classes that passed the regex filters.

```
usage: ./cv npfilt [-h] --input INPUT --config CONFIG [--out OUT]

optional arguments:
  -h, --help            show this help message and exit
  --input INPUT, -i INPUT
                        path to numpy point cloud (default: None)
  --config CONFIG, -c CONFIG
                        Path to class mapping (default: None)
  --out OUT, -o OUT     path to output las file (default:
                        point_cloud_filtered.npy)
```

### NP2GEOM

Currently only extracts planes (like building rooftops). Parameters to be explained later under "np2geom" key.

$ cm np2geom --help
usage: ./cv np2geom [-h] --input INPUT --config CONFIG [--out OUT]

optional arguments:
  -h, --help            show this help message and exit
  --input INPUT, -i INPUT
                        path to numpy point cloud (default: None)
  --config CONFIG, -c CONFIG
                        Path to JSON config (default: None)
  --out OUT, -o OUT     path to output las file (default:
                        point_cloud_map.json)


### NP2LAS 

Converts Numpy file to LAS file format. Can be visualized with plas.io.

```
$ cm np2las --help
usage: ./cv np2las [-h] --input INPUT [--config CONFIG] [--out OUT]

optional arguments:
  -h, --help            show this help message and exit
  --input INPUT, -i INPUT
                        path to numpy point cloud (default: None)
  --config CONFIG, -c CONFIG
                        Path to class mapping (default: None)
  --out OUT, -o OUT     path to output las file (default: point_cloud.las)
```




