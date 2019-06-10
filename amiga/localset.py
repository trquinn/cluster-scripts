from default_localset import *

max_traverse_depth = 1
amiga_command = "cd %s; export OMP_NUM_THREAD=1; $HOME/src/ahf-v1.0-096/bin/AHF-v1.0-097 %s"
#amiga_command = "cd %s; /u/apontzen/ahf-v1.0-084/bin/AHF-v1.0-084 %s"
#amiga_command = "cd %s; /u/mtremmel/Scripts/amiga/ahf-v1.0-091/bin/AHF-v1.0-091 %s"
#amiga_command = "cd %s; mpirun -np 8 /u/mtremmel/Scripts/amiga/ahf-v1.0-091/bin/AHF-v1.0-091 %s"
#amiga_command = "cd %s; mpiexec -np 20 /u/mtremmel/Scripts/amiga/ahf-v1.0-091/bin/AHF-v1.0-091 %s"
#amiga_command = "cd %s; mpirun /u/mtremmel/Scripts/amiga/ahf-v1.0-091/bin/AHF-v1.0-091 %s"

#amiga_command = """qsub <<EOF
#PBS -S /bin/sh
#PBS -N AHF
#PBS -l select=25:ncpus=28:mpiprocs=4:model=bro:bigmem=False
#PBS -l walltime=1:00:00
#PBS -m abe
#PBS -M m.tremmel6@gmail.com

#PBS -q normal

#. /usr/share/modules/init/sh
#module load mpi-sgi/mpt
#export OMP_NUM_THREADS=1

#cd """+os.getcwd()+"""/%s
#mpiexec /u/mtremmel/Scripts/amiga/ahf-v1.0-091/bin/AHF-v1.0-091 %s
#EOF"""

# amiga_command = """qsub <<EOF
# #PBS -S /bin/sh
# #PBS -N AHF
# #PBS -l select=1:ncpus=28:model=bro:bigmem=False
# #PBS -l walltime=1:00:00
# #PBS -m abe
# #PBS -M m.tremmel6@gmail.com
# 
# 
# cd """+os.getcwd()+"""/%s
# /u/apontzen/ahf-v1.0-084/bin/AHF-v1.0-084 %s
# EOF"""

#amiga_command = """qsub <<EOF
##PBS -S /bin/sh
##PBS -N AHF
##PBS -l mem=60GB,ncpus=16
##PBS -l walltime=1:00:00
##PBS -m abe
##PBS -M m.tremmel6@gmail.com
#
#cd """+os.getcwd()+"""/%s
#/u/apontzen/ahf-v1.0-084/bin/AHF-v1.0-084 %s
##EOF"""
