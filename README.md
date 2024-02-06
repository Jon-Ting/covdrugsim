# CovDrugSim

[![ci-cd](https://github.com/Jon-Ting/covdrugsim/actions/workflows/ci-cd.yml/badge.svg)](https://github.com/Jon-Ting/covdrugsim/actions/workflows/ci-cd.yml)

## Description

`CovDrugSim` is a package that provides functionalities to automate quantum mechanical calculations and molecular dynamics simulations of covalent drugs.

## Features

### Aims
* Automatic creation of high-performance computing cluster submission files to run Gaussian calculations.
* Automatic analysis of molecular dynamics simulation trajectories.

### Under Development
* Complete example.ipynb.

## Installation

Use `pip` or `conda` to install `CovDrugSim`:

```bash
$ pip install covdrugsim
```
```bash
$ conda install -c conda-forge covdrugsim
```

## Usage

`covdrugsim` can be used to conduct quantum mechanical calculations and molecular dynamics simulations as follows:

```python
from covdrugsim.qmCalc.genScript import genAllScripts

targetDirPath = '/mnt/c/Users/JonTing/exampleXYZs'  # Absolute path to the directories containing all of your xyz files to be run
genAllScripts(targetDirPath, verbose=True)
```
Check out the [notebook tutorial](https://github.com/Jon-Ting/covdrugsim/blob/main/docs/example.ipynb) for further explanations and demonstrations!

Descriptions of source codes:
### Quantum Mechanical Calculations (qmcalc)

#### unitConv
unitConv.py - Interconverts between kinetics and thermodynamic quantities (dGbarr, k, t_half, RT).

#### runGaussian
* settings.py - Contains variables for different type of Gaussian jobs that are used by prepGaussian.py.
* admin.py - Group files with the same names (before extension, e.g. abc.inp is the same as abc.xyz) into individual directories.
* prepGaussian.py - Batch generation of Gaussian input files and job submission files on HPCs with PBS Scheduler.
* tabulate.py - Batch tabulation of interested values from Gaussian (version 16) output files into an Excel file.
* gsub.sh - Batch submission of Gaussian QM calculation jobs on HPCs.

Typical workflow for a mechanism-based project where flexible molecules are involved would be:
1) Conduct conformational searches on the species along the reaction coordinate (using MacroModel).
2) Export all conformers within 3 kcal/mol of the lowest energy structure to a directory in .xyz format. The naming convention is very important, be consistent, but make sure each conformer has a different name (I do this by adding numbers at the end of their names, signifying their ranks from the conformational searches).
3) Change your input directory in admin.py to where you store the coordinate files and run it. This will group all of the conformers into individual directories.
4) Change your input directory in prepGaussian.py to the same location and run it. This will generate the Gaussian input files and job submission files in the corresponding directory. Make sure you check at least a few of the files generated to see that you got the charges, spacing at the end of file, solvents, resources requested, etc right. I named all of the Gaussian job submission jobs with \*.sh, feel free to change it according to your preference (Line 52 in prepGaussian.py).
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
- bbRMSD.py plots the RMSD of Bruton's Tyrosine Kinease (BTK) backbones over time, for the purpose of checking the stability of the simulations.
- hbondAnalysis.py plots the distribution of the number of hydrogen bonds between BTK backbones over time.
- ligDihedral.py plots the distribution of the critical C=C-C=O dihedral angle near BTK active site over time.
- SCbondDist.py plots the distances between the reacting S and C atoms over time.
- sumCharge.py sums up the charges to aid in the parameterisation of non-standard amino acids.
- prepMTB.py was written during an attempt to map the unbound ligand to covalently bound ligand. Was not utilised in the end.

## Documentation

Detailed documentation and usage examples are hosted by [Read the Docs](https://covdrugsim.readthedocs.io/en/latest/).

## Contributing

`CovDrugSim` appreciates your enthusiasm and welcomes your expertise! 

Please check out the [contributing guidelines](https://github.com/Jon-Ting/covdrugsim/blob/main/CONTRIBUTING.md) and 
[code of conduct](https://github.com/Jon-Ting/covdrugsim/blob/main/CONDUCT.md). 
By contributing to this project, you agree to abide by its terms.

## License

The project is distributed under an [MIT License](https://github.com/Jon-Ting/covdrugsim/blob/main/LICENSE).

## Credits

The package was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) using the 
The codes were written by [Jonathan Yik Chang Ting](https://github.com/Jon-Ting) for [University of Queensland Bachelors of Advanced Science (Honours)](https://study.uq.edu.au/study-options/programs/bachelor-advanced-science-honours-2516) [CHEM6511](https://my.uq.edu.au/programs-courses/course.html?course_code=CHEM6511) under the title "[Molecular Modelling of Reversible Covalent Inhibition of Bruton’s Tyrosine Kinase by Cyanoacrylamides](https://github.com/Jon-Ting/Molecular-Modelling-of-Reversible-Covalent-Inhibition-of-Brutons-Tyrosine-Kinase-by-Cyanoacrylamide)". Click on the title to see the details of the project.

## Contact

Email: `Jonathan.Ting@anu.edu.au`/`jonting97@gmail.com`

Feel free to reach out if you have any questions, suggestions, or feedback.

