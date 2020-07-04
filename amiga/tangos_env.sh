#!/bin/bash
# Script to add a simulation to the tangos database.  The simulation
# directory is the first argument to this script

module load python

export TANGOS_SIMULATION_FOLDER=$HOME/scratch/
export TANGOS_DB_CONNECTION=$HOME/scratch/tangos/sqlite.db

# tangos add $1
# This command takes over 12 hours
# tangos add h82651gs
#
#  MPI version of link.  NB: the MPI implementation uses a master-slave setup;
# there are nrank-1 worker threads.
# ibrun tangos link --for h82651gs --backend mpi4py
# tangos import-properties Mvir Rvir --for h82651gs
# tangos_add_bh --sims h82651gs
# ibrun tangos_add_bh --sims h82651gs --backend mpi4py
ibrun tangos write BH_mass BH_mdot_histogram --for h82651gs --type bh --backend mpi4py
