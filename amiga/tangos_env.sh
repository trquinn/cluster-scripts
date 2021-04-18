#!/bin/bash
# Script to add a simulation to the tangos database.  The simulation
# directory is the first argument to this script

module load gnu
module load openmpi_ib
module load python

export TANGOS_SIMULATION_FOLDER=$HOME/scratch/
export TANGOS_DB_CONNECTION=$HOME/scratch/tangos/sqlite-test.db

# tangos add $1
# This command takes over 12 hours
# Without .amiga.grp, this only takes 2.5 hours
tangos add h82651gs --handler=pynbody.ChangaUseIDLInputHandler
#  The following takes 15 minutes
# tangos import-properties Mvir Rvir --for h82651gs
#  MPI version of link.  NB: the MPI implementation uses a master-slave setup;
# there are nrank-1 worker threads.
# ibrun tangos link --for h82651gs --backend mpi4py
# The following could only have 3 worker threads because of memory issues.
# ibrun tangos write contamination_fraction --for h82651gs --backend mpi4py
# ibrun tangos write shrink_center max_radius SFR_histogram --backwards --with-prerequisites --include-only="NDM()>1000" --for h82651gs --backend mpi4py
# tangos_add_bh --sims h82651gs
# ibrun tangos_add_bh --sims h82651gs --backend mpi4py
# 
# Note: the following did not write the BH_mass, presumably because of missing
# prequisites.
# tangos write BH_mass BH_mdot_histogram --for h82651gs --type bh
# ibrun tangos write BH_mass BH_mdot_histogram --for h82651gs --type bh --backend mpi4py
#
# Let's add more halo information:
# tangos write dm_density_profile gas_density_profile uvi_image SFR_histogram --with-prerequisites --include-only="NDM()>1000" --for h82651gs
# The uvi_image seems to take a lot of time, let's skip it for now.
# tangos write dm_density_profile gas_density_profile SFR_histogram --with-prerequisites --include-only="NDM()>1000" --for h82651gs
# ibrun tangos write contamination_fraction --for h82651gs --backend mpi4py
# ibrun tangos write shrink_center max_radius SFR_histogram --with-prerequisites --include-only="NDM()>1000" --for h82651gs --backend mpi4py
