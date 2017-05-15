# Produce cluster mass vs. formation time plot
import pylab
import numpy
import cPickle as pickle

munit =  2.5370915e+19 # mass unit in solar masses

fmass = open('mass.pkl')
mass = numpy.array(pickle.load(fmass))
fmass.close()
ftime = open('time.pkl')
time = numpy.array(pickle.load(ftime))
ftime.close()

mass = mass*munit

pylab.semilogy(time, mass, '+')
pylab.ylabel('Mass ($M_\odot$)')
pylab.xlabel('formation 1/(1+z)')
pylab.xlim(0.0, 1.1)
pylab.ylim(1e13, 1e16)



