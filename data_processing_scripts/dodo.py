from glob import glob
import os
from os import path


def task_convert_take_to_csv():
    return {
        'targets': [r'.\VRCliffExp_2017-06-12_12-49-55_VR-3A_VR_R_E_9A4-639.csv'],
        'file_dep': [r'.\VRCliffExp_2017-06-12_12-49-55_VR-3A_VR_R_E_9A4-639.tak'],
        'actions': ['ipy64 take_to_csv.py %(dependencies)s %(targets)s']
    }


def task_convert_take_to_avi():
    return {
        'targets': [r'.\VRCliffExp_2017-06-12_12-49-55_VR-3A_VR_R_E_9A4-639.avi'],
        'file_dep': [r'.\VRCliffExp_2017-06-12_12-49-55_VR-3A_VR_R_E_9A4-639.tak'],
        'actions': ['ipy64 take_to_avi.py %(dependencies)s %(targets)s']
    }