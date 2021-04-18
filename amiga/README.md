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

## testing tangos

Set up environment variables and python (see tangos_env.sh)
Start tangos with: "tangos serve"

In python:
>>> import tangos
>>> tangos.all_simulations() # gets list of simulations
>>> tangos.get_simulation("h82651gs").timesteps # list of timesteps
>>> halo = tangos.get_halo("h82651gs/%4096/halo_1") # get halo 1 from last timestep

"halo.keys()" reports a bunch of BH_central; how do I pick the right one?

6/11/20: I can't get past "ValueError: Halo 220 does not exist" with timestep 131.
Let me start again from the beginning.

6/13/20: The ValueError above persists after rerunning everything in tangos_env.sh.

6/14/20: The issue is that pynbody is trying to read the \*.amiga.grp files,
and these files have different halo numberings than the \*AHF\* files.
Start all over again after moving the \*.amiga.\* files to a subdirectory.
