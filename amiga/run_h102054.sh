#!/bin/bash
#SBATCH --partition=shared
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=5
#SBATCH -t 24:00:00
#SBATCH --mem=64G
#SBATCH --export=ALL
#SBATCH --mail-user=trq@astro.washington.edu
#SBATCH --mail-type=ALL

module load python

export LM_LICENSE_FILE=/share/apps/compute/idl/license/idl.lic:$LM_LICENSE_FILE

module load idl

python magic_amiga_new.py >& DIAG.amiga.12
