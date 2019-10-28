#!/usr/bin/env python3

from subprocess import check_output
from random import random, randint
from compare_json import eq_str_json_list
from multiprocessing import Pool, Array
from time import sleep, time
from functools import partial

exe = ["fad_cpp", "fad_ml", "bad_cpp", "bad_ml"]
global_env = {}

def make_cmd(exe, *args, **kwargs):
    res = ["./%s" % exe]
    for arg in args:
        res += [arg]
    for k,v in kwargs.items():
        res += ["-%s" % k, str(v)]
    return res

def get_str_jsons(nsteps, dt):
    cmds = map(lambda exe: make_cmd(exe, n=nsteps, dt=dt), exe)
    outs = map(check_output, cmds)
    return map(lambda b: b.decode("utf8"), outs)

def compare_once(nsteps, dt):
    jsons = list(get_str_jsons(nsteps, dt))
    ok = eq_str_json_list(jsons, ["exec_time"])

    return jsons, ok

def compare_(id, n, mindt=0., maxdt=1., minsteps=0, maxsteps=2, verbose=False,
             **kwargs):
    starttime = time()
    padsize = len(str(n))
    for i in range(n):
        global_env["progress"][id] = i
        if verbose:
            cur_time = time() - starttime;
            print("testing: | %*d/%d | (approx time: %.2fs)" %\
                (padsize, i, n, cur_time), end="\r")
        nsteps = randint(minsteps, maxsteps)
        dt = random() * (maxdt - mindt) + mindt

        jsons, ok = compare_once(nsteps, dt)

        if (not ok):
            if verbose:
                print()
                print("Failure with JSONs:")
                for js in jsons:
                    print("\t%s" % js)
            return jsons, False
    if verbose: print()
    return [], True

def compare(n, **kwargs): return compare_(0, n, verbose=True, **kwargs)

def compare_parallel(n, nprocess=4, **kwargs):
    quotient = int(n / nprocess)
    remainder = n % nprocess
    total_runs = [quotient]*nprocess
    for i in range(remainder):
        total_runs[i] += 1
    padsize = len(str(total_runs[0]))

    with Pool(nprocess) as p:
        args = [(i, total_runs[i]) for i in range(nprocess)]
        res = p.starmap_async(partial(compare_, **kwargs), args)
        count = 0
        while True:
            res.wait(0)
            if (res.ready()):
                break
            else:
                cur_count = ""
                for i in range(nprocess):
                    cur_count += "%*d/%d | " %\
                        (padsize, global_env["progress"][i], args[i][1])
                print("testing: |", cur_count, "(approx time: %.2fs)" %\
                        (count / 10), end="\r")
            count += 1
            sleep(0.1)
        p.close()
        p.join()
    for (jsons, ok) in res.get():
        if (not ok):
            print()
            print("Failure with JSONs:")
            for js in jsons:
                print("\t%s" % js)
            return jsons, False
    print()
    return [], True



if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="runs fad_cpp, fad_ml, \
    bad_cpp and bad_ml with the same arguments nstep and dt and checks that \
    their results are equal")
    parser.add_argument('-n', '-ntests', type=int, default=50,
                        help='number of tests to run')
    parser.add_argument('-j', '-nprocesses', type=int, default=8,
                        help='number of processes to spawn')
    parser.add_argument('-minsteps', type=int, default=0,
                        help='minimal number of steps')
    parser.add_argument('-maxsteps', type=int, default=2,
                        help='maximal number of steps')
    parser.add_argument('-mindt', type=float, default=0.,
                        help='minimal size of step')
    parser.add_argument('-maxdt', type=float, default=1.,
                        help='maximal size of step')
    args = parser.parse_args();

    global_env["progress"] = Array('i', args.j)

    kwargs = { "ntests": args.n, "nprocesses": args.j,
               "minsteps": args.minsteps, "maxsteps": args.maxsteps,
               "mindt": args.mindt, "maxdt": args.maxdt }

    print("Options:", kwargs)

    if args.j == 1:
        _, ok = compare(args.n, **kwargs)
    else:
        _, ok = compare_parallel(args.n, nprocess=args.j, **kwargs)
    if (ok):
        print("OK")
        exit(0)
    else:
        print("NOT OK")
        exit(1)