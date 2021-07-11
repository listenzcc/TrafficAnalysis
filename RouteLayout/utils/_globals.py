'''
FileName: globals.py
Author: Chuncheng
Version: V0.0
Purpose: Global Variables of the Package
'''

from ._requires import *

# Encoding
Encoding = 'utf-8'

# Number of Road Nodes
Num = 100

# Folder of middleResults
MiddleFolder = os.path.join(__file__, '..', '..', '..', 'middleResults')

# Folder of GeoData
GeoDataFolder = os.path.join(os.environ['SYNC'], 'GeoData', 'json-files')
