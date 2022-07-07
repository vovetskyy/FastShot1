import sys
import time
from datetime import datetime
from pprint import pprint as pp

import gp_sys_stats1 as gpss

DEF_LOOPS = 3

timed_stats = {}

def meas_loop(loops_count):
    global timed_stats

    # ---------------------------------
    # do measurements
    for i in range(1, loops_count + 1):
        timestamp = datetime.now()

        sys_stats = gpss.get_sys_stats()
        cpu_stats = gpss.get_cpu_stats()
        gpu_stats = gpss.get_gpu_stats()
        procs_stats = gpss.get_process_stats()

        # 2022_06_25_17_30_54_915740_ as unique id for the measurement
        # (expected to be used for synchronization with other measurements)
        datetime_str = timestamp.strftime('%Y_%m_%d_%H_%M_%S_%f_%Z')

        timed_stats[datetime_str] = ({'SYS Stats': sys_stats}, {'CPU Stats': cpu_stats}, {'GPU Stats': gpu_stats}, {'Processes Stats': procs_stats})



if __name__ == '__main__':
    # parameters:
    # %1 -- number of measurement loops (DEF_LOOPS by default)
    num_loops = DEF_LOOPS

    start_time = time.time()

    # ---------------------------------
    # calculate number of loops
    if(len(sys.argv) > 1):
        try:
            num_loops = int(sys.argv[1])
        except:
            print('Can\'t covert \"' + sys.argv[1] + '\" to (int). Default value ' + str(DEF_LOOPS) + ' is used.')


    # ---------------------------------
    # prepare measurements
    gpss.init_measurements()
    gpss.start_measurements()

    meas_loop(num_loops)

    gpss.stop_measurements()

    # ---------------------------------
    # prepare results
    pp(timed_stats)

    # ---------------------------------
    # print script's runtime info to STDERR
    script_time = time.time() - start_time
    print('Scripttime: ' + str(script_time) + ' sec', file=sys.stderr)
    print('Avg. time per measurement: ' + str(script_time/num_loops) + ' sec', file=sys.stderr)
