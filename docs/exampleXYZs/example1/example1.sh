#!/bin/bash
#PBS -l wd
#PBS -q normal
#PBS -l walltime=24:00:00,mem=8000mb,ncpus=8,software=g16,jobfs=9000mb,storage=scratch/p39

module load gaussian/g16c01
g16 < example1.inp > example1.out 2>&1