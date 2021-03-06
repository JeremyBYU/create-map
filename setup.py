from setuptools import setup, find_packages
setup(
    name="createmap",
    version="0.1",
    packages=find_packages(),
    scripts=['cm'],

    # installed or upgraded on the target machine
    install_requires=['numpy', 'shapely', 'shapely-geojson', 'laspy>=1.5.0', 'matplotlib', 'seaborn', "Cython", 'descartes'],

    package_data={
        # If any package contains *.txt or *.rst files, include them:
        '': ['*.txt', '*.rst', 'cm'],
    },

    # metadata to display on PyPI
    author="Jeremy Castagno",
    author_email="jdcasta@umich.edu",
    description="Creates map data from point cloud data",
    license="MIT",
    keywords="voxel elevation lidar las",
    url="",   # project home page, if any

)