import subprocess
import time
from multiprocessing import Pool


class commonError(Exception):
    def __init__(self, message):
        self.message = message


# [func, [1, 2, 3]]

# single function run, designed for multicore
def funRun(args):
    try:
        fun = args[0]
        param = args[1]
        results = fun(*param)
        flag = True
    except Exception as e:
        results = e
        flag = False

    return results, flag


# single command run, designed for multicore
def cmdRun(cmd):
    print(cmd)
    proc = subprocess.run(
        cmd,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True,
    )
    # get cmd info
    mess = proc.stderr + proc.stdout
    if proc.returncode == 0:
        return mess, True
    else:
        mess1 = "\n\n\nAn Error Occured During The Following Command Line Executing.\n"
        mess2 = "\n         Please Stop The Program To Check The Error.         \n\n\n"
        mess = """^^^{}^^^\n{}\n^^^{}^^^""".format(mess1, cmd, mess2)
        return mess, False


# time counter for multiRun
def track_job(job, time_start, update_interval=3, print_interval=300):
    """
    from stackoverflow
    job: multiprocessing job
    """
    minute_count = 0
    while job._number_left > 0:
        delta_minutes = (time.time() - time_start) // print_interval
        if delta_minutes and (delta_minutes != minute_count):
            print(
                "{0} minutes has passed since the last print".format(delta_minutes * 5)
            )
            print("Tasks remaining = {0}".format(job._number_left * job._chunksize))
            minute_count = delta_minutes

        time.sleep(update_interval)


# multiCore
def multiRun(args, func=None, nCore=4):
    """
    This function is designed for multiCore.

    multiRun(func, args, type, nCore=1)
    {P}arameters:
        args: Parameters for multirun, [[1, 2, 3], [2, 3, 4]] or ["cmd1", "cmd2", "cmd3"].
        func: function name for multicore, None mean cmd mode.
        nCore: int, how many cores to use.
    """
    p = Pool(nCore)
    print("Start multicore running, master process number: {}".format(nCore))
    print(
        "Note: some cmamand line verbose may be blocked, the program will record them in record file."
    )
    time_start = time.time()
    if func is None:
        # in this mode, success means that the output will be stdout, failed means that the output will be False
        results = p.map_async(cmdRun, args)
    else:
        # in this mode, success means that the output will be function output
        reshaped_args = [[[func, x]] for x in args]
        results = p.starmap_async(funRun, reshaped_args)

    # print mess
    print("Subprocesses Start running......")
    print("Waiting for all subprocesses done...")

    track_job(job=results, time_start=time_start, update_interval=3, print_interval=300)

    p.close()
    p.join()
    print("All subprocesses done.")

    if func is None:  # check output for cmd
        messages = [x[0] for x in results.get()]
        flag = [x[1] for x in results.get()]
        mess = "\n\n\n".join([str(x) for x in messages])
        if (all(flag)) and results.successful():
            return mess, True
        else:
            print(mess)
            raise commonError("Error occured in multi-core running!")
    else:  # check output for function
        output = [x[0] for x in results.get()]
        flag = [x[1] for x in results.get()]
        if (all(flag)) and results.successful():
            return output, True
        else:
            print(str(output))
            raise commonError("Error occured in multi-core running!")


# command line demo
args = [
    "fastqc sub1_1.fq",
    "fastqc sub1_2.fq",
    "fastqc sub2_1.fq",
    "fastqc sub2_2.fq",
    "fastqc sub3_1.fq",
    "fastqc sub3_2.fq",
    "fastqc sub5_1.fq",
    "fastqc sub5_2.fq",
    "fastqc sub4_1.fq",
    "fastqc sub4_2.fq",
]


# function demo
def a1(a, b, c):
    o = a + b + c
    return o


func = a1

args = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9],
    [3, 2, 3],
]
