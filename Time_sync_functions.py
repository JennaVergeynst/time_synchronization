"""
Created on Wen Feb 13 2019

Contains functions:
- get_DTD
- add_DTD
- smooth_DTD
- model_spline_part


@author: Jenna Vergeynst
"""


import numpy as np
import pandas as pd
import pytz
from scipy.interpolate import UnivariateSpline, splrep
import pickle
import glob
import random


def get_DTD(row, S_on_base, timecol='Time'):
        """
        function to get DTD of a row
        The function compares Time of row (of Sx_on_rec) with nearest time in Sx_on_base,
        but within time_margin (100) seconds, to make it faster and avoid points too far in time.
        Within this time_margin, it looks up the iloc of the nearest time point,
        then takes the DTD with this point.

        Input:
        -----
        S_on_base : df with sync detections on base receiver
        row: row of df with sync detections on other receiver
        """
        try:
            correspoints = S_on_base[row.lower_lim:row.upper_lim]
            nearest_iloc = correspoints.index.get_loc(row[timecol], method='nearest')
            nearest_time = correspoints.reset_index().iloc[nearest_iloc][timecol]
            DTD = (row[timecol] - nearest_time).total_seconds()
#             DTDs = pd.Series((row[timecol] - correspoints.index).total_seconds())
#             index_of_smallest = DTDs.abs().idxmin()
#             DTD = DTDs[index_of_smallest]
            return DTD
        except: # if there is no point in interval: IndexError, ValueError
            return None

def add_DTD(Sx_on_rec, Sx_on_base, tcol='Time', time_margin=100, check_period=None):
    """
    Input
    -----
    Sx_on_rec : df with detections of sync tag on other receiver
    Sx_on_base : df with detections of sync tag on base receiver
    tcol : str, name of time column (default Time)
    time_margin : time interval in which to search in the other receiver df
                  (Sx_on_rec) for corresponding time points
    check_period: str with date, month or year to check, default None
    Returns
    ------
    df with DTD column added
    """
    if pd.notnull(check_period):
        Sx_on_rec = Sx_on_rec.set_index(tcol)[check_period].reset_index()
        Sx_on_base = Sx_on_base.set_index(tcol)[check_period].reset_index()

    Sx_on_rec['lower_lim'] = Sx_on_rec[tcol]-pd.Timedelta(seconds=time_margin)
    Sx_on_rec['upper_lim'] = Sx_on_rec[tcol]+pd.Timedelta(seconds=time_margin)

    Sx_on_base = Sx_on_base.set_index(tcol)

    Sx_on_rec['DTD'] = Sx_on_rec.apply(lambda row: get_DTD(row, Sx_on_base, timecol=tcol), axis=1)

    return Sx_on_rec

def smooth_DTD(Sx_on_rec, outlier_lim=0.0001, window_size=6):
    """
    Sx_on_rec : df with detections of sync tag on other receiver with DTD added
    outlier_lim : if the difference between to adjacent DTDs is larger than
                  this value, it is omitted. Default 0.0001
    window_size : smooth the result to throw out also outliers if there are
                  multiple adjacent ones (and only first or last is thrown out)
    """
    Sx_on_rec['DTD_smooth'] = Sx_on_rec.DTD.copy()
    # put first and last value on nan to avoid border phenomena
    Sx_on_rec.loc[0,'DTD_smooth'] = np.nan
    Sx_on_rec.loc[len(Sx_on_rec)-1,'DTD_smooth'] = np.nan
    Sx_on_rec.loc[Sx_on_rec['DTD_smooth'].diff().abs()>outlier_lim, 'DTD_smooth'] = np.nan
    Sx_on_rec['DTD_smooth'] = Sx_on_rec['DTD_smooth'].rolling(window=window_size).mean()

    return Sx_on_rec

def model_spline_part(DTD_S, ts, DTD_col='DTD_smooth', k=4, s=1e-3):
    """
    Function to model the spline (error on DTD due to receiver drift)

    Parameters
    ----------
    DTD_S : df with time in index and DTD between 2 receivers in rows (result from DTD_Sx)
    ts : timeseries on which to apply the modelled spline (logically the time column of the receiver to correct)
    DTD_col : str, column name of DTD to model, default DTD_smooth
    k : Degree of the smoothing spline.  Must be <= 5.
    Default is k=3, a cubic spline.
    s : Positive smoothing factor used to choose the number of knots.
    Default value of 0.0003 gives good equilibrum between interpolating through each point
    and smoothing slightly (but also requires outliers >0.001 to be removed)


    Returns
    -------
    ts_part : part of the timeseries for which this spline part is modeled
    ys : modelled spline
    """

    if len(DTD_S)>5:

        ts_part = ts[(DTD_S.reset_index().Time.min()<ts) & (ts<DTD_S.reset_index().Time.max())]
        x = DTD_S[DTD_S.notna().values].index.astype(int)
        y = DTD_S[DTD_S.notna().values][DTD_col].values
        s = UnivariateSpline(x, y, k=k, s=s)

        ys = s(np.int64(ts_part))
        df_part = pd.DataFrame(columns=['Time','spline'])
        df_part['Time'] = ts_part
        df_part['spline'] = ys

    else:
        df_part = pd.DataFrame()

    return df_part
