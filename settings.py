'''
FileName: settings.py
Author: Chuncheng
Version: V0.0
Purpose: Setting Common Variables
'''

# Import All the Necessary Files
# All the modules only have to use this script to import the Necessary Modules | Packages
# >> from settings import *
import os
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from tqdm.auto import tqdm

# Number of Road Nodes
Num = 100

# Folder of middleResults
MiddleFolder = os.path.join(__file__, '..', 'middleResults')

# Timer Wrapper


def timer(func):
    def func_wrapper(*args, **kwargs):
        from time import time
        time_start = time()
        result = func(*args, **kwargs)
        time_end = time()
        time_spend = time_end - time_start
        print('\nTime Costing: {}: {:0.4f} s\n'.format(func.__name__, time_spend))
        return result
    return func_wrapper
