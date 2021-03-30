INTRODUCTION
------------

This project is the Python version of the Z-Transform Osteometric Sorting method. 
Osteometric Sorting utilizes size and shape to sort bones from one another. 

 * For a full description of the methods used in this program:
https://onlinelibrary.wiley.com/doi/10.1111/1556-4029.13813


REQUIREMENTS
------------

This module requires the following modules:

 * Pandas (https://https://pandas.pydata.org/)
 * scikit-learn (https://https://scikit-learn.org/stable/)
 * statsmodels (https://www.statsmodels.org/stable/index.html) 

INSTALLATION
------------
 
The following are steps to install the Python Z-Transform Osteometric Sorting Program
on a Linux/Mac OS machine.

1. Clone this repo.
```sh
   git clone https://github.com/jwarsom/osteometrics.git
   ```
2. Create virtual environment (recommended) (https://docs.python.org/3/library/venv.html#)
```sh
   python3 -m venv /path/to/new/virtual/environment
   ```

3. Activate the virtual environment 
```sh
source /path/to/new/virtual/environment/bin/activate
   ```

4. Change into the osteometrics directory
```sh
cd /path/to/osteometrics
   ```
5. Install the osteometric sorting z-transform program
pip install -e . -r requirements.txt
   
## Usage

```sh
   python /path/to/osteometrics/osteometrics/osteometric_sorting.py 
   ```

Arguments

| Flag | Description | values |
| --- | --- | --- |
|input | The csv input file containing skeletal element metadata and measurements. | |
|reference | The csv file containing the skeletal element reference group data  | |
|p_method | The variant of z-transform osteometric sorting applied| 'uweightedZ', 'effectSizeZ', 'standardErrorZ'|
|alpha | Alpha level for z-transform osteometric sorting | default: 0.1 |
|loocv | Perform leave-one-out cross validation of the reference data| default: false | 
|time | Report runtime | default: false |

Input File Format:
The z-transform program is expect the input and reference csv files to have the following fields

| Field | Description | values |
| --- | --- | --- |
|Id | The skeletal element Id | |
| Side | The skeletal element side | Left, Right|
| Element | The type of skeletal element | Clavicle, Femur, Fibula, Humerus, Os coxa, Radius, Scapula, Tibia, Ulna |
| Measurement_Columns| Each column represents a single measurement type | See below for the measurement column names for each skeletal element type. All fields are required for each element type but may be left blank. |

Clavicle
* 'Cla_01', 'Cla_04', 'Cla_05'

Femur
* 'Fem_01', 'Fem_02', 'Fem_03', 'Fem_04', 'Fem_05', 'Fem_06', 'Fem_07'

Fibula 
* 'Fib_01', 'Fib_02'

Humerus
* 'Hum_01', 'Hum_02', 'Hum_03', 'Hum_04', 'Hum_05'

Os coxa
* 'Osc_01', 'Osc_02'

Radius
* 'Rad_01', 'Rad_05', 'Rad_06'

Scapula
* 'Sca_01', 'Sca_02'

Tibia
* 'Tib_01', 'Tib_02', 'Tib_03', 'Tib_04', 'Tib_05'

Ulna
* 'Uln_01', 'Uln_04', 'Uln_05', 'Uln_06'

For a description of each of these fields visit: https://cora-docs.readthedocs.io/en/latest/forensics-anthro-guide/measurements/