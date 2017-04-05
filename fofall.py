#!/usr/bin/env python
# Script to create FOF based mass function from cosmo600p.768 simulation.
# 
# I assume a 768^3 grid of particles and use the standard linking length value
# of .2 times the interparticle separation.
#
import os
import glob
simname = 'cosmo600p.768'
partgrid = 768.0
b = .2/partgrid  # linking length

def mysystem(command):
    print command
    os.system(command)

def main():
    for snap in glob.glob(simname + '.000[0-5]??') :
    	mysystem('aprun -n 1 -d 16 ./fof -e %g -m 32 -d -v -o %s.fof -p 1 -std < %s > DIAG.fof' % (b, snap, snap))
    # The following just produces the "stat" file.
#    mysystem('skid -tau %g -std -nu -unbind %s.fof -stats -p 1 -o %s.sfof < %s.00500 > DIAG.skid' % (b, simname, simname, simname))

if __name__ == '__main__':
 	main()
