import os
from os.path import isdir

from covdrugsim.qmcalc.runGaussian.settings import keywordDict


def genFromDir(inputDir, WALLTIME, VMEM, MEM, JOBFS, CHARGE, SPIN, METHOD, BASIS_SET, SOLVENT, SOLVENT_MODEL, CLUSTER, CALC_TYPE, NCPUS, SOFTWARE, VERSION):
    """Generate Gaussian input job files and submission files for molecules in given directories"""
    assert CALC_TYPE in keywordDict.keys(), 'Calculation type not known!'
    conformers = [g for g in os.listdir(inputDir) if isdir('{0}/{1}'.format(inputDir, g))]
    for j, title in enumerate(conformers):
        conformer_dir = '{0}/{1}'.format(inputDir, title)
        combination = '{0}/{1}'.format(METHOD, BASIS_SET)
        SCRF = ' scrf=({0},solvent={1})'.format(SOLVENT, SOLVENT_MODEL)
        gaussInpGeomOpt(title, conformer_dir, MEM, NCPUS, combination, keywordDict[CALC_TYPE]['freq'],
                           SCRF, keywordDict[CALC_TYPE]['type'], CHARGE, SPIN)
        writeJobScript(title, conformer_dir, CLUSTER, NCPUS, SOFTWARE, WALLTIME, VMEM, JOBFS, VERSION)


def gaussInpGeomOpt(title, dirc, mem, ncpus, combination, freq, scrf, calc_type, charge, spin):
    with open('{0}/{1}.inp'.format(dirc, title), 'w') as f:
        f.write('%mem={0}mb\n%nproc={1}\n%chk={2}.chk\n'.format(mem, ncpus, title))
        f.write('# {0}{1}{2}{3}'.format(combination, scrf, calc_type, freq))
        f.write('\n\n{0}\n\n{1} {2}\n'.format(title, charge, spin))
        with open('{0}/{1}.xyz'.format(dirc, title), 'r') as g:
            lineList = g.readlines()
            hasEnergyName = 'Energy' in lineList[1] or 'TI' in lineList[1] or 'Name' in lineList[1]  # Potential bug-breeding spots
            hasPath = ':' in lineList[1]
            has_blank = '\n' in lineList[1]
            for i, line in enumerate(lineList):
                if hasEnergyName and i > 1:
                    f.write('{0}'.format(line))
                elif hasPath and i > 1:
                    f.write('\n{0}'.format(line)) if i == 2 else f.write('{0}'.format(line))
                elif has_blank and i > 1:
                    f.write('{0}'.format(line))
                elif not(hasEnergyName) and not(hasPath) and not(has_blank) and i > 0:
                    f.write('{0}'.format(line))
                else:
                    pass
            f.write('\n')  # Necessary


def writeJobScript(title, dirc, cluster, ncpus, software, walltime, vmem, jobfs, version):
    with open('{0}/{1}.sh'.format(dirc, title), 'w') as f:
        if cluster == 'Raijin':
            f.write('#!/bin/bash\n#PBS -l wd\n#PBS -q normal\n')
            f.write('#PBS -l walltime={0},mem={1}mb,ncpus={2},software={3},jobfs={4}mb'.format(walltime, vmem, ncpus, software, jobfs))
            f.write('\n\nmodule load gaussian/{0}{1}'.format(software, version))
            f.write('\n{0} < {1}.inp > {1}.out 2>&1'.format(software, title))
        elif cluster == 'RCC':
            f.write('#!/bin/bash\n#PBS -S /bin/bash\n#PBS -l walltime={0}\n#PBS -A UQ-SCI-SCMB\n'.format(walltime))
            f.write('#PBS -l select=1:ncpus={0}:mem={1}MB'.format(ncpus, vmem))
            f.write('\n\ncd $PBS_O_WORKDIR')
            f.write('\n\nmodule load gaussian/{0}-{1}-bash'.format(software, version.upper()))
            f.write('\n{0} < {1}.inp > {1}.out'.format(software, title))
        else:
            raise Exception('Cluster not recognized!')


if __name__ == "__main__":

    jobList = ['geom_opt', 'spe', 'SCS']

    # Default values, unlikely changing
    NCPUS, SOFTWARE, VERSION = int(8), 'g16', 'b01'

    # Change these!
    job = jobList[0]
    inputDir = "/User/kahochow/Desktop/Li_mechanism/Li_work/Reactant"  # One level above your directories
    WALLTIME, VMEM, MEM, JOBFS = '12:00:00', int(8000), int(8000), int(2400)
    METHOD, BASIS_SET = 'B3LYP', '6-31+G(d)'
    CHARGE, SPIN = int(0), int(1)  # Careful for CHARGE if it's transition state!
    SOLVENT, SOLVENT_MODEL = "water", "smd"
    CLUSTER = "Raijin"
    CALC_TYPE = 'GOVF'
    # "GOVF" if normal geometry optimisation,
    # "TSGOVF" if transition state geometry optimisation,
    # "SPEiS" if single point energy calculation

    genFromDir(inputDir, WALLTIME, VMEM, MEM, JOBFS, CHARGE, SPIN, METHOD, BASIS_SET, SOLVENT, SOLVENT_MODEL, CLUSTER, CALC_TYPE, NCPUS, SOFTWARE, VERSION)
