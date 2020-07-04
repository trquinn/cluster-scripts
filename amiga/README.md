Scripts in this directory are to
1) create group catalogs for a simulation (see run_h89.sh, for example).
2) load these catalogs into a TANGOS database.

Needed software:
"magic_amiga.py" (included here)


tangos

Michael's simulation scripts: https://github.com/mtremmel/Simpy

Directions for shortened orbit file from Michael:

First, is to generate a shortened.orbit file. This takes the .orbit file
and makes it more manageable to work with.

Simpy.BlackHoles.orbit.truncOrbitFile(simname, minstep=1, maxstep=4096,
				      ret_output=False, MBHinit=1e6)

where simname is the name of the simulation (where a step is simname.stepnumber) and maxstep is the total number of steps (likely 4096 or 8192).

This should work ok, but let me know if it doesn't. The result should be the creation of a shortened.orbit file

Then to make the mergers, you need to have the original output files from the simulation. The diagnostic files. This is super important because these files have output that says when two SMBHs merge.

Simpy.BlackHoles.mergers.reducedata(simname, RetData=False, outname='*out*', mergename='BHmerge.txt', out_ext='.mergers',t_end=13.8)

So what this does is reads through all the diagnostic files, which it finds based on outname (like *out* or *diag* or however you've named them). Then it stores the merger information in a file named BHmerge.txt. It then
reads this file and creates a new file called simname.mergers. This looks for every merger happening up until t_end. Reading in the diagnostics will take longer because they can be large (another problem with the way things work)
