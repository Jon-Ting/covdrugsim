# covdrugsim

Quantum mechanical calculations and molecular dynamics simulations of covalent drugs.

Written by Jonathan Yik Chang Ting (Student ID: 44254124) for University of Queensland Bachelors of Advanced Science Honours Project (CHEM6511) in 2019.
Project Title: Molecular Modelling of Reversible Covalent Inhibition of Bruton’s Tyrosine Kinase by Cyanoacrylamides

## Installation

```bash
$ pip install covdrugsim
```

## Usage

`covdrugsim` can be used to conduct quantum mechanical calculations and molecular dynamics simulations as follows:

```python
from covdrugsim.qmCalc import qmCalc
from covdrugsim.mdSim import mdSim
import matplotlib.pyplot as plt

filePath = "test.txt"  # Path to your file
qmCalc(filePath)
mdSim(filePath)
plt.show()
```


Descriptions of source codes:
### Quantum Mechanical Calculations (qmcalc)

#### unitConv
unitConv.py - Interconverts between kinetics and thermodynamic quantities (dGbarr, k, t_half, RT).

#### runGaussian
settings.py - Contains variables for different type of Gaussian jobs that are used by prepGaussian.py.
admin.py - Group files with the same names (before extension, e.g. abc.inp is the same as abc.xyz) into individual directories.
prepGaussian.py - Batch generation of Gaussian input files and job submission files on HPCs with PBS Scheduler.
tabulate.py - Batch tabulation of interested values from Gaussian (version 16) output files into an Excel file.
gsub.sh - Batch submission of Gaussian QM calculation jobs on HPCs.

Typical work flow for a mechanism-based project where flexible molecules are involved would be:
1) Conduct conformational searches on the species along the reaction coordinate (using MacroModel).
2) Export all conformers within 3 kcal/mol of the lowest energy structure to a directory in .xyz format. The naming convention is very important, be consistent, but make sure each conformer has a different name (I do this by adding numbers at the end of their names, signifying their ranks from the conformational searches).
3) Change your input directory in admin.py to where you store the coordinate files and run it. This will group all of the conformers into individual directories.
4) Change your input directory in prepGaussian.py to the same location and run it. This will generate the Gaussian input files and job submission files in the corresponding directory. Make sure you check at least a few of the files generated to see that you got the charges, spacing at the end of file, solvents, resources requested, etc right. I named all of the Gaussian job submission jobs with *.sh, feel free to change it according to your preference (Line 52 in prepGaussian.py).
5) Copy the directories across to the HPCs (Raijin/Gadi/Tinaroo/Awoonga, NOTE: The details for job submissions on Raijin and RCC HPCs are different, specify the cluster before running prepGaussian.py in Step 4).
6) Change directory to the directory that contains all the conformers subdirectories and run 'gsub.sh' (Make sure it's an executable, if you can't run it, use chmod to change it). This will submit all of the Gaussian submission jobs to the HPC. Note that prior to this you need to adjust Line 6 in the gsub.sh file to the naming convention you give to your Gaussian submit files if you have changed them in the prepGaussian.py.
7) After the jobs are done, copy them over to your local machine.
8) Change your input directory in tabulate.py to the directory that contains all the conformers and run it. Note that you need to have the Python package pandas installed for it to work.

#### visAnalysis
energyLeveller.py - Draws energy profile diagrams.
plotConfig.py - Stores configuration for figure-plotting functions.
plotFigs.py - Plots figures for QM data analysis.


### Molecular Dynamics Simulations (mdsim)
- config.py contains some variables that are used repetitively for almost all files.
- baseID.py plots the distances between potential base species and the targeted protons.
- bbRMSD.py plots the RMSD of BTK backbones over time, for the purpose of checking the stability of the simulations.
- hbondAnalysis.py plots the distribution of the number of hydrogen bonds between BTK backbones over time.
- ligDihedral.py plots the distribution of the critical C=C-C=O dihedral angle near BTK active site over time.
- SCbondDist.py plots the distances between the reacting S and C atoms over time.
- sumCharge.py sums up the charges to aid in the parameterisation of non-standard amino acids.
- prepMTB.py was written during an attempt to map the unbound ligand to covalently bound ligand. Was not utilised in the end.


## Contributing

Interested in contributing? Check out the contributing guidelines. Please note that this project is released with a Code of Conduct. By contributing to this project, you agree to abide by its terms.

## License

`covdrugsim` was created by Jonathan Yik Chang Ting. It is licensed under the terms of the MIT license.

## Credits

`covdrugsim` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter).
