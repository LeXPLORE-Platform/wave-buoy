import os
import yaml
import glob
import sys
from functions import log
from surfacewaves import surfacewaves

with open("scripts/input_python.yaml", "r") as f:
    directories = yaml.load(f, Loader=yaml.FullLoader)

log("Creating directories")
for directory in directories.values():
    if not os.path.exists(directory):
        os.makedirs(directory)

if len(sys.argv) == 1:
    files = os.listdir(directories["Level0_dir"])
    files = [os.path.join(directories["Level0_dir"], f) for f in files]
    files.sort()
    log("Reprocessing complete dataset from {}".format(directories["Level0_dir"]))
elif len(sys.argv) == 2:
    files = [str(sys.argv[1]).replace('\\', '/')]
    log("Live processing file {}".format(files[0]))

for file in files:
    log("Processing surface waves data", 1)
    S = surfacewaves()
    if S.read_data(file):
        S.quality_flags("quality_assurance.json")
        S.to_netcdf(directories["Level1_dir"], "L1", time_label="time", output_period="weekly")
        
        
        
        
        
