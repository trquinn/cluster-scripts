# functions to find and mark cluster in low res DM only zoom in
# version for 600 Mpc volume
kpcunit = 600000.0
msolunit = 2.7523584e+19
omega = 0.3086
medmass = omega/(288*2**5)**3

def findgal() :
    charm.createGroup_AttributeRange('highres', 'All', 'mass', -1, medmass*1.1)
    cntPot = charm.findAttributeMin('highres', 'potential')
    return cntPot

def mtot(group) :
    dmass = charm.getAttributeSum(group, 'dark', 'mass')
    gmass = charm.getAttributeSum(group, 'gas', 'mass')
    smass = charm.getAttributeSum(group, 'star', 'mass')
    return dmass + gmass + smass

def density(group, r) :
    from math import pi
    v =  (4*pi/3.0)*r**3
    return mtot(group)/v

def getgaldensity(center, r) :
    global kpcunit
    charm.createGroupAttributeSphere('gal', 'All', 'position', center[0],
                                     center[1], center[2], r/kpcunit)
    return density('gal', r/kpcunit)

def writemark() :
    charm.writeGroupArray('gal', 'index', '/tmp/vir3.mark')

def readmark() :
    charm.readMark('/tmp/vir3.mark', 'mark', 'index')
    charm.createGroup_AttributeRange('marked', 'All', 'mark', 1., 100.)
