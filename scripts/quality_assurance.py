import os
import yaml
import netCDF4
import numpy as np
import xarray as xr
import pandas as pd
from datetime import datetime, timezone
from functions import log, advanced_quality_flags


log("Performing advanced quality check")
with open("scripts/input_python.yaml", "r") as f:
    directories = yaml.load(f, Loader=yaml.FullLoader)

folder = directories["Level1_dir"]
filelist = os.listdir(directories["Level1_dir"])
filelist.sort()
log("Reading Level 1 data")
df = pd.DataFrame()
for file in filelist:
    file_path = folder + file
    ds = xr.open_dataset(file_path)
    df = df.append(ds.to_dataframe())
    ds.close()
df = df.reset_index()
mask = ~np.isnat(df["time"])
df["time"][mask] = df["time"][mask].apply(lambda x: datetime.timestamp(datetime.strptime(str(x), '%Y-%m-%d %H:%M:%S').replace(tzinfo=timezone.utc)))

log("Apply advance quality checks to data")
advanced_df = advanced_quality_flags(df, json_path="quality_assurance.json")

log("Update NetCDF files with new QA")
for file in filelist:
    file_path = os.path.join(folder, file)
    dset = netCDF4.Dataset(file_path, 'r+')
    idx = np.where((advanced_df["time"] >= dset["time"][0]) & (advanced_df["time"] <= dset["time"][-1]))[0]
    for var in dset.variables:
        if "_qual" in var:
            dset[var][:] = np.array(advanced_df[var][idx], dtype=bool)
    dset.close()
