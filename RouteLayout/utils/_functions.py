'''
FileName: functions.py
Author: Chuncheng
Version: V0.0
Purpose: Reuseable Functions
'''

from ._requires import *
from ._globals import *


def Timer(func):
    ''' Wrapper of Timer,
    Designed for Supporting @timer Useage.
    '''
    def func_wrapper(*args, **kwargs):
        from time import time
        time_start = time()
        result = func(*args, **kwargs)
        time_end = time()
        time_spend = time_end - time_start
        Debug('AutoTimer: {} costs {:0.4f} seconds\n'.format(
            func.__name__, time_spend))
        return result
    return func_wrapper


def Path(name, folder=MiddleFolder):
    ''' Get the Full-Path of [folder]/[name] '''
    return os.path.join(folder, name)


def Debug(msg):
    print('--- D: {}'.format(msg))


def Info(msg):
    print('--- I: {}'.format(msg))


def Warning(msg):
    print('??? W: {}'.format(msg))


def Error(msg):
    print('!!! E: {}'.format(msg))

# def _dump(name, obj, folder=_middleFolder):
#     ''' Dump [obj] to [folder]/[name] '''
#     p = os.path.join(folder, name)
#     if os.path.isfile(p):
#         print('W: File Override Warning: {}'.format(p))
#     dump(obj, p)
#     print('D: Saved New File: {}'.format(p))
#     return p


# def _load(name, folder=_middleFolder):
#     ''' Load file at [folder]/[name] '''
#     p = os.path.join(folder, name)
#     print('D: Loading Middle Results of {}'.format(p))
#     return load(p)
