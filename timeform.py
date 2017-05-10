# ResolutionServer routine to find the formation epoch of all groups using a
# series of snapshots from a cosmological simulation.
# The definition of formation time is the time at which the most
# massive progenitor of the cluster reaches a specified mass fraction
# (specified by 'fracformed') of the cluster at the final time.
#
# The script depends on having a series of group catologues specified by
# a "grp" tipsy array file.  The tipsy files are expected to have names
# of the form 'simname'.stepnumber, and the grp files should have ".fof.grp"
# appended to the snapshot name.
#


from math import *
import os
import glob
import pickle
simname = 'cosmo600p.768'
fracformed = .75 # if a group is at least this fraction of the final mass, it
                 # is considered formed
formednow = []
#
# map/reduce to get the mass of all groups
#
grpmassmap = """def localparticle(p):
	return (p.gid, p.mass)
"""
grpmassreduce = """def localparticle(p):
    mass = 0.0
    for i in range(0, len(p.list)) :
        mass += p.list[i][1]
    return (p.list[0][0], mass)
"""

#
# map/reduce to find all the groups that have formed.
# If any particle is in a group whose mass is greater than fracform times the
# final group, then mark that final group as formed.
#
grpformedmap = """def localparticle(p):
    fracform = p._param[0]
    massfinal = p._param[1]
    masscurrent = p._param[2]
    formed = False
    if masscurrent[int(p.gid)] >= fracform*massfinal[int(p.fgid)] :
    	formed = True
    return (p.fgid, formed)
"""

grpformedreduce = """def localparticle(p):
    formed = False
    for i in range(0, len(p.list)) :
    	if p.list[i][1] :
    	    formed = True
            break
    return(p.list[0][0], formed)
"""

def timeform() :
    global formednow
    # get sorted array of outputs
    snaps = glob.glob(simname + '.??????')
    snaps.sort()
    snaplast = snaps[-1]
    # read in final output
    charm.loadSimulation(snaplast)
    charm.readTipsyArray(snaplast + '.fof.grp', 'gid')
    # make more efficient by only working on the particles in groups
    charm.createGroup_AttributeRange('ingroup', 'All', 'gid', .99, 1e38)
    # create array of final masses
    # mfinal is a list of tuples of (gid, mass)
    mfinal = charm.reduceParticle('ingroup', grpmassmap, grpmassreduce, None)
    # Create list of just the masses
    mfinlist = [1e38] # 0 group == particles not in a group
    mfinlist.extend([group[1] for group in mfinal])
    # initialize tform to invalid
    tform = [False]*len(mfinlist)
    # step through timesteps:
    for snap in snaps :
        print snap
        charm.loadSimulation(snap)
        charm.readTipsyArray(snaplast + '.fof.grp', 'fgid')
        charm.readTipsyArray(snap + '.fof.grp', 'gid')
        charm.createGroup_AttributeRange('ingroup', 'All', 'gid', .99, 1e38)
        # masses of all the groups
        masses = charm.reduceParticle('ingroup', grpmassmap, grpmassreduce, None)
        fsavemass = open('massdump.pkl', 'w')
        pickle.dump(tform, fsavemass)
        fsavemass.close()
        mlist = [1e38] # 0 group == particles not in a group
        mlist.extend([group[1] for group in masses])
        formednow = charm.reduceParticle('ingroup', grpformedmap, grpformedreduce, (fracformed, mfinlist, mlist))
        for grp in formednow :
            if (tform[int(grp[0])] == False) and grp[1] :
                tform[int(grp[0])] = charm.getTime()
        # Save temporary results
        fsavetime = open('timedump.pkl', 'w')
        pickle.dump(tform, fsavetime)
        fsavetime.close()
    # Save results
    fmass = open('mass.pkl', 'w')
    pickle.dump(mfinlist[1:], fmass)
    fmass.close()
    ftime = open('time.pkl', 'w')
    pickle.dump(tform[1:], ftime)
    ftime.close()
    return mfinal, mfinlist[1:], tform[1:], snaps

