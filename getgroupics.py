# script to get the initial position and size of a group
# This needs the grp file from the group finder at z = 0, and the IC file
# from the volume run

# group = 19686 # the final gid of the group in question
# fileIC = 'runs22.bin'
# fileGRP = 'runs22.000500.fof.grp'
group = 201824 # the final gid of the group in question
fileIC = 'cosmo600.768.tbin'
fileGRP = 'cosmo600p.768.000512.fof.grp'

charm.loadSimulation(fileIC)

charm.readTipsyArray(fileGRP, 'fgid')

print charm.createGroup_AttributeRange('cluster', 'All', 'fgid', group - .5, group + .5)

range = charm.getAttributeRangeGroup('cluster', 'dark', 'position')

# center of bounding box:
print 0.5*(range[0][0] + range[1][0]), 0.5*(range[0][1] + range[1][1]), 0.5*(range[0][2] + range[1][2])

# semi-axes of bounding box:
print 0.5*(range[0][0] - range[1][0]), 0.5*(range[0][1] - range[1][1]), 0.5*(range[0][2] - range[1][2])

# radius of circumscribed sphere:
print (((range[0][0] - range[1][0])**2 + (range[0][1] - range[1][1])**2 + (range[0][2] - range[1][2])**2)**0.5)*0.5
