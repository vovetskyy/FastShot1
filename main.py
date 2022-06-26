import sys
import time
from datetime import datetime
from pprint import pprint as pp

import gp_sys_stats1 as gpss

DEF_LOOPS = 3

if __name__ == '__main__':
    # parameters:
    # %1 -- number of measurement loops (DEF_LOOPS by default)
    num_loops = DEF_LOOPS

    start_time = time.time()
    timed_stats = {}

    if(len(sys.argv) > 1):
        try:
            num_loops = int(sys.argv[1])
        except:
            print('Can\'t covert \"' + sys.argv[1] + '\" to (int). Default value ' + str(DEF_LOOPS) + ' is used.')

    gpss.init_measurements()

    for i in range(1, num_loops+1):
        timestamp = datetime.now()

        cpu_stats = gpss.get_cpu_stats()
        procs_stats = gpss.get_process_stats()

        # 2022_06_25_17_30_54_915740_ as unique id for the measurement
        # (expected to be used for synchronization with other measurements)
        datetime_str = timestamp.strftime('%Y_%m_%d_%H_%M_%S_%f_%Z')

        timed_stats[datetime_str] = ({'CPU Stats': cpu_stats}, {'Processes Stats': procs_stats})

    pp(timed_stats)

#   print(time.time() - start_time)
