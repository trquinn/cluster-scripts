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

# Group 201824 from cosmo600
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
name='h201824mr'
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
    refsize2 = 40.  # Radius of inner refine in Mpc
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
        mysystem('rhotophik < out3 > %s.phfft' % (name, ))
        mysystem('gradrhok x < %s.phfft > gr_tmp.fft; invfftr < gr_tmp.fft > %s.fx' % (name, name))
        mysystem('gradrhok y < %s.phfft > gr_tmp.fft; invfftr < gr_tmp.fft > %s.fy' % (name, name))
        mysystem('gradrhok z < %s.phfft > gr_tmp.fft; invfftr < gr_tmp.fft > %s.fz' % (name, name))

    # make high res waves
    hrboxsize = 50.
    hrboxsize_hinv = hrboxsize*h
    nwaves_hr = 1536
    # for low res only: "unpad" the fft to this number
    nwaves_keep = 768

    # mysystem('echo %d %g 1.0 %g 1.0 0.0 -50 %g %g %g | kgen_mt > hr.fft0'
    #             % (nwaves_hr, hrboxsize_hinv, h, omega,  tilt, gamma))
    # mysystem('export OMP_NUM_THREADS=4; invfftr < hr.fft0 > hr.rg')
    # mysystem('fft < hr.rg > hr.rfft')
    kmax = nwaves_hr*6.28*sqrt(3.0)/hrboxsize
    # mysystem('powk 1000 %g < hr.rfft > hr.pow' % (kmax))
    # zero out waves up to the Nyquist of the LR run
    # mysystem('speczero 0 %g < hr.rfft > hrz.fft'
    #              % ((hrboxsize_hinv/pboxsize_hinv)*nwaves_base/2))
    # mysystem('powk 1000 %g < hrz.fft > hrz.pow' % (kmax))
    # mysystem('unpad %d < hrz.fft > hrz_lr.fft'
    #              % (nwaves_keep,))
    # mysystem('rhotophik < hrz_lr.fft > hr_lr.phfft')
    # mysystem('gradrhok x < hr_lr.phfft | invfftr > hr_lr.fx')
    # mysystem('gradrhok y < hr_lr.phfft | invfftr > hr_lr.fy')
    # mysystem('gradrhok z < hr_lr.phfft | invfftr > hr_lr.fz')

    # Center of group (in real Mpc)
    mx = 83.203125
    my = 239.84375
    mz = 197.65625

    # mysystem('pmovefrgbg2t %s.g6.bin %s.fx %s.fy %s.fz hr_lr.fx hr_lr.fy hr_lr.fz %g %g %g %g %g %g %g %g > %s.sbin'
    #          % (name, name, name, name, zstart, bias, omega,
    #             om_lambda, 0.0, mx, my, mz, name))
    # Unit conversion from Mpc, 10^15 M_sun, Gyr to natural units
    tscale=1.0/sqrt(4.498*h*h*.0002776)
    mysystem('scalet %g %g < %s.sbin > %s.tbin' % (pboxsize, tscale, name, name))
        
if __name__ == '__main__':
	main()
