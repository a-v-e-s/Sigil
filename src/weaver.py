from multiprocessing import Process, cpu_count
from threading import Thread
from time import sleep

def weaver(targets, args, separate=True, leave_idle=1):
    cpus = cpu_count()
    cpus_to_use = cpus - leave_idle if cpus > 1 else 1
    jobs = []
    count = 0
    for x in targets:
        if separate:
            w = Process(target=x, args=args[count])
        else:
            w = Thread(target=x, args=args[count])
        jobs.append(w)
        count += 1
    #
    running_jobs = []
    for x in range(cpus_to_use):
        try:
            jobs[x].start()
            running_jobs.append(jobs[x])
            jobs.remove(jobs[x])
        except IndexError:
            break
    #
    while jobs:
        sleep(0.5)
        for x in running_jobs:
            if not x.is_alive():
                running_jobs.remove(x)
                jobs[0].start()
                running_jobs.append(jobs[0])
                jobs.remove(jobs[0])
                break
    #
    for x in running_jobs:
        x.join()
