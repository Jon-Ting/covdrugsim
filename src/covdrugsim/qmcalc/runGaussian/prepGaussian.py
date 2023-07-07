import os
from os.path import isdir

from covdrugsim.qmcalc.runGaussian.settings import keywordDict


def genFromDir(inputDir, 
               method='B3LYP', basisSet='6-31+G(d)', solvent='water', solventModel='smd',
               mem=8000, ncpus=8, calcType='GOVF', charge=0, spin=1, 
               scheduler='pbs', cluster='gadi', 
               walltime='10:00:00', vmem=8000, jobfs=2400, software='g16', version='c01'):
    """
    Generate Gaussian input job files and submission files for molecules under all directories under a specified directory ('inputDir').

    Parameters
    ----------
    inputDir : str
        Directory path to the input directories.
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
        Software to use for the job.
    version : str
        Version of the software.
    """
    assert calcType in keywordDict.keys(), 'Calculation type not known!'
    conformers = [g for g in os.listdir(inputDir) if isdir(f"{inputDir}/{g}"))]
    for name in conformers:
        conformerDir = f"{inputDir}/{name}"
        combination = f"{method}/{basisSet}"
        scrf = f" scrf=({solvent},solvent={solventModel})"
        gaussInpGeomOpt(name, conformerDir, 
                        mem, ncpus, combination, keywordDict[calcType]['freq'], 
                        scrf, keywordDict[calcType]['type'], charge, spin)
        writeJobScript(name, conformerDir, 
                       scheduler, cluster, 
                       ncpus, walltime, vmem, jobfs, software, version)


def gaussInpGeomOpt(name, dirPath, 
                    mem=8000, ncpus=8, 
                    combination='B3LYP/6-31+G(d)', scrf=' scrf=(water,solvent=smd)', freq=' freq=noraman', 
                    calcType='GOVF', charge=0, spin=1):
    """
    Generate a Gaussian input file based on specified inputs.

    Parameters
    ----------
    name : str
        Name of the jobscript, also used for input and output file of the software to run.
    dirPath : str
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
    calcType : str
        Type of calculation (e.g. 'GOVF' for normal geometry optimisation; 'TSGOVF' for transition state geometry optimisation, 
        'SPEiS' for single point energy calculation, refer to 'keywordDict' for other options).
    charge : int
        Charge of the molecule (pay special attention if you have a transition state).
    spin : int
        Spin of the molecule.
    """
    with open(f"{dirPath}/{name}.inp", 'w') as inpFile:
        inpFile.write(f"%mem={mem}mb\n%nproc={ncpus}\n%chk={name}.chk\n"
        inpFile.write(f"# {combination}{scrf}{calcType}{freq}"
        inpFile.write(f"\n\n{name}\n\n{charge} {spin}\n"
        with open(f"{dirPath}/{name}.xyz", 'r') as xyzFile:
            lineList = xyzFile.readlines()
            hasEnergyName = 'Energy' in lineList[1] or 'TI' in lineList[1] or 'Name' in lineList[1]  # Potential bugs
            hasPath = ':' in lineList[1]
            hasBlank = '\n' in lineList[1]
            for (i, line) in enumerate(lineList):
                if hasEnergyName and (i > 1):
                    inpFile.write(line)
                elif hasPath and (i > 1):
                    inpFile.write(f"\n{line}" if i == 2 else inpFile.write(line)
                elif hasBlank and (i > 1):
                    inpFile.write(line)
                elif not(hasEnergyName) and not(hasPath) and not(has_blank) and (i > 0):
                    inpFile.write(line)
            inpFile.write('\n')


def writeJobScript(name, dirPath='.', 
                   scheduler='pbs', cluster='gadi', 
                   ncpus=8, walltime='10:00:00', vmem=8000, jobfs=2400, software='g16', version='c01'):
    """
    Generate a HPC jobscript based on specified inputs. 

    Parameters
    ----------
    name : str
        Name of the jobscript, also used for input and output file of the software to run.
    dirPath : str
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
    software : str
        Software to use for the job.
    version : str
        Version of the software.
    
    Notes
    -----
    - If your HPC system does not use PBS jobscript modifications will be needed for the function.
    - Feel free to change the default values according to your most commonly used settings.
    """
    with open(f"{dirPath}/{name}.sh", 'w') as f:
        if scheduler == 'pbs':
            if cluster == 'gadi':
                f.write('#!/bin/bash\n#PBS -l wd\n#PBS -q normal\n')
                f.write(f"#PBS -l walltime={walltime},mem={vmem}mb,ncpus={ncpus},software={software},jobfs={jobfs}mb")
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


if __name__ == "__main__":

    jobList = ['geom_opt', 'spe', 'SCS']

    # Default values, unlikely changing
    NCPUS, SOFTWARE, VERSION = int(8), 'g16', 'c01'

    # Change these!
    job = jobList[0]
    inputDir = "/User/kahochow/Desktop/Li_mechanism/Li_work/Reactant"  # One level above your directories
    WALLTIME, VMEM, MEM, JOBFS = '12:00:00', int(8000), int(8000), int(2400)
    METHOD, BASIS_SET = 'B3LYP', '6-31+G(d)'
    CHARGE, SPIN = int(0), int(1)  # Careful for CHARGE if it's transition state!
    SOLVENT, SOLVENT_MODEL = "water", "smd"
    CLUSTER = "Raijin"
    CALC_TYPE = 'GOVF'

    genFromDir(inputDir, WALLTIME, VMEM, MEM, JOBFS, CHARGE, SPIN, METHOD, BASIS_SET, SOLVENT, SOLVENT_MODEL, CLUSTER, CALC_TYPE, NCPUS, SOFTWARE, VERSION)
