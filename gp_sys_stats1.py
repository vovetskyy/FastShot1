import psutil
from pprint import pprint as pp


def init_measurements():
    # foo execution of psutil.cpu_percent(), as 1st time it will return a meaningless 0.0 value
    # see https://psutil.readthedocs.io/en/latest/#psutil.cpu_percent for details
    psutil.cpu_percent()

    # foo loop over cpu_percent, as 1st time it always returns meaningless 0.0
    # See https://psutil.readthedocs.io/en/latest/#psutil.Process.cpu_percent for details
    for p in psutil.process_iter(['name']):
        foo = p.cpu_percent()

def get_detaied_net_stats():
    detailed_net_stats = {}

    net_io_detailed = psutil.net_io_counters(pernic=True)
    for netif, load in net_io_detailed.items():
        bytes_sent = load.bytes_sent
        bytes_recv = load.bytes_recv
        id_str = 'NET(' + netif + '), sent/received, bytes'
        detailed_net_stats[id_str] = (bytes_sent, bytes_recv)

    #pp(net_io_detailed)
    return detailed_net_stats


def get_cpu_stats():
    cpus = {}

    cpus['CPU: Num of cores'] = psutil.cpu_count()
    cpus['CPU: Load, %, per core'] = psutil.cpu_percent(percpu=True)
    cpus['CPU: Times, seconds, per core'] = psutil.cpu_times(percpu=True)
    cpus['CPU: Freq, MHz, per core'] = psutil.cpu_freq(percpu=True)

    mem = psutil.virtual_memory()
    cpus['MEM: total/used/available, bytes'] = (mem.total, mem.used, mem.available)

    disk_io = psutil.disk_io_counters()
    cpus['IO, read/write, bytes'] = (disk_io.read_bytes, disk_io.write_bytes)
    cpus['IO, read/write, milliseconds'] = (disk_io.read_time, disk_io.write_time)

    # get total network bytes
    net_io = psutil.net_io_counters()
    cpus['NET Total, sent/received, bytes'] = (net_io.bytes_sent, net_io.bytes_recv)

    # get network bytes per interface
    cpus['NET, per Interface:'] = get_detaied_net_stats()

    return cpus


def get_process_stats():
    procs = {}

    core_cnt = psutil.cpu_count()

    for p in psutil.process_iter(['name']):
        # as different processes may have the same name (like "chrome.exe"),
        # combination of name + pid will be used as unique process Id (dictionary keys)
        proc_name = p.name()
        pid_str = str(p.pid)
        proc_id_str = proc_name + '(' + pid_str + ')'

        io_counters = p.io_counters()

        procs[proc_id_str] = ({'Proc name': proc_name},
                              {'Proc Pid': pid_str},
                            # it is recommended to divide reported load by number of cores.
                            # Otherwise load may be even > 100%.
                            # See https://psutil.readthedocs.io/en/latest/#psutil.Process.cpu_percent
                            {'CPU load, %': (p.cpu_percent() / core_cnt)},
                           {'MemUsage, bytes': (p.memory_info().rss)},
                           {'IO Reads/writes/other, bytes': (io_counters.read_bytes, io_counters.write_bytes,
                                                             io_counters.other_bytes)},
                           {'Network': ('TBD')})
    return procs
