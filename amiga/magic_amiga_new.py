#!/usr/bin/env python
"""
magic_amiga.py by Andrew Pontzen

This script is supposed to make it much easier to AMIGA all your gasoline output.
Before starting, you probably need to change some of the lines in localset.py
which contains the command line instructions to AMIGA etc."""

# Initial things:

import os
import localset_michael
import re

from localset_michael import ignore_error, ignore_idl_error, file_ignore_pattern, idl_preamble, idl_proc_name, idl_pass_z, idl_command, amiga_command, amiga_params, max_traverse_depth, only_idl, newstyle_amiga


##### YOU SHOULDN'T NEED TO CHANGE ANYTHING AFTER THIS LINE ######

identifier = "magic_amiga.py v0.0"

_mpi_initialized = False  # used in embarrassing parallelization tasks

import glob
import os
import math
import sys
import time
import fnmatch

import builtins as bi

if "all" not in bi.__dict__:
    # py2.4 backporting for UW
    def all(x):
        for xi in x:
            if not xi:
                return False

        return True

    def any(x):
        for xi in x:
            if xi:
                return True

        return False


def can_load(f):
    import pynbody
    try:
        pynbody.load(f)
        return True
    except:
        return False


def find(extension=None, mtd=None, ignore=None, basename=""):
    if mtd == None:
        mtd = max_traverse_depth
    if ignore == None:
        ignore = file_ignore_pattern
    out = []

    if extension is not None:
        for d in range(mtd + 1):
            out += glob.glob(basename + ("*/" * d) + "*." + extension)

        out = [f[:-(len(extension) + 1)] for f in out]

        out = [f for f in out if not any([fnmatch.fnmatch(f, ipat) for ipat in ignore])]
    else:
        for d in range(mtd + 1):
            out += list(filter(can_load,
                          glob.glob(basename + ("*/" * d) + "*.00???")))
            out += list(filter(can_load,
                          glob.glob(basename + ("*/" * d) + "*.00????")))

    return set(out)


def get_param_file(output_file):
    """Work out the param file corresponding to the
    specified output"""

    q = "/".join(output_file.split("/")[:-1])
    if len(q) != 0:
        path = "/".join(output_file.split("/")[:-1]) + "/"
    else:
        path = ""

    candidates = glob.glob(path + "*.param")

    if len(candidates) == 0:
        candidates = glob.glob(path + "../*.param")

    if len(candidates) == 0:
        raise RuntimeError("No .param file in " + path + \
            " (or parent) -- please supply or create tipsy.info manually")

    candidates = [x for x in candidates if "direct" not in x and "mpeg_encode" not in x]

    if len(candidates) > 1:
        raise RuntimeError("Can't resolve ambiguity -- too many param files matching " + \
            path)

    return candidates[0]


def param_file_to_dict(param_file):
    f = open(param_file, 'r')
    out = {}

    for line in f:
        try:
            s = line.split()
            if s[1] == "=" and "#" not in s[0]:
                key = s[0]
                v = s[2]

                if key[0] == "d":
                    v = float(v)
                elif key[0] == "i" or key[0] == "n" or key[0] == "b":
                    v = int(v)

                out[key] = v
        except (IndexError, ValueError):
            pass
    f.close()
    return out


def info_from_params(param_file, tipsy_info_file, return_hubble=False):
    f = open(param_file, 'r')

    munit = dunit = hub = None
    for line in f:
        try:
            s = line.split()
            if s[0] == "dMsolUnit":
                munit = float(s[2])
            elif s[0] == "dKpcUnit":
                dunit = float(s[2])
            elif s[0] == "dHubble0":
                hub = float(s[2])
            elif s[0] == "dOmega0":
                om_m0 = s[2]
            elif s[0] == "dLambda":
                om_lam0 = s[2]

        except IndexError as ValueError:
            pass
    f.close()

    if munit == None or dunit == None or hub == None:
        raise RuntimeError("Can't find all parameters required in .param file")

    denunit = munit / dunit ** 3
    # see original param2units.py for explanation of this factor
    velunit = 8.0285 * math.sqrt(6.67300e-8 * denunit) * dunit

    hub *= 10. * velunit / dunit
    
    if return_hubble:
        return hub

    if tipsy_info_file is not None:
        tu = open(tipsy_info_file, "w")
        print(om_m0, file=tu)
        print(om_lam0, file=tu)
        print(1.e-3 * dunit * hub, file=tu)

        print(velunit, file=tu)
        print(munit * hub, file=tu)
        print(" ", file=tu)
        print("# Auto-created from " + param_file + " by " + identifier, file=tu)
        tu.close()
    else:
        return [1.e-3 * dunit * hub, munit * hub, velunit, 0.025, om_m0, om_lam0]


def ahf_dejunk(t):
    """Remove the redshift etc junk information on AHF file outputs
    to get a clear comparative"""
    if type(t) == list or type(t) == set:
        return set([ahf_dejunk(x) for x in t])

    cleaned = ".z".join(t.split(".z")[:-1])
    if cleaned[-5:] == ".0000":
        cleaned = cleaned[:-5]

    if cleaned == "":
        cleaned = "z".join(t.split("z")[:-1])

    return cleaned


def ahf_getjunk(t):
    """Get the junky z* spec from an AHF filename for Alyson's script"""

    if "0000.z" in t:
        plop = t.split(".z")[-1]
        return "z" + (".".join(plop.split(".")[:2]))
    else:
        plop = t.split(".z")[-1]
        return "z" + (".").join(plop.split(".")[:2])
        #raise RuntimeError, "Old style AMIGA output, by the looks of things -- sorry, not set up to handle that"


def _mpi_assign_thread(job_iterator):
    # Sit idle until request for a job comes in, then assign first
    # available job and move on. Jobs are labelled through the
    # provided iterator
    import pypar
    import pypar.mpiext

    j = -1

    print("Manager --> Entered iterator code")

    alive = [True for i in range(pypar.size())]

    while any(alive[1:]):
        dest = pypar.receive(source=pypar.mpiext.MPI_ANY_SOURCE, tag=1)
        try:
            time.sleep(0.05)
            j = job_iterator.next()[0]
            print("Manager --> Sending job", j, "to rank", dest)
        except StopIteration:
            alive[dest] = False
            print("Manager --> Sending out of job message to ", dest)
            j = None

        pypar.send(j, destination=dest, tag=2)

    print("Manager --> All jobs done and all processors>0 notified; exiting thread")


def mpi_sync_db(session):
    """Causes the halo_db module to use the rank 0 processor's 'Creator' object"""

    global _mpi_initialized

    if _mpi_initialized:
        import pypar
        import halo_db as db

        if pypar.rank() == 0:
            x = session.merge(db._current_creator)
            session.commit()
            time.sleep(0.5)
            print("Manager --> transmit run ID=", x.id)
            for i in range(1, pypar.size()):
                pypar.send(x.id, tag=3, destination=i)

            db._current_creator = x

        else:
            ID = pypar.receive(source=0, tag=3)
            print("Rank", pypar.rank(), " --> set run ID=", ID)
            db._current_creator = session.query(
                db.Creator).filter_by(id=ID).first()
            print(db._current_creator)

    else:
        print("NOT syncing DB references: MPI unavailable")


def _mpi_iterate(task_list):
    """Sets up an iterator returning items of task_list. If this is rank 0 processor, runs
    a separate thread which dishes out tasks to other ranks. If this is >0 processor, relies
    on getting tasks assigned by the rank 0 processor."""
    import pypar
    if pypar.rank() == 0:
        job_iterator = iter(enumerate(task_list))
        #import threading
        #i_thread = threading.Thread(target= lambda : _mpi_assign_thread(job_iterator))
        # i_thread.start()

        # kluge:
        i_thread = None
        _mpi_assign_thread(job_iterator)
        while True:
            try:
                job = job_iterator.next()[0]
                print("Manager --> Doing job", job, "of", len(task_list), "myself")
                yield task_list[job]
            except StopIteration:
                print("Manager --> Out of jobs message to myself")
                if i_thread is not None:
                    i_thread.join()
                _mpi_end_embarrass()
                return

    while True:

        pypar.send(pypar.rank(), tag=1, destination=0)
        job = pypar.receive(0, tag=2)

        if job is None:
            _mpi_end_embarrass()
            return
        else:
            yield task_list[job]

    _mpi_end_embarrass()


def embarrass(file_list, pre_roll=0, post_roll=0):
    """Get a file list for this node (embarrassing parallelization)"""
    global _mpi_initialized

    if type(file_list) == set:
        file_list = list(file_list)

    import sys
    try:
        proc = int(sys.argv[-2])
        of = int(sys.argv[-1])
    except (IndexError, ValueError):
        if pre_roll != 0 or post_roll != 0:
            raise AssertionError(
                "Pre/post-roll no longer supported for MPI -- non-contiguuous")
        print("Trying to run in MPI mode...")
        import pypar

        _mpi_initialized = True

        proc = pypar.rank() + 1
        of = pypar.size()
        print("Success!", proc, "of", of)

        return _mpi_iterate(file_list)

    i = (len(file_list) * (proc - 1)) / of
    j = (len(file_list) * proc) / of - 1
    assert proc <= of and proc > 0
    if proc == of:
        j += 1
    print(proc, "processing", i, j, "(inclusive)")

    i -= pre_roll
    j += post_roll

    if i < 0:
        i = 0
    if j >= len(file_list):
        j = len(file_list) - 1

    return file_list[i:j + 1]


def _mpi_end_embarrass():
    global _mpi_initialized
    if _mpi_initialized:
        import pypar
        print(pypar.rank() + 1, " of ", pypar.size(), ": BARRIER")
        pypar.barrier()
        print(pypar.rank() + 1, " of ", pypar.size(), ": FINALIZE")
        pypar.finalize()
        _mpi_initialized = False
    else:
        print("Non-MPI run : Exit without MPI_Finalize")


def end_embarrass():
    print("end_embarrass is deprecated")


def failmsg(m):
    """Pretty-print a failure message"""
    msg = "* FAIL " + m + " *"
    print("*" * len(msg))
    print(msg)
    print("*" * len(msg))


if __name__ == "__main__":
    print("Scanning...")

    if "idl" in sys.argv:
        only_idl = True
        del sys.argv[sys.argv.index("idl")]

    par = False

    if "par" in sys.argv:
        par = True
        del sys.argv[sys.argv.index("par")]

    restr = None
    if "only" in sys.argv:
        restr = sys.argv[sys.argv.index("only") + 1]
        del sys.argv[sys.argv.index("only"):sys.argv.index("only") + 2]

    res = None
    if "res" in sys.argv:
        res = int(sys.argv[sys.argv.index("res") + 1])
        del sys.argv[sys.argv.index("res"):sys.argv.index("res") + 2]

    no_idl = False
    if "no_idl" in sys.argv or "no-idl" in sys.argv:
        no_idl = True
        try:
            sys.argv.remove("no_idl")
        except:
            pass
        try:
            sys.argv.remove("no-idl")
        except:
            pass

    if len(sys.argv) > 1:
        max_traverse_depth = int(sys.argv[1])

    print("Maximum number of folders deep = ", max_traverse_depth)

    if not only_idl:
        outputs = find() 

        outputs_ahf = ahf_dejunk(find("AHF_halos"))

        to_amiga = outputs - outputs_ahf

        if restr is not None:
            to_amiga = [x for x in to_amiga if restr in x]

        to_amiga = sorted(to_amiga)

        print("Found", len(outputs), "outputs")
        print(len(outputs_ahf), "with AHF already run, so...")
        print("**** RUNNING AMIGA ON", len(to_amiga), "OUTPUTS ****")
        if len(to_amiga) != 0:
            print("**** Here is the list of outputs which I'm going to AMIGA ... ****")
            print(to_amiga)
            print("**** Starting AMIGA runs... ****")

        if par:
            to_amiga = embarrass(to_amiga)

        for i in to_amiga:
            print("  Processing", i)

            path = ("/".join(i.split("/")[:-1]))
            if path == "":
                path = "."

            if newstyle_amiga:
                amiga_param_file = i + ".AHF_param"
                pf = open(amiga_param_file, "w")

                tpars = info_from_params(get_param_file(i), None)

                lgrid = 65536  # for 768 run

                if res is None:
                    print("res from ",i)
                    try:
                        res = int(
                            re.findall("([0-9][0-9][0-9]+)(g|.0|.tip)", i.split("/")[-1])[0][0])
                    except (IndexError, ValueError):
                        if res is None:
                            raise RuntimeError("Cannot work out run resolution from filename")

                print("res=",res)
                base = 768
                if "cosmo6" in i:
                    base = 192

                try:
                    import pynbody
                    f = pynbody.load(i)
                    scalefac = f.properties['a']
                    if scalefac < 0.2:
                        scalefac = 0.2
                except ImportError:
                    scalefac = 1.0

                lgrid *= 2 ** int(math.log(scalefac *
                                           res / base) / math.log(2))
                print(res, "->", lgrid)

                print(amiga_params % tuple([i, i, lgrid] + tpars), file=pf)
                pf.close()

                start_run = amiga_param_file

            else:
                tipsy_info_file = path + "/tipsy.info"

                if not os.path.isfile(tipsy_info_file):
                    print("   > creating ", tipsy_info_file)
                    pfile = get_param_file(i)
                    print("   > param file is ", pfile)
                    info_from_params(pfile, tipsy_info_file)

                tname = i.split("/")[-1]

                start_run = i + ".AHF_startrun"
                srf = open(start_run, "w")
                print(tname + " 90 1", file=srf)
                print(tname, file=srf)
                print(amiga_params, file=srf)
                print("# Auto-created by " + identifier, file=srf)

                srf.close()  # close file efore launching amiga

            try:
                # basic check that file is readable
                f = open(i)
                f.close()

                if os.system(amiga_command % (path, start_run.split("/")[-1])) != 0 and not ignore_error:
                    raise RuntimeError("Command exited with error")

                # the following so that a double ctrl^c definitely exits even if
                # return vals from os.system not playing ball
                time.sleep(1)

            except IOError:
                ex = "* FAIL on reading " + i + " *"
                print("*" * len(ex))
                print(ex)
                print("*" * len(ex))

        print("<>" * 20)

    if no_idl:
        sys.exit(0)

    # Re-assess the situation
    outputs_ahf = ahf_dejunk(find("AHF_halos"))
    outputs_alyson = find("amiga.grp")

    # print "Found",len(outputs_ahf),"outputs with AMIGA files"
    # print "Found",len(outputs_alyson),"with Alyson's magic"
    to_alyson = outputs_ahf - outputs_alyson
    to_alyson = sorted(to_alyson)
    print("**** RUNNING ALYSON'S SCRIPT ON", len(to_alyson), "OUTPUTS ****")

    if len(to_alyson) != 0:
        print("**** Here is the list of things I'm running Alyson's script on ****")
        print(to_alyson)
        print("**** Starting Alyson's script runs... ****")

    # HEALTH WARNING -- assumes the value of h0
    h0 = 0.73
    

    if par:
        to_alyson = embarrass(to_alyson)

    for i in to_alyson:
        h0 = info_from_params(get_param_file(i), None, return_hubble=True)
        print("  processing", i, "h0=",h0)
        path = ("/".join(i.split("/")[:-1]))
        if path == "":
            path = "."

        amiga_in = glob.glob(i + "*AHF_halos")[0]  # guaranteed to exist now
        zspec = ahf_getjunk(amiga_in)
        start_run = i + ".IDL_startrun"
        srf = open(start_run, "w")
        tipsy_if = open(path + "/tipsy.info")
        tipsy_if.readline()
        tipsy_if.readline()
        dunit = float(tipsy_if.readline().strip().split(" ")[0]) * 1000
        vunit = float(tipsy_if.readline().strip().split(" ")[0])
        munit = float(tipsy_if.readline().strip().split(" ")[0]) / h0
        tipsy_if.close()
        print(idl_preamble, file=srf)
        if idl_pass_z:
            print(idl_proc_name + ",'" + i + "','" + zspec + \
                "',", dunit, ",munit=", munit, ",vunit=", vunit, ",h0=", h0, file=srf)
        else:
            print(idl_proc_name + ",'" + i + \
                "',boxsize=%e,munit=%e,vunit=%e,h0=%f" % (
                    dunit, munit, vunit, h0), file=srf)
        print("exit", file=srf)
        print("; These are the commands which were passed to IDL by " + \
            identifier, file=srf)
        del srf

        if os.system(idl_command + " " + start_run) != 0 and not ignore_idl_error:
            raise RuntimeError("Error reported from IDL")
