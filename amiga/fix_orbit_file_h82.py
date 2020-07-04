import Simpy
simname = "h82651gs"

# create "files.list"
Simpy.Files.getFileLists(simname, NCHILADA=False)

# create shorted orbit file
# Estimated time: 3 hours
Simpy.BlackHoles.orbit.truncOrbitFile(simname, minstep=1, maxstep=4096,
				      ret_output=False, MBHinit=1e6)
#
# The following will need all the DIAG files.
#
Simpy.BlackHoles.mergers.reducedata(simname, RetData=False, outname='DIAG/DIAG*',
                    mergename='BHmerge.txt', out_ext='.mergers',t_end=13.8)
