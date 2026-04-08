# -*- coding: utf-8 -*-
import os
import math
import netCDF4
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta, timezone
from general.functions import GenericInstrument


class WaveBuoy(GenericInstrument):
    def __init__(self, *args, **kwargs):
        super(WaveBuoy, self).__init__(*args, **kwargs)
        self.general_attributes = {
            "institution": "Eawag",
            "source": "Surface waves",
            "references": "LéXPLORE common instruments damien.bouffard@eawag.ch",
            "history": "See history on Renku",
            "conventions": "CF 1.7",
            "comment": "Surface waves measurements collected on Lexplore Platform in Lake Geneva",
            "title": "Lexplore Surface Waves Measurements"
        }

        self.dimensions = {
            'time': {'dim_name': 'time', 'dim_size': None}
        }

        self.variables = {
            'time': {'var_name': 'time', 'dim': ('time',), 'unit': 'seconds since 1970-01-01 00:00:00','long_name': 'time'},
            'hs': {'var_name': 'hs', 'dim': ('time',), 'unit': 'm', 'long_name': 'wave height'},
            'tp': {'var_name': 'tp', 'dim': ('time',), 'unit': 's', 'long_name': 'wave period'},
            'wd': {'var_name': 'wd', 'dim': ('time',), 'unit': 'deg', 'long_name': 'wave direction'},
            'h10': {'var_name': 'h10', 'dim': ('time',), 'unit': 'm', 'long_name': 'highest 10% wave heights'},
            'heading': {'var_name': 'heading', 'dim': ('time',), 'unit': 'deg', 'long_name': 'heading'},
            'mwd': {'var_name': 'mwd', 'dim': ('time',), 'unit': 'deg', 'long_name': 'mean wave direction'},
            'hmax': {'var_name': 'hmax', 'dim': ('time',), 'unit': 'm', 'long_name': 'max wave height'},
            'te': {'var_name': 'te', 'dim': ('time',), 'unit': 's', 'long_name': 'energy period'},
            'pitch': {'var_name': 'pitch', 'dim': ('time',), 'unit': 'deg', 'long_name': 'pitch'},
            'roll': {'var_name': 'roll', 'dim': ('time',), 'unit': 'deg', 'long_name': 'roll'},
        }


class WaveBuoy1(WaveBuoy):
    def read_data(self, file):
        self.log.info("Reading data from {}".format(file), 1)
        try:
            df = pd.read_csv(file, sep=";", header=None)
            if len(df) == 0:
                self.log.info("No data found in {}".format(file), 1)
                return False
            df.columns = ["DATE", "TIME", "heading", "hs", "tp", "wd", "mwd", "hmax", "h10", "pitch", "roll"]
            df['time'] = pd.to_datetime(df["DATE"] + " " + df["TIME"], format='%Y-%m-%d %H:%M:%S',
                                        utc=True).values.astype(
                float) / 10 ** 9
            df = df.sort_values(by=['time'])
            now_ts = datetime.now(timezone.utc).timestamp()
            start_2022_ts = datetime(2022, 1, 1, tzinfo=timezone.utc).timestamp()
            df = df[(df['time'] >= start_2022_ts) & (df['time'] <= now_ts)]
            
            if len(df) == 0:
                self.log.info("No valid data found after filtering {}".format(file), 1)
                return False
            
            empty = np.empty((len(df)))
            empty[:] = np.nan
            for variable in self.variables:
                if variable in df.columns:
                    self.data[variable] = np.array(df[variable].values)
                else:
                    self.data[variable] = empty.copy()
        except Exception as e:
            self.log.info("Failed to read data from {}".format(file), indent=1)
            return False
        return True


class WaveBuoy2(WaveBuoy):
    def read_data(self, file):
        self.log.info("Reading data from {}".format(file), 1)
        try:
            df = pd.read_csv(file, header=None)
            if len(df) == 0:
                self.log.info("No data found in {}".format(file), 1)
                return False
            df.columns = ["DATE", "TIME", "heading", "hs", "tp", "wd", "mwd", "hmax", "h10", "te", "pitch", "roll"]
            df['time'] = pd.to_datetime(df["DATE"] + " " + df["TIME"], format='%Y-%m-%d %H:%M:%S', utc=True).values.astype(
                    float) / 10 ** 9
            df = df.sort_values(by=['time'])
            
            # Filter out data: future timestamps and before 2022
            now_ts = datetime.now(timezone.utc).timestamp()
            start_2022_ts = datetime(2022, 1, 1, tzinfo=timezone.utc).timestamp()
            df = df[(df['time'] >= start_2022_ts) & (df['time'] <= now_ts)]
            
            if len(df) == 0:
                self.log.info("No valid data found after filtering {}".format(file), 1)
                return False
            
            empty = np.empty((len(df)))
            empty[:] = np.nan
            for variable in self.variables:
                if variable in df.columns:
                    self.data[variable] = np.array(df[variable].values)
                else:
                    self.data[variable] = empty.copy()
        except Exception as e:
            self.log.info("Failed to read data from {}".format(file), indent=1)
            return False
        return True

