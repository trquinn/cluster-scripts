#!/usr/bin/env python
# Script to set up a renormalized cluster.
#
# The assumption is that this will be drawn from a uniform volume of 600 Mpc,
# and the high res. region will be XXX 16/h Mpc in size.
# Planck cosmology will be used.

# Waves: Big cube used 768**3 waves
# Renormalized: Ultimate resolution is 768(gas)/1152(dm)^3 in 25Mpc cube.
# Mpc cube, or 1536/2304 in 50Mpc cube.  Of the 1536, the top 24**3 waves will
# overlap the 768**3.  From 24 to 768 (Nyquist) will be filled by the high res.

# Group 34462 from cosmo600
# 5e14 Msun
#
# Med res run: down to 384**3 in 25Mpc
#
import sys, os, glob, string
from math import *
# Cosmology
# Note that these parameters need to be consistent with the CMBFAST data
# file
############################################
#
pboxsize = 600.0 # In Mpc
h = 0.6777
omega = 0.3086
om_lambda = .6914
tilt = 0.9611
gamma = -1 # power spectrum gets read in from CMBFAST
sigma8 = .8288
bias = 1.0/sigma8
omegab = 0.04825
zstart = 139.0
dmgasratio = (omega - omegab)/omegab
gastemp = 1e4

#
############################################
name='h34462mr'
cpart = 'cpartt'
refine = 'refinet'
# markfile = 'vir3.mark'

def mysystem(command):
    print command
    os.system(command)

def main():

    basegrid = 288 # base particle grid (need 64 x to get romulus resolution)
    nwaves_base = 768
    basegrid3 = basegrid**3
    pmass = omega/basegrid3
    pboxsize_hinv=pboxsize*h
    pboxsize2 = 0.5*pboxsize
    basedr=pboxsize/basegrid
    epsMpc = 0.00035155674140696647*64 # .351 kpc is romulus softening
    baseeps=epsMpc/pboxsize
    # make base particle grid
    # os.system('%s %d %g %g %g %g > %s.g1.bin' % (cpart, basegrid3, pmass, -pboxsize2, pboxsize2, baseeps, name))
    #
    # parameters for refinement
    # refine 5 times for this test run
    #
    refsize2 = 36.  # Radius of inner refine in Mpc
    rmin= refsize2
    rmax= pboxsize2
    rfac= exp(log(rmax/rmin)/5.0)

    r_refine=rmax

    dr=basedr
    r_refine=r_refine/rfac
    print 'r_refine', r_refine
    # os.system('%s %g %g 2 %s.g2.bin < %s.g1.bin' % (refine, dr, r_refine, name, name))

    dr= dr*0.5
    r_refine=r_refine/rfac
    print 'r_refine', r_refine
    # os.system('%s %g %g 2 %s.g3.bin < %s.g2.bin' % (refine, dr, r_refine, name, name))

    r_refine=r_refine/rfac
    dr= dr*0.5
    print 'r_refine', r_refine
    # os.system('%s %g %g 2 %s.g4.bin < %s.g3.bin' % (refine, dr, r_refine, name, name))

    r_refine=r_refine/rfac
    dr= dr*0.5
    print 'r_refine', r_refine
    # os.system('%s %g %g 2 %s.g5.bin < %s.g4.bin' % (refine, dr, r_refine, name, name))

    r_refine=r_refine/rfac
    dr= dr*0.5
    print 'r_refine', r_refine
    # os.system('%s %g %g 2 %s.g6.bin < %s.g5.bin' % (refine, dr, r_refine, name, name))

    # Following is for high res.
    # r_refine=r_refine/rfac
    # dr= dr*0.5
    # print 'r_refine', r_refine
    # os.system('%s %g %g 2 1 %g %g %s %s.g6.bin n%s < %s.g5.bin'
    #           % ('gasrefmarks', dr, r_refine, gastemp, dmgasratio, markfile,
    #              name, markfile, name))
    # make waves
    if 0 :
        mysystem('echo %d %s 1.0 %s  1. 0.0  -7678301 %s %s %s | kgen_mt > out1' % (nwaves_base, pboxsize_hinv, h, omega,  tilt, gamma))
        mysystem('invfftr< out1 > out2')
        mysystem('fft <out2 > out3')
        kmax = nwaves_base*6.28*sqrt(3.0)/pboxsize
        mysystem('powk 1000 %g < %s.rfft > %s.pow' % (kmax, name, name))
        mysystem('rhotophik < out3 > base.phfft')
        mysystem('gradrhok x < base.phfft > gr_tmp.fft; invfftr < gr_tmp.fft > base.fx' % (name, ))
        mysystem('gradrhok y < base.phfft > gr_tmp.fft; invfftr < gr_tmp.fft > base.fy' % (name, ))
        mysystem('gradrhok z < base.phfft > gr_tmp.fft; invfftr < gr_tmp.fft > base.fz' % (name, ))

    # make high res waves
    hrboxsize = 75.
    hrboxsize_hinv = hrboxsize*h
    nwaves_hr = 2304
    # for low res only: "unpad" the fft to this number
    nwaves_keep = 1152

    # mysystem('echo %d %g 1.0 %g 1.0 0.0 -50 %g %g %g | kgen_mt > hrb.fft0'
    #              % (nwaves_hr, hrboxsize_hinv, h, omega,  tilt, gamma))
    # mysystem('export OMP_NUM_THREADS=2; invfftr < hrb.fft0 > hrb.rg')
    # mysystem('fft < hrb.rg > hrb.rfft')
    kmax = nwaves_hr*6.28*sqrt(3.0)/hrboxsize
    # mysystem('powk 1000 %g < hrb.rfft > hrb.pow' % (kmax))
    # zero out waves up to the Nyquist of the LR run
    mysystem('speczero 0 %g < hrb.rfft > hrbz.fft'
                  % ((hrboxsize_hinv/pboxsize_hinv)*nwaves_base/2))
    mysystem('powk 1000 %g < hrbz.fft > hrbz.pow' % (kmax))
    mysystem('unpad %d < hrbz.fft > hrbz_lr.fft'
                  % (nwaves_keep,))
    mysystem('rhotophik < hrbz_lr.fft > hrb_lr.phfft')
    mysystem('gradrhok x < hrb_lr.phfft | invfftr > hrb_lr.fx')
    mysystem('gradrhok y < hrb_lr.phfft | invfftr > hrb_lr.fy')
    mysystem('gradrhok z < hrb_lr.phfft | invfftr > hrb_lr.fz')

    # Center of group (in real Mpc)
    mx = -252.734375
    my = -78.90625
    mz = 71.484375

    mysystem('pmovefrgbg2t %s.g6.bin base.fx base.fy base.fz hrb_lr.fx hrb_lr.fy hrb_lr.fz %g %g %g %g %g %g %g %g > %s.sbin'
              % (name, zstart, bias, omega, om_lambda, 0.0, mx, my, mz, name))
    # Unit conversion from Mpc, 10^15 M_sun, Gyr to natural units
    tscale=1.0/sqrt(4.498*h*h*.0002776)
    mysystem('scalet %g %g < %s.sbin > %s.tbin' % (pboxsize, tscale, name, name))
        
if __name__ == '__main__':
	main()
