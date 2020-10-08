# -*- coding: utf-8 -*-
"""
Created on Thu Oct  8 15:13:44 2020

@author: Freddy
"""

import numpy as np
import pandas as pd

#Helpers
import os
#import pycountry
import glob
from datetime import datetime, date, timedelta, time


#Ploting
import matplotlib.pyplot as plt
#import seaborn as sns


input_directory_path = os.path.join('input')
processed_directory_path = 'processed'
output_directory_path = os.path.join('output')

os.makedirs(input_directory_path, exist_ok=True)
os.makedirs(processed_directory_path, exist_ok=True)
os.makedirs(output_directory_path, exist_ok=True)

# Import function timeseries_opsd

def load_timeseries_opsd(years=None, fn=None, countries=None, source="ENTSOE_transparency"):
    """
    Read data from OPSD time-series package own modification.

    Parameters
    ----------
    years : None or slice()
        Years for which to read load data (defaults to
        slice("2018","2019"))
        
    fn : file name or url location (file format .csv)
    
    countries : Countries for which to read load data.
        
    source : "ENTSOE_transparency" or "ENTSOE_power_statistics"

    Returns
    -------
    load : pd.DataFrame
        Load time-series with UTC timestamps x ISO-2 countries
    """

     
    if source == 'ENTSOE_transparency':
        generation = (pd.read_csv(fn, index_col=[0], header=[0, 1, 2, 3, 4, 5], parse_dates=True)
                    .dropna(how="all", axis=0))
        
    else:
        raise NotImplementedError(f"Data for source `{source}` not available.")
    
    
    #generation = generation.rename(columns={'GB_UKM' : 'GB'}).filter(items=countries)
       
    
    return generation

def import_eurostat_energy_balance_sheets(path):
    """
    Load and standardize the raw eurostat energy balance sheet files.

    Parameters
    ----------
    path : Path to data directory


    """
    
    
    # combining path and .xlsb data
    
    filenames = sorted(glob.glob(path + "/*.xlsb"))
    
    # import xlsb files
    # using pd.concat function as import function to append data to dataframe
    # encoding: "utf-16" see entso-e documentation
    # colum selection is possible by using "usecols=['DateTime','ResolutionCode','AreaCode','AreaTypeCode','GenerationUnitEIC',...]" 
    
    entsoe_pp_timeseries = pd.concat((pd.read_csv(f, sep='\t', encoding='utf-16', index_col = 3) for f in filenames))
    
    entsoe_pp_timeseries.drop(columns=["Year","Month","Day"], inplace=True)
    
    entsoe_pp_timeseries.index = pd.to_datetime(entsoe_pp_timeseries.index)

    #set generation and consumtion as absolut value (assuming that the negative entries are incorrect)
    entsoe_pp_timeseries['ActualGenerationOutput'] = entsoe_pp_timeseries.ActualGenerationOutput.abs()
    
    entsoe_pp_timeseries['ActualConsumption'] = entsoe_pp_timeseries.ActualConsumption.abs()

    return entsoe_pp_timeseries



df = pd.read_excel(io=input_directory_path + '\DE-Energy-balance-sheets-June-2020-edition_1.xlsb', sheet_name='2018', engine='pyxlsb')