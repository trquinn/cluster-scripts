import pynbody
import glob

basename = 'cosmo25p.768sg1bwK1BHe75'
snapfiles = glob.glob(basename + ".00????")

for file in snapfiles: 
    print("Processing " + file + "\n")
    s = pynbody.load(file)
    h = s.halos()
    statoutfile = s.filename + ".amiga.stat"
    tipsyoutfile = s.filename + ".amiga.gtp"
    print("Writing stats\n")
    h.writestat(s, h, statoutfile)
# h.writetipsy(s, h, tipsyoutfile)
# The following requires trq's modifications to pynbody ahf.py
# write out the grp file in NChilada format.
    print("Writing grp\n")
    h.writegrp_nc()
