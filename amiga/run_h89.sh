#!/bin/bash
#SBATCH --partition=large-shared
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH -t 44:00:00
#SBATCH --mem=256G
#SBATCH --export=ALL
#SBATCH --mail-user=trq@astro.washington.edu
#SBATCH --mail-type=ALL

module load python

export LM_LICENSE_FILE=/share/apps/compute/idl/license/idl.lic:$LM_LICENSE_FILE

module load idl

python magic_amiga.py >& DIAG.amiga.26
