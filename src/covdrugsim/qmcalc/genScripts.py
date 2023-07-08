import os
from os.path import isdir

from covdrugsim.qmcalc.constants import keywordDict
from covdrugsim.qmcalc.admin import groupFilesIntoDir


def writeGaussInpFile(name, inpDirPath, 
                      keywordLine=None, 
                      mem=4000, ncpus=8, 
                      combination=' m062x/6-311+g(d,p)', scrf=' scrf=(cpcm,solvent=water)', freq=' freq', grid=' opt=calcfc int(grid=ultrafine)', 
                      charge=0, spin=1,
                      verbose=False):
    """
    Generate a Gaussian input file based on specified inputs.

    Parameters
    ----------
    name : str
        Name of the jobscript, also used for input and output file of the software to run.
    inpDirPath : str
        Directory path to store the jobscript.
    mem : Union[int,str]
        Amount of memory to request for the Gaussian job.
    ncpus : Union[int,str]
        Number of CPUs to request for the job.
    combination : str
        Keyword for DFT method and basis set specification in Gaussian.
    scrf : str
        Keyword for solvent specification in Gaussian.
    freq : str
        Keyword for force constant and resulting vibrational frequencies computation in Gaussian.
    grid : str
        Keyword for grid specification in Gaussian.
    charge : int
        Charge of the molecule (pay special attention if you have a transition state).
    spin : int
        Spin of the molecule.
    verbose : bool
        Whether to display details of the process.
    """
    with open(f"{inpDirPath}/{name}.inp", 'w') as inpFile:
        inpFile.write(f"%mem={mem}mb\n%nprocshared={ncpus}\n%chk={name}.chk\n")
        if keywordLine:
            inpFile.write(keywordLine)
        else:
            inpFile.write(f"#{combination}{scrf}{grid}{freq}")
        inpFile.write(f"\n\n{name}\n\n{charge} {spin}\n")
        with open(f"{inpDirPath}/{name}.xyz", 'r') as xyzFile:
            lineList = xyzFile.readlines()

            # Couldn't recount why this was implemented, to be looked into
            hasEnergyName = 'Energy' in lineList[1] or 'TI' in lineList[1] or 'Name' in lineList[1]
            hasPath = ':' in lineList[1]
            hasBlank = '\n' in lineList[1]
            for (i, line) in enumerate(lineList):
                if hasEnergyName and (i > 1):
                    inpFile.write(line)
                elif hasPath and (i > 1):
                    inpFile.write(f"\n{line}") if i == 2 else inpFile.write(line)
                elif hasBlank and (i > 1):
                    inpFile.write(line)
                elif not(hasEnergyName) and not(hasPath) and not(hasBlank) and (i > 0):
                    inpFile.write(line)
            inpFile.write('\n')
    if verbose:
        print(f"    Generated Gaussian input file for {name}!")


def writeHPCJobScript(name, inpDirPath='.', 
                      scheduler='pbs', cluster='gadi', 
                      ncpus=8, walltime='24:00:00', vmem=8000, jobfs=9000, project='p39', software='g16', version='c01',
                      verbose=False):
    """
    Generate a HPC jobscript based on specified inputs. 

    Parameters
    ----------
    name : str
        Name of the jobscript, also used for input and output file of the software to run.
    inpDirPath : str
        Directory path to store the jobscript.
    scheduler : str
        Scheduler to submit the job to.
    cluster : {'gadi', 'uq-rcc'}
        Cluster to run the job on.
    ncpus : Union[int,str]
        Number of CPUs to request for the job.
    walltime : str
        Wall time to request for the job.
    vmem : Union[int,str]
        Amount of memory to request for the HPC job.
    jobfs : Union[int,str]
        Amount of Jobfs memory to request for the job.
    project : str
        Project ID on NCI Gadi, only used if 'cluster' = 'gadi'.
    software : str
        Gaussian software name to use for the job.
    version : str
        Version of the Gaussian software.
    verbose : bool
        Whether to display details of the process.
    
    Notes
    -----
    - If your HPC system does not use PBS jobscript modifications will be needed for the function (open an issue on GitHub!).
    - Feel free to change the default values according to your most commonly used settings.
    """
    with open(f"{inpDirPath}/{name}.sh", 'w') as f:
        if scheduler == 'pbs':
            if cluster == 'gadi':
                f.write('#!/bin/bash\n#PBS -l wd\n#PBS -q normal\n')
                f.write(f"#PBS -l walltime={walltime},mem={vmem}mb,ncpus={ncpus},software={software},jobfs={jobfs}mb,storage=scratch/{project}")
                f.write(f"\n\nmodule load gaussian/{software}{version}")
                f.write(f"\n{software} < {name}.inp > {name}.out 2>&1")
            elif cluster == 'uq-rcc':
                f.write(f"#!/bin/bash\n#PBS -S /bin/bash\n#PBS -l walltime={walltime}\n#PBS -A UQ-SCI-SCMB\n")
                f.write(f"#PBS -l select=1:ncpus={ncpus}:mem={vmem}MB")
                f.write('\n\ncd $PBS_O_WORKDIR')
                f.write(f"\n\nmodule load gaussian/{software}-{version.upper()}-bash")
                f.write(f"\n{software} < {name}.inp > {name}.out")
            else:
                raise Exception(f"Cluster {cluster} not recognised/accommodated for yet!")
        else: 
            raise Exception(f"Scheduler {scheduler} not recognised/accommodated for yet!")
    if verbose:
        print(f"    Generated HPC job script for {name}!")


def genAllScripts(inpDirPath,
                  keywordLine=None,
                  method='m062x', basisSet='6-311+g(d,p)', solvent='water', solventModel='cpcm',
                  mem=4000, ncpus=8, calcType='GOVF', charge=0, spin=1,
                  scheduler='pbs', cluster='gadi',
                  walltime='24:00:00', vmem=8000, jobfs=9000, project='p39', software='g16', version='c01',
                  verbose=False):
    """
    Generate Gaussian input job files and submission files for molecules under all directories under a specified directory ('inpDirPath').

    Parameters
    ----------
    inpDirPath : str
        Directory path to the input directories.
    keywordLine : Union[str,None]
        The line of keywords specification for Gaussian job, the other input arguments will be used to compose the line if it is not provided.
    method : str
        Keyword for DFT method specification in Gaussian.
    basisSet : str
        Keyword for basis set specification in Gaussian.
    solvent : str
        Keyword for solvent specification in Gaussian.
    solventModel : str
        Keyword for SCRF method specification in Gaussian.
    mem : Union[int,str]
        Amount of memory to request for the Gaussian job.
    ncpus : Union[int,str]
        Number of CPUs to request for the job.
    calcType : str
        Type of calculation (e.g. 'GOVF' for normal geometry optimisation; 'TSGOVF' for transition state geometry optimisation, 
        'SPEiS' for single point energy calculation, refer to 'keywordDict' for other options).
    charge : int
        Charge of the molecule (pay special attention if you have a transition state).
    spin : int
        Spin of the molecule.
    scheduler : str
        Scheduler to submit the job to.
    cluster : {'gadi', 'uq-rcc'}
        Cluster to run the job on.
    walltime : str
        Wall time to request for the job.
    vmem : Union[int,str]
        Amount of memory to request for the HPC job.
    jobfs : Union[int,str]
        Amount of Jobfs memory to request for the job.
    software : str
        Gaussian software name to use for the job.
    version : str
        Version of the software.
    verbose : bool
        Whether to display details of the process.

    Notes
    -----
    - Users should organise their directories such that a directory is created for each molecule to be calculated, and all of these directories should be placed under the specified directory that this function takes in ('inpDirPath')
    """
    if verbose:
        print(f"\nGenerating all job scripts for molecules under directories under {inpDirPath}...")
    assert calcType in keywordDict.keys(), 'Calculation type not known!'

    molecules = [g for g in os.listdir(inpDirPath) if isdir(f"{inpDirPath}/{g}")]
    if len(molecules) == 0:
        groupFilesIntoDir(inpDirPath, verbose=verbose)
        molecules = [g for g in os.listdir(inpDirPath) if isdir(f"{inpDirPath}/{g}")]

    for name in molecules:
        if verbose:
            print(f"  Processing {name}...")
        moleculeDir = f"{inpDirPath}/{name}"
        combination = f" {method}/{basisSet}"
        scrf = f" scrf=({solventModel},solvent={solvent})"
        freq = keywordDict[calcType]['freq']
        grid = keywordDict[calcType]['grid']
        writeGaussInpFile(name, moleculeDir, 
                          keywordLine, 
                          mem, ncpus, 
                          combination, freq, scrf, grid, charge, spin, 
                          verbose)
        writeHPCJobScript(name, moleculeDir, 
                          scheduler, cluster, 
                          ncpus, walltime, vmem, jobfs, project, software, version,
                          verbose)
    if verbose:
        print('DONE -- Generated all scripts!\n')


if __name__ == "__main__":
    # Test case
    inpDirPath = '/mnt/c/Users/ASUS/Documents/covdrugsim/src/covdrugsim/data/exampleXYZs'

    keywordLine = '# m062x/6-311+g(d,p) opt=calcfc freq scrf=(cpcm,solvent=water) int(grid=ultrafine)'

    method, basisSet = 'm062x', '6-311+g(d,p)'
    solvent, solventModel = 'water', 'cpcm'
    mem, ncpus = 4000, 8
    calcType = 'GOVF'
    charge, spin = 0, 1

    scheduler, cluster = 'pbs', 'gadi'
    walltime, vmem, jobfs, project = '24:00:00', 8000, 9000, 'p39'
    software, version = 'g16', 'c01'

    genAllScripts(inpDirPath, 
                  keywordLine,
                  method, basisSet, solvent, solventModel,
                  mem, ncpus, calcType, charge, spin,
                  scheduler, cluster,
                  walltime, vmem, jobfs, project, software, version,
                  verbose=True)

