from glob import glob
import os
from os import path
from datetime import datetime

basedir = r"Z://nickdg/data/VR_Experiments_Round_2"
take_basedir = path.join(basedir, 'Motive Files', 'VR_Experiment_Data', 'MotiveProjects_2')
converted_basedir = path.join(basedir, 'Converted Motive Files')

def task_convert_take_files():
    """Turns the proprietary Motive Take file formatted-files from the experiment into CSV and AVI files."""
    for idx1, (currpath, pathnames, fnames) in enumerate(os.walk(take_basedir)):
        take_files = [path.basename(fname) for fname in glob(path.join(currpath, '*.tak'))]
        for idx2, take_file in enumerate(take_files):
            basename = path.splitext(take_file)[0]
            if 'Exp' not in basename:
                creation_datetime = datetime.fromtimestamp(path.getctime(path.join(currpath, take_file)))
                basename = basename + '_' + creation_datetime.strftime('%Y%m%d_%H%M%S') + '_' + str(idx1) + '_' + str(idx2)
            if 'Acuity' not in basename:
                continue

            # print('About to Start Working on File: ', path.join(currpath, basename))
            if not 'H' in take_file[:5]:  # Skipping the Babit files
                yield {
                    'file_dep': [path.join(currpath, take_file)],
                    'targets': [path.join(converted_basedir, basename, basename + '.csv')],
                    'actions': ['ipy64 take_to_csv.py "%(dependencies)s" "%(targets)s"'],
                    'name': 'to_csv: {}'.format(basename),
                    'verbosity': 2,
                }

                yield {
                    'file_dep': [path.join(currpath, take_file)],
                    'targets': [path.join(converted_basedir, basename, basename + '.avi')],
                    'actions': ['ipy64 take_to_avi.py "%(dependencies)s" "%(targets)s"'],
                    'name': 'to_avi: {}'.format(basename),
                    'verbosity': 2,
                }

