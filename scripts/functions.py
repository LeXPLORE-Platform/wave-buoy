import json
import numpy as np
from envass import qualityassurance
from datetime import datetime
import copy

def copy_variables(variables_dict):
    var_dict = dict()
    for var in variables_dict:
        var_dict[var] = variables_dict[var][:]
    nc_copy = copy.deepcopy(var_dict)
    return nc_copy
    
def log(str, indent=0, start=False):
    if start:
        out = "\n" + str + "\n"
        with open("log.txt", "w") as file:
            file.write(out + "\n")
    else:
        out = datetime.now().strftime("%H:%M:%S.%f") + (" " * 3 * (indent + 1)) + str
        with open("log.txt", "a") as file:
            file.write(out + "\n")
    print(out)

    
def error(str):
    out = datetime.now().strftime("%H:%M:%S.%f") + "   ERROR: " + str
    with open("log.txt", "a") as file:
        file.write(out + "\n")
    raise ValueError(str)


def find_closest_index(arr, value):
    return min(range(len(arr)), key=lambda i: abs(arr[i] - value))


def is_number(n):
    try:
        float(n)
    except ValueError:
        return False
    else:
        return True


def json_converter(quality_assurance_dict):
    for key in quality_assurance_dict:
        for check_type in quality_assurance_dict[key]:   
            for check in quality_assurance_dict[key][check_type]:
                if "now" in quality_assurance_dict[key][check_type][check]:
                    quality_assurance_dict[key][check_type][check][1] = datetime.now().timestamp()
                if quality_assurance_dict[key][check_type][check] == "True":
                    quality_assurance_dict[key][check_type][check] = True
    return quality_assurance_dict


def isnt_number(n):
    try:
        float(n)
    except ValueError:
        return True
    else:
        return False


def advanced_quality_flags(df, json_path="quality_assurance.json"):
    """
        input :
            - df is a dataframe of level 1B where basic check have been performed
            - json path: path for the advanced quality check json file, produced by the jupyter notebook
        output:
            - dictionnary where the dataframe is stored with updated advanced quality checks
        """
    quality_assurance_dict = json.load(open(json_path))
    var_name = quality_assurance_dict.keys()
    advanced_df = df.copy()
    for var in var_name:
        if quality_assurance_dict[var]:
            qa = qualityassurance(np.array(df[var]), np.array(df["time"]), **quality_assurance_dict[var]["advanced"])
            advanced_df[var + "_qual"][np.array(qa, dtype=bool)] = 1
    return advanced_df
