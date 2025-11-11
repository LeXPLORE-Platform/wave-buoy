# LéXPLORE Surface Waves

## Project Information

[LéXPLORE](https://lexplore.info) is a state-of-the-art research platform situated on Lake Geneva, dedicated to a wide range of limnological studies. This innovative platform is the result of a collaborative effort between five leading institutions: [Eawag](https://www.eawag.ch/en/), [EPFL](https://www.epfl.ch/en/), [INRAE](https://www6.lyon-grenoble.inrae.fr/carrtel/), [UNIGE](https://unige.ch), [UNIL](https://www.unil.ch/index.html). Since February 2019, the LéXPLORE platform is anchored at 110 m depth off the lake's north-shore (46°30'00.8"N 6°39'39.0"E).

The data presented here is part of the core dataset maintained by the technical team of LéXPLORE.
The data is used and displayed on the [Datalakes website](https://www.datalakes-eawag.ch/) where other related data or products can be visualised and downloaded.

The specific dataset contains raw and processed data recorded by a surface waves databuoy records. Data includes surface wave height, period and direction. 


**References**:

Wüest, A., Bouffard, D., Guillard, J., Ibelings, B. W., Lavanchy, S., Perga, M. ‐E., & Pasche, N. (2021). LéXPLORE: a floating laboratory on Lake Geneva offering unique lake research opportunities. Wiley Interdisciplinary Reviews: Water, 8(5), e1544 (15 pp.). https://doi.org/10.1002/wat2.1544

See also the [360° virtual tour](https://www.eawag.ch/repository/lexplore/index.htm)


## Citation
Bouffard, D., Cunillera, G, Fillon, R., Gios, M., Guillard, J., Ibelings, B., Keller, J., Lavanchy, S., Miesen, F., Pasche, N., Perga, M-E., Plüss, M., Quetin, P., Runnalls, J. (2024). Surface waves data and products from the LéXPLORE platform, Lake Geneva, 2022-2024,  2024. https://doi.org/10.25678/000D9J


## Keywords
LéXPLORE, Lake Geneva, Surface waves, Datalakes

## Sensors

The surface waves databuoy records at 60 minute intervals the surface waves characteristics (height, period, direction). 
The system is based on a MEMS (microelectromechanical system) technology that accounts for 3D motion, rotation, compass and heading in all dimensions.

### Surface waves (height, period, direction)
- **Brand, Model & SN**:    SeaView wave sensor, SVS603, SN wave01055
- **System integration**:   Sensor integrated in a Nexsens CB-450 databuoy, Nexsens X2 datalogger with 2.4Ghz radio telemetry
- **Accuracy**:             Significant wave height  (Hs): 1cm @ 0.1m; 2cm @ 1.5m; 10cm @ 25m
                            Period: 0.02sec @ 1sec; 0.04sec @ 2sec; 0.1sec @ 20sec
                            Wave direction: ±4 degrees 
- **Setup**:                sampling period: one datapoint every 60 min (17 min of measurement).  

Documentation regarding the instrument can be found in `notes`

## Geospatial Information

Before 17.10.2023, the buoy was located 60 m North - East of LéXPLORE: 46°30′02.311″N 6°39′41.261″E

Since 17.10.2023, the buoy is located 30 m South - West of LéXPLORE: 46°29′59.68″N 6°39′40.45″E 

## Temporal coverage 
- start: April 2022
- stop: live dataset

## Code

[![License: MIT][mit-by-shield]][mit-by]

:warning You need to have [git](https://git-scm.com/downloads) and [git-lfs](https://git-lfs.github.com/) installed in order to successfully clone the repository.

- Clone the repository to your local machine using the command: 

 `git clone https://renkulab.io/gitlab/lexplore/wave-buoy.git`
 
 Note that the repository will be copied to your current working directory.

- Use Python 3 and install the requirements with:

 `pip install -r requirements.txt`

 The python version can be checked by running the command `python --version`. In case python is not installed or only an older version of it, it is recommend to install python through the anaconda distribution which can be downloaded [here](https://www.anaconda.com/products/individual). 


### Process new data

In order to process new data locally on your machine the file path needs to be adapted to your local file system. The following steps are therefore necessary: 

- Edit the `scripts/input_batch.bat` file. Change all the directory paths to match your local file system. This file contains all the file paths necessary to launch the batch scripts `runfile.bat`.

- Edit the `scripts/input_python.py` file. Change all the directory paths to match your local file system. This file contains all the directories where the python script outputs data to.

To process new data, place the data in the input directory which you specified in the `scripts/input_batch.bat` file. Double-clicking on the `runfile.bat` file will automatically 
process all the data in the input directory and store the output in the directories specified in the `scripts/input_python.py` file. 

### Adapt/Extend data processing pipeline

The python script `scripts/main.py` defines the different processing steps while the python script `scripts/surfacewaves.py` contains the python class surfacewaves with all the corresponding 
class methods to process the data. To add a new processing or visualization step, a new class method can be created in the `surfacewaves.py` file and the step can be added in `main.py` file.
Both above mentioned python scripts are independent of the local file system.


## Data


### License

[![CC BY 4.0][cc-by-shield]][cc-by] 

This data is released under the Creative Commons license - Attribution - CC BY (https://creativecommons.org/licenses/by/4.0/). This license states that consumers ("Data Users" herein) may distribute, adapt, reuse, remix, and build upon this work, as long as they give appropriate credit, provide a link to the license, and indicate if changes were made.
 
The Data User has an ethical obligation to cite the data source (see the DOI number) in any publication or product that results from its use. Communication, collaboration, or co-authorship (as appropriate) with the creators of this data package is encouraged. 
 
Extensive efforts are made to ensure that online data are accurate and up to date, but the authors will not take responsibility for any errors that may exist in data provided online. Furthermore, the Data User assumes all responsibility for errors in analysis or judgment resulting from use of the data. The Data User is urged to contact the authors of the data if any questions about methodology or results occur. 


### Data Structure


- **Level 0**: Raw data collected from the different sensors.

- **Level 1**: Raw data stored to NetCDF file where attributes (such as sensors used, units, description of data, etc.) are added to the data, column with quality flags are added to the Level 1A data. Quality flag "1" indicates that the data point didn't pass the 
quality checks and further investigation is needed, quality flag "0" indicates that no further investigation is needed. Masked data can be found in the L1 product with the extention '_qual'


Netcdf file info
* Coordinates: time [UTC] 
* Data variables:
    * significant wave height, *hs* [m]
    * wave period, *tp* [s]
    * wave direction, *wd* [°]
    * highest 10% wave height, *h10* [m]

An example of visualisation of the Netcdf file is provided as Jupyter Notebook.

**Reading from NetCDF**.
There are a number of resources that give detailed information on how to read and interact with NetCDF files. Linked below are some suggested resources.

- Python		https://unidata.github.io/netcdf4-python/
- R		https://cran.r-project.org/web/packages/ncdf4/ncdf4.pdf


**Reading Time.** Datetime is in Unix time format (seconds since 01 Sept. 1970 [UTC]). *Warning*: the display in [Datalakes website](https://www.datalakes-eawag.ch/) is in local time but the downloaded data are always in UTC. Most languages have a function for parsing this format to a datetime object.

- Python		
```
from datetime import datetime 
dt = datetime.utcfromtimestamp(unixdatetime)
```
- R	
```
library(anytime)
dt <- anytime(unixdatetime)
```

## Quality assurance

Quality checks include but are not limited to range validation, data type checking and flagging missing data. The basic quality check is defined in the  'quality_assurance.json' file and include the following test:
* "time": numeric, bounds: [1514764800, "now"],
* "hs": numeric, bounds: [0, 5],
* "tp": numeric, bounds: [0, 40],
* "wd": numeric, bounds: [0, 360], 
* "h10": numeric, bounds: [0, 5].

Advanced quality assurance can be run using the `scripts/quality_assurance.py` function. In order to better define the quality assurance users can interact with the data and define new quality assurance checks in `notebooks/define_quality assurance.ipynb`.






###  Events 

Maintenance dates, interesting or surprising events, non identified by the basic quality check are listed in `notes/events`.
Check also the `notes/sensor_history`.

## Collaborators

- **Concept, finances, project management** Damien Bouffard, Bas Ibelings, Natacha Pasche, Marie-Elodie Perga, Serena Rasconi    
- **Installation, maintenance, data collection** Guillaume Cunillera, Mateo Gios, Roxane Fillon, Jeremy Keller, Sébastien Lavanchy, Floreana Miesen, Michael Plüss, Philippe Quetin
- **Data pipeline** Damien Bouffard, James Runnalls
- **Data review** Damien Bouffard

## Contact
- **Contact science** [Damien Bouffard](mailto:damien.bouffard@eawag.ch)
- **Contact software** [James Runnalls](mailto:james.runnalls@eawag.ch)
- **Contact tech** [Guillaume Cunillera](mailto:guillaume.cunillera@epfl.ch)




[cc-by]: http://creativecommons.org/licenses/by/4.0/
[cc-by-shield]: https://img.shields.io/badge/License-CC%20BY%204.0-g.svg?label=Data%20License
[mit-by]: https://opensource.org/licenses/MIT
[mit-by-shield]: https://img.shields.io/badge/License-MIT-g.svg?label=Code%20License
