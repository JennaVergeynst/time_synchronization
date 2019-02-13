"""
Created on Wen Feb 13 2019

Script to create "Detection Time Difference" dataframes of one receiver pair

@author: Jenna Vergeynst
"""

import numpy as np
import pandas as pd
import pytz
from scipy.interpolate import UnivariateSpline, splrep
import pickle
import glob
import random


from Time_sync_functions import add_DTD


Sbase_ID = '62059'
Srec_ID = '62211'

# choose a central receiver in the network as "timekeeper" or base receiver
# All other receivers are synchronised to the base receiver
base_receiver = pd.read_pickle('example_base_461059.pkl')
other_receiver = pd.read_pickle('example_rec_461211.pkl')

# Take sub dataframes for detections of synctags of both receivers on these receivers
Sbase_on_base = base_receiver[base_receiver.ID==Sbase_ID].copy()
Sbase_on_rec = other_receiver[other_receiver.ID==Sbase_ID].copy()
Srec_on_base = base_receiver[base_receiver.ID==Srec_ID].copy()
Srec_on_rec = other_receiver[other_receiver.ID==Srec_ID].copy()

## Add DTD to the sub dataframes of other_receiver
# DTD = difference in detection time between both receivers when detecting
# the same ping coming from a certain transmitter (here synchronisation transmitter)
# Warning: might take some minutes!
Sbase_on_rec = add_DTD(Sbase_on_rec, Sbase_on_base, tcol='Time', time_margin=100)
Srec_on_rec = add_DTD(Srec_on_rec, Srec_on_base, tcol='Time', time_margin=100)

Sbase_on_rec.to_pickle('461211_Sbase_DTD.pkl')
Srec_on_rec.to_pickle('461211_Srec_DTD.pkl')
