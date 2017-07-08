#!/bin/csh -x
# This makes the   ICs for a 600Mpc uniform box in PLANCK cosmology.
# This simulation has the equivalent resolution as 50Mpc with 64^3 particles.
# Or 25 Mpc with 32^3 particles.
# Softening will therefore be 350pc*24 ~ 8.4kpc
# 
#  softening scaling = 2.5 Kpc for a 100Mpc 432^3 Box. Softening propto 2.5 (432/FFT) (Boxsize/100)  
#e.g for a 25Mpc box with a  64^3 FFT eps=4.25Kpc
#
#CMBFAST version  with gas
########################################
# Run details:
#   boxsize:   600   Mpc
#   h:         0.6777
#   Omega_m:   0.26035+0.04825 = 0.3086
#   Omega_L:   0.6914
#   Sigma_8:   0.8288
#   DREED Power Spectrum
#   n=0.9611
#   omegab=0.04825
########################################
# set work directories
set bindir = $HOME/bin
set datadir =  .
########################################
#
# COSMOLOGICAL SETTINGS HERE
#
################################
set pboxsize=600.0
set omega=0.3086
set lambda=0.6914
set h=0.6777
set tilt=0.9611
# gamma=-1 to read in CMBFAST.tf (has to be in datadir) gamma=0 to use BBKS
set gamma=-1.
# b = sigma8^-1 = 0.77^-1
set b=1.2065
# set w to 0 for lambda runs.
set w=0.
# omega baryon
set omegab=0.04825
set dmgasratio=`echo $omegab $omega | awk '{ print ($2-$1)/$1 ; }'`
echo dmgasratio=$dmgasratio
# Initial Temperature
set temp=500
set pboxsize_hinv=`echo $pboxsize $h | awk '{ print $1 * $2 ; }'`
########################################################################## 
 

#####################################################PARTICLE FILE FOR INITIAL UNIFORM RUN 
set gridsize=768
set nwave_keep=192
set darkgridsize=768
set partgrid3=`echo $darkgridsize | awk '{print $1 * $1 * $1;}'`
set pmass=`echo $omega $partgrid3 | awk '{printf("%.16g", $1/$2);}'`
set pboxsize2=`echo $pboxsize | awk '{ printf("%.16g", $1/2.0) ; }'`
# base softening in Mpc h-1 (8.4 kpc)
set baseeps_hinv = 0.005718
# 25Mpc at 384^3 gives 0.703kpc
# base softening in sims units
set baseeps=`echo $baseeps_hinv $pboxsize_hinv | awk '{ printf("%.16g", $1/$2) ; }'`
echo baseeps=$baseeps

$bindir/cpartt $partgrid3 $pmass -$pboxsize2 $pboxsize2 $baseeps > cosmo600PLK.768.bin

#
######################################################INITIAL LORES FFT+displacements
#set bias to 1 in kgen
echo $gridsize $pboxsize_hinv 1.0 $h  1. 0.0  -7678301 $omega $tilt $gamma |$bindir/kgen_mt > out1
$bindir/invfftr< out1 > out2
$bindir/fft <out2 > out3
##correct sampling has to be 4*gridsize. Turn this on for zoomed in runs. Modify filename in rhotopik
$bindir/unpad $nwave_keep <out3>out3b
$bindir/powk 200 5 <out3>cosmo6.50PLK.pow
$bindir/rhotophik < out3b > out4.phfft
$bindir/gradrhok x < out4.phfft | $bindir/invfftr > cosmo600PLK.fx
$bindir/gradrhok y < out4.phfft | $bindir/invfftr > cosmo600PLK.fy
$bindir/gradrhok z < out4.phfft | $bindir/invfftr > cosmo600PLK.fz

# generate UNIFORM ICS


# Move particles and use the force(s). 59 here is the starting z
$bindir/pmovefrgt cosmo600PLK.768.bin cosmo600PLK.fx cosmo600PLK.fy cosmo600PLK.fz 139 $b $omega $lambda $w 0. 0. 0. > cosmo600.768.sbin
set tscale=`echo $h | awk '{printf("%.16g", 1/sqrt(4.498*$1*$1*2.776e-4)) ; }'`
$bindir/scalet $pboxsize $tscale < $datadir/cosmo600.768.sbin > $datadir/cosmo600.768.tbin

