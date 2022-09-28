#!/bin/bash
# Script to add a simulation to the tangos database.  The simulation
# directory is the first argument to this script

# The following was for comet
# module load gnu
# module load openmpi_ib
# module load python
#
# for expanse:
module load gcc
module load openmpi
module load python
module load py-mpi4py
module load sdsc

export TANGOS_SIMULATION_FOLDER=$HOME/scratch/
export TANGOS_DB_CONNECTION=$HOME/scratch/tangos/sqlite.db

# tangos add $1
# This command takes over 12 hours
# Without .amiga.grp, this only takes 2.5 hours
# N.B.: the handler argument requires the "issue-117" branch of tangos to be installed.
# This needs 32GB
# tangos add h102054gs --handler=pynbody.ChangaIgnoreIDLInputHandler
# tangos add h102054gs
#  The following takes 15 minutes
# tangos import-properties Mvir Rvir --for h102054gs
# tangos link --for h102054gs
#  MPI version of link.  NB: the MPI implementation uses a master-slave setup;
# there are nrank-1 worker threads.
# ibrun tangos link --for h102054gs --backend mpi4py
# The following could only have 3 worker threads because of memory issues.
# tangos write contamination_fraction --for h102054gs
# ibrun tangos write contamination_fraction --for h102054gs --backend mpi4py
# ibrun tangos write shrink_center max_radius SFR_histogram --backwards --with-prerequisites --include-only="NDM()>1000" --for h102054gs --backend mpi4py
# tangos write shrink_center max_radius SFR_histogram --with-prerequisites --include-only="NDM()>1000" --for h102054gs
# tangos_add_bh --sims h102054gs
# ibrun tangos_add_bh --sims h102054gs --backend mpi4py
# 
# Note: the following did not write the BH_mass, presumably because of missing
# prequisites.
tangos write BH_mass BH_mdot_histogram --for h102054gs --type bh
# ibrun tangos write BH_mass BH_mdot_histogram --for h102054gs --type bh --backend mpi4py
#
# Let's add more halo information:
# tangos write dm_density_profile gas_density_profile uvi_image SFR_histogram --with-prerequisites --include-only="NDM()>1000" --for h102054gs
# The uvi_image seems to take a lot of time, let's skip it for now.
# tangos write dm_density_profile gas_density_profile SFR_histogram --with-prerequisites --include-only="NDM()>1000" --for h102054gs
# ibrun tangos write contamination_fraction --for h102054gs --backend mpi4py
# ibrun tangos write shrink_center max_radius SFR_histogram --with-prerequisites --include-only="NDM()>1000" --for h102054gs --backend mpi4py
