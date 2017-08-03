# functions to find and mark cluster in low res DM only zoom in
# version for 600 Mpc volume
kpcunit = 600000.0
msolunit = 2.7523584e+19
omega = 0.3086
medmass = omega/(288*2**5)**3

def findgal() :
    charm.createGroup_AttributeRange('highres', 'All', 'mass', -1, medmass*1.1)
    cntMass = charm.getCenterOfMass('highres')
    # get 5 Mpc sphere around cntMass
    charm.createGroupAttributeSphere('center', 'All', 'position', cntMass[0],
                                     cntMass[1], cntMass[2], 5000./kpcunit)
    cntPot = charm.findAttributeMin('center', 'potential')
    return cntPot

def mtot(group) :
    dmass = charm.getAttributeSum(group, 'dark', 'mass')
    return dmass
#    gmass = charm.getAttributeSum(group, 'gas', 'mass')
#    smass = charm.getAttributeSum(group, 'star', 'mass')
#    return dmass + gmass + smass

def density(group, r) :
    from math import pi
    v =  (4*pi/3.0)*r**3
    return mtot(group)/v

def getgaldensity(center, r) :
    global kpcunit
    charm.createGroupAttributeSphere('gal', 'All', 'position', center[0],
                                     center[1], center[2], r/kpcunit)
    return density('gal', r/kpcunit)

def getmass(group):
    return msolunit*charm.getAttributeSum(group, 'dark', 'mass')

def writemark() :
    charm.writeGroupArray('gal', 'index', 'vir3.mark')

def writemark_hres() :
    """Get just the high res particles out of the gal group and write out their indices"""
    charm.createGroup_AttributeRange('galhighres', 'gal', 'mass', -1, medmass*1.1)
    charm.writeGroupArray('gal', 'index', 'vir3hr.mark')

def readmark() :
    charm.readMark('/tmp/vir3.mark', 'mark', 'index')
    charm.createGroup_AttributeRange('marked', 'All', 'mark', 1., 100.)
