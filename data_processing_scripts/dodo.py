from glob import glob
import os
from os import path


basedir = r"Z://nickdg/data/VR_Experiments_Round_2"
take_basedir = path.join(basedir, 'Motive Files', 'VR_Experiment_Data', 'MotiveProjects_2')
converted_basedir = path.join(basedir, 'Converted Motive Files')

def task_convert_take_files():
    """Turns the proprietary Motive Take file formatted-files from the experiment into CSV and AVI files."""
    for currpath, pathnames, fnames in os.walk(take_basedir):
        take_files = [path.basename(fname) for fname in glob(path.join(currpath, '*.tak'))]
        for take_file in take_files:
            basename = path.splitext(take_file)[0]
            yield {
                'file_dep': [path.join(currpath, take_file)],
                'targets': [path.join(converted_basedir, basename, basename + '.csv')],
                'actions': ['ipy64 take_to_csv.py "%(dependencies)s" "%(targets)s"'],
                'name': 'to_csv: {}'.format(basename),
            }
            print(currpath)
            yield {
                'file_dep': [path.join(currpath, take_file)],
                'targets': [path.join(converted_basedir, basename, basename + '.avi')],
                'actions': ['ipy64 take_to_avi.py "%(dependencies)s" "%(targets)s"'],
                'name': 'to_avi: {}'.format(basename),
            }


