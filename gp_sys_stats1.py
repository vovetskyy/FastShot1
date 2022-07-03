import psutil
from scapy.all import *
from pprint import pprint as pp

# variable to start/stop sniffing using scapy
meas_running = False
# all network adapter's MAC addresses
all_macs = {}
# A dictionary to map each connection to its corresponding process ID (PID)
connection2pid = {}
# A dictionary to map each process ID (PID) to total Upload (0) and Download (1) traffic
pid2traffic = defaultdict(lambda: [0, 0])

sniff_count = 0


# ---------------------------------------
# General measurements handling part

def init_measurements():
    global meas_running
    global all_macs

    # ensure default state of non-sniffing
    meas_running = False

    # foo execution of psutil.cpu_percent(), as 1st time it will return a meaningless 0.0 value
    # see https://psutil.readthedocs.io/en/latest/#psutil.cpu_percent for details
    psutil.cpu_percent()

    # foo loop over cpu_percent, as 1st time it always returns meaningless 0.0
    # See https://psutil.readthedocs.io/en/latest/#psutil.Process.cpu_percent for details
    for p in psutil.process_iter(['name']):
        foo = p.cpu_percent()

    # get the all network adapter's MAC addresses
    all_macs = {iface.mac for iface in ifaces.values()}


def start_measurements():
    global meas_running

    meas_running = True

    # start connection cyclic monitoring in the separate thread
    connections_thread = Thread(target=get_connections)
    connections_thread.start()

    # start scapy.sniff in the separate thread, as otherwise start_measurements will never return
    sniff_thread = Thread(target=start_sniffing)
    sniff_thread.start()

    # sniff(prn=test_func, count=10, store=False, stop_filter=is_measurement_running)


def stop_measurements():
    global meas_running

    meas_running = False
    # pp(pid2traffic)


def is_measurement_running(x):
    global meas_running

    return not meas_running



# ---------------------------------------
# Network sniffing part
# details about getting of network load per process see in
# https://www.thepythoncode.com/article/make-a-network-usage-monitor-in-python#network-usage-per-process

def start_sniffing():
    sniff(prn=process_packet, count=0, store=False, stop_filter=is_measurement_running)


def get_connections():
    """A function that keeps listening for connections on this machine
    and adds them to `connection2pid` global variable"""
    global connection2pid
    while meas_running:
        # using psutil, we can grab each connection's source and destination ports
        # and their process ID
        for c in psutil.net_connections():
            if c.laddr and c.raddr and c.pid:
                # if local address, remote address and PID are in the connection
                # add them to our global dictionary
                connection2pid[(c.laddr.port, c.raddr.port)] = c.pid
                connection2pid[(c.raddr.port, c.laddr.port)] = c.pid

        # sleep for a second, feel free to adjust this
        time.sleep(1)


def process_packet(packet_info):
    global pid2traffic
    global sniff_count
#    print('Process packets')
#    pp(packet_info)
    try:
        # get the packet source & destination IP addresses and ports
        packet_connection = (packet_info.sport, packet_info.dport)
    except (AttributeError, IndexError):
        # sometimes the packet does not have TCP/UDP layers, we just ignore these packets
        pass
    else:
        # get the PID responsible for this connection from our `connection2pid` global dictionary
        packet_pid = connection2pid.get(packet_connection)
        if packet_pid:
            if packet_info.src in all_macs:
                # the source MAC address of the packet is our MAC address
                # so it's an outgoing packet, meaning it's upload
                pid2traffic[packet_pid][0] += len(packet_info)
            else:
                # incoming packet, download
                pid2traffic[packet_pid][1] += len(packet_info)
    sniff_count +=1


# ---------------------------------------
# Statistic collection part

def get_cpu_net_stats():
    detailed_net_stats = {}

    net_io_detailed = psutil.net_io_counters(pernic=True)
    for netif, load in net_io_detailed.items():
        bytes_sent = load.bytes_sent
        bytes_recv = load.bytes_recv
        id_str = 'NET(' + netif + '), sent/received, bytes'
        detailed_net_stats[id_str] = (bytes_sent, bytes_recv)

    # pp(net_io_detailed)
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
    cpus['NET, per Interface:'] = get_cpu_net_stats()

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
                              {'Network Total, sent/received, bytes': pid2traffic[p.pid]})

    # pp(pid2traffic)
    # pp(procs)
    return procs
