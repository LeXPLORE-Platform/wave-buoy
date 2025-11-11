# -*- coding: utf-8 -*-

import netCDF4
import pandas as pd
import numpy as np
import os
from datetime import datetime, date
import datetime as dt
import json
from functions import log, json_converter, copy_variables
from dateutil.relativedelta import relativedelta
from envass import qualityassurance 


class surfacewaves(object):
    def __init__(self):
        self.id = ""
        self.folder = ""
        self.data = {}
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
            'time': {'var_name': 'time', 'dim': ('time',), 'unit': 'seconds since 1970-01-01 00:00:00','longname': 'time'},
            'hs': {'var_name': 'hs', 'dim': ('time',), 'unit': 'm', 'longname': 'wave height'},
            'tp': {'var_name': 'tp', 'dim': ('time',), 'unit': 's', 'longname': 'wave period'},
            'wd': {'var_name': 'wd', 'dim': ('time',), 'unit': 'deg', 'longname': 'wave direction'},
            'h10': {'var_name': 'h10', 'dim': ('time',), 'unit': 'm', 'longname': 'highest 10% wave heights'},
            # 'heading': {'var_name': 'heading', 'dim': ('time',), 'unit': 'deg', 'longname': 'wave direction'},
            # 'mwd': {'var_name': 'mwd', 'dim': ('time',), 'unit': 'deg', 'longname': 'mean wave direction'},
            # 'hmax': {'var_name': 'hmax', 'dim': ('time',), 'unit': 'm', 'longname': 'max wave height'},
        }
            
    def to_netcdf(self, folder, title, time_label="timestamp", output_period="weekly"):
        if not os.path.exists(folder):
            os.makedirs(folder)

        time_arr = self.data[time_label]
        dt_min = datetime.utcfromtimestamp(np.nanmin(time_arr))
        dt_max = datetime.utcfromtimestamp(np.nanmax(time_arr))

        if type(output_period) == int: 
            start = (dt_min - dt.timedelta(days=dt_min.weekday())).replace(hour=0, minute=0, second=0, microsecond=0)
            td = dt.timedelta(days=output_period)
        elif output_period == "daily": 
            start = (dt_min - dt.timedelta(days=dt_min.weekday())).replace(hour=0, minute=0, second=0, microsecond=0)
            td = dt.timedelta(days=1)
        elif output_period == "weekly":
            start = (dt_min - dt.timedelta(days=dt_min.weekday())).replace(hour=0, minute=0, second=0, microsecond=0)
            td = dt.timedelta(weeks=1)
        elif output_period == "monthly":
            start = dt_min.replace(day=1, hour=0, minute=0, second=0)
            td = relativedelta(months=+1)
        elif output_period == "yearly":
            start = dt_min.replace(month=1, day=1, hour=0, minute=0, second=0)
            td = relativedelta(year=+1)
        elif output_period == "profile":
            start = dt_min
            td = dt_max-dt_min
        else:
            log("Output periods {} not defined.".format(output_period))
        while start < dt_max:
            end = start + td
            s = datetime.timestamp(start)
            e = datetime.timestamp(end)

            filename = "{}_{}.nc".format(title, start.strftime('%Y%m%d'))
            out_file = os.path.join(folder, filename)
            log("Writing data from {} until {} to NetCDF file {}".format(start, end, filename), 2)

            if os.path.isfile(out_file):
                nc = netCDF4.Dataset(out_file, mode='a', format='NETCDF4')

                nc_time_arr = np.array(nc.variables["time"][:])

                if np.all(np.isin(time_arr, nc_time_arr)):
                    log("Duplicated run, no data added", 2)
                    nc.close()
                    start = start + td
                    continue
                else:
                    valid_time = (time_arr >= s) & (time_arr < e)
                    valid_duplicates = ~np.isin(time_arr, nc_time_arr)
                    valid = np.logical_and(valid_time, valid_duplicates)
                    combined_time = np.append(nc_time_arr, time_arr[valid])
                    order = np.argsort(combined_time)
                    
                    nc_copy = copy_variables(nc.variables)
                    
                    for key, values in self.variables.items():
                        data = self.data[key]
                        combined = np.append(nc_copy[key][:], data[valid])
                        out = combined[order]
                        nc.variables[key][:] = out

                    nc.close()

            else:
                nc = netCDF4.Dataset(out_file, mode='w', format='NETCDF4')

                for key in self.general_attributes:
                    setattr(nc, key, self.general_attributes[key])

                for key, values in self.dimensions.items():
                    nc.createDimension(values['dim_name'], values['dim_size'])

                for key, values in self.variables.items():
                    var = nc.createVariable(values["var_name"], np.float64, values["dim"], fill_value=np.nan)
                    var.units = values["unit"]
                    var.long_name = values["longname"]
                    var[:] = np.array(self.data[key])

                nc.close()

            start = start + td  

    def quality_flags(self, file_path, simple=True):
        quality_assurance_dict = json_converter(json.load(open(file_path)))
        for key, values in self.variables.copy().items():
            if (quality_assurance_dict[key]["advanced"]) or (quality_assurance_dict[key]["simple"]):
                name = key + "_qual"
                self.variables[name] = {'var_name': name, 'dim': values["dim"],
                                        'unit': '0 = nothing to report, 1 = more investigation',
                                        'longname': name, }
                data = np.array(self.data[key])
                if simple == True:
                    if np.isnan(data).all():
                        self.data[name] = np.ones(len(data))
                    else:
                        self.data[name] = qualityassurance(data, np.array(self.data["time"]), **quality_assurance_dict[key]["simple"])
                else: 
                    quality_assurance_all = dict(quality_assurance_dict[key]["simple"], **quality_assurance_dict[key]["advanced"])
                    if np.isnan(data).all():
                        self.data[name] = np.ones(len(data))
                    else:
                        self.data[name]= qualityassurance(np.array(self.data[key]), np.array(self.data["time"]), **quality_assurance_all)

    def read_data(self, file):
        log("Reading wave buoy data from: "+file, 3)
        if int(os.path.basename(file)[0:4]) > int(date.today().year):
            log("Year is greater than current year, not processing file.")
            return False
        try:
            df = pd.read_csv(file, sep = ";", header = None)
            df = df.iloc[:, 0: 9]
            df.columns = ["yymmdd", "hhmmss", "heading", "hs", "tp", "wd", "mwd", "hmax", "h10"]
            df["time_tp"] = pd.to_datetime(df['yymmdd'] + ' ' + df['hhmmss'])
            df["time"] = df["time_tp"].apply(lambda x: datetime.timestamp(x))
            df.drop_duplicates(subset = 'yymmdd', inplace = True)
            df.sort_values("time", inplace=True)
            df.reset_index(inplace=True, drop=True)
            df["datetime"] = pd.to_datetime(df['time'], unit='s')
            df["heading"] = pd.to_numeric(df["heading"], errors='coerce')
            df["tp"] = pd.to_numeric(df["tp"], errors='coerce')
            df["wd"] = pd.to_numeric(df["wd"], errors='coerce')
            df["mwd"] = pd.to_numeric(df["mwd"], errors='coerce')
            df["hmax"] = pd.to_numeric(df["hmax"], errors='coerce')
            df["h10"] = pd.to_numeric(df["h10"], errors='coerce')
            self.data = df
            self.time = df["time"]
            log("Successfully read data", 3)
        except Exception as e:
            log("Failed to parse data", e)
            return False
        return True

    @staticmethod
    def addDataNetCDF(data, idx, ncfile, **kwargs):
        if "dim" in kwargs.keys():
            ndim = len(kwargs["dim"])
        else:
            ndim = 0        

        var = ncfile.variables[kwargs["var_name"]] 
        if ndim == 2:
            var[:, idx:] = data[:, idx:]
        elif ndim == 1:
            var[idx:] = data[idx:]
        else:
            var[:] = data
