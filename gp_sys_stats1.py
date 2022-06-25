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


def get_cpu_stats():
    cpus = {}

    cpus['CPU: Num of cores'] = psutil.cpu_count();
    cpus['CPU: Load, %, per core'] = psutil.cpu_percent(percpu=True)
    cpus['CPU: Times, seconds, per core'] = psutil.cpu_times(percpu=True)
    cpus['CPU: Freq, MHz, per core'] = psutil.cpu_freq(percpu=True)

    mem = psutil.virtual_memory()
    cpus['MEM: total/used/available, bytes'] = (mem.total, mem.used, mem.available)

    disk_io = psutil.disk_io_counters()
    cpus['IO, read/write, bytes'] = (disk_io.read_bytes, disk_io.write_bytes)
    cpus['IO, read/write, milliseconds'] = (disk_io.read_time, disk_io.write_time)

    net_io = psutil.net_io_counters()
    cpus['NET, sent/received, bytes'] = (net_io.bytes_sent, net_io.bytes_recv)

    return cpus


def get_process_stats():
    procs = {}

    core_cnt = psutil.cpu_count()

    for p in psutil.process_iter(['name']):
        io_counters = p.io_counters()
        procs[p.name()] = ({'CPU load, %': (p.cpu_percent() / core_cnt)},
                           {'MemUsage, bytes': (p.memory_info().rss)},
                           {'IO Reads/writes/other, bytes': (io_counters.read_bytes, io_counters.write_bytes,
                                                             io_counters.other_bytes)},
                           {'Network': ('TBD')})
    return procs
