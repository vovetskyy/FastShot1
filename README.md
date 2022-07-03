# GP_FastShot1

## Provided Statistics
### By CPU 
#### General Info
* Number of cores
* Core Freq, Min/Max/Current, MHz
#### Cores utilization
* Core load, %
* Core utilization, ms
#### Virtual Memory
* Total, bytes
* Used, bytes
* Available, bytes
#### Disk I/O
* read bytes
* written bytes
* read operations, ms
* write operations, ms
#### Network:
* sent bytes, total
* received bytes, total
* sent bytes, per Interface
* received bytes, per Interface


### By Process:
#### General Info
* Name
* PID
#### Cores utilization
* CPU load, %, normalized to number of cores
#### Virtual Memory
* Usage, bytes
#### Disk I/O
* read bytes
* written bytes
* other bytes (Windows specific, he number of bytes transferred during operations other than read and write operations. Details see in [psutil Documentation](https://psutil.readthedocs.io/en/latest/))
#### Network:
* sent bytes
* received bytes

** Note: statistics by Interfaces (Ethernet, Bluetooth, etc.) is not provided, as it is possible only for outgoing packages, where MAC-address can be mapped to Interface. details about getting of network load per process see in https://www.thepythoncode.com/article/make-a-network-usage-monitor-in-python#network-usage-per-process 

## Dependencies:
### Python Libraries
* sys
* time
* datetime
* pprint
* [psutil](https://psutil.readthedocs.io/en/latest/)
* [scapy](https://scapy.readthedocs.io/en/latest/usage.html)

### General Libraries
* for scapy: libpcap (On Windows e.g. as [Npcap](https://npcap.com/#download)).
 For details see [StackOverflow](https://stackoverflow.com/questions/68691090/python-scapy-error-no-libpcap-provider-available).
* 
