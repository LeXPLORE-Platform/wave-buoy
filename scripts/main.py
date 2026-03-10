# -*- coding: utf-8 -*-
import os
import json
import argparse
from instruments import WaveBuoy1, WaveBuoy2
from general.functions import logger, files_in_directory
from functions import retrieve_new_files, merge_files

def main(server=False, logs=False, remove_api_data=False):
    repo = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    if logs:
        log = logger(os.path.join(repo, "logs/wavebuoy"))
    else:
        log = logger()
    log.initialise("Processing LéXPLORE wave buoy data")
    directories = {f: os.path.join(repo, "data", f) for f in ["Level0", "Level1", "failed"]}
    for directory in directories:
        os.makedirs(directories[directory], exist_ok=True)
    edited_files = []

    log.begin_stage("Collecting inputs")
    if server:
        log.info("Processing files from sftp server")
        directories["Level0"] = os.path.join(directories["Level0"], "v2")
        os.makedirs(directories["Level0"], exist_ok=True)
        if not os.path.exists(os.path.join(repo, "creds.json")):
            raise ValueError("Credential file required to retrieve live data from the fstp server.")
        with open(os.path.join(repo, "creds.json"), 'r') as f:
            creds = json.load(f)
        new_files = retrieve_new_files(directories["failed"],
                                       creds, server_location="data/WaveBuoy",
                                       filetype=".csv", remove=remove_api_data, overwrite=True)
        files = merge_files(directories["Level0"], new_files)
        edited_files = edited_files + files
    else:
        files = files_in_directory(directories["Level0"])
        files.sort()
        log.info("Reprocessing complete dataset from {}".format(directories["Level0"]))
    log.end_stage()

    log.begin_stage("Processing data to L1")
    for file in files:
        if "v1" in file:
            sensor = WaveBuoy1(log=log)
            version = "v1"
        elif "v2" in file:
            sensor = WaveBuoy2(log=log)
            version = "v2"
        else:
            continue

        if sensor.read_data(file):
            sensor.quality_assurance(file_path="notes/quality_assurance.json")
            edited_files.extend(sensor.export(directories["Level1"], f"L1_WaveBuoy_{version}", output_period="weekly"))
    log.end_stage()

    return edited_files

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--server', '-s', help="Collect and process new files from FTP server", action='store_true')
    parser.add_argument('--logs', '-l', help="Write logs to file", action='store_true')
    args = vars(parser.parse_args())
    main(server=args["server"], logs=args["logs"])