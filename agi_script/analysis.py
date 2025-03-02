from datetime import datetime
import json

def ts():
    now = datetime.now()
    return now.strftime("%d%m%Y-%H:%M:%S")

target = "trace.txt"
outFile = ts() + '.json'
timeAligned = False

'''
one metric
 {
 "ts" : [list of ts]
 "v1" : [list of v1]
 "v2" : [list of v2]
 }

all metric
{
"metric_name": metric_obj
}
'''

memKeys = ['ts', 'total', 'free', 'buffer', 'cached', 'swap']

batteryKeys = ['ts', 'charge', 'percent', 'current']
# battery charge capacity in uah; current in ua, negative means inflow

GPUcounterKeys = ['ts', 'clocks', 'utilization', 'bus', 'read', 'write']
# "GPU clocks per sec"                # 1
# "GPU percent utilization"           # 3
# "GPU bus busy percent"              # 104
# "GPU read bytes per sec"            # 145
# "GPU write bytes per sec"           # 146

o = {
    "clock ts alignment" : {},
    "CPU memory": {i:[] for i in memKeys},                       # meminfo
    "battery" : {i:[] for i in batteryKeys},                         # battery
    "GPU memory" : {"ts":[], "size":[]},                      # gpu_mem_total, pid:0
    "GPU frequency" : {"ts":[], "freq":[]},                   # gpu_frequency
    "GPU counters" : {i:[] for i in GPUcounterKeys},                    #
}

with open(target, "r") as f:
    raw = f.readlines()

getV = lambda x: int(x.split(": ")[-1])
getF = lambda x: float(x.split(": ")[-1])
getTs = getV

for i in range(len(raw)):

    if not timeAligned and 'clock_snapshot {' in raw[i]:
        o['clock ts alignment']['ts'] = [
            getTs(raw[i+4]), getTs(raw[i+8]), getTs(raw[i+12]), getTs(raw[i+16]), getTs(raw[i+20]), getTs(raw[i+24]),
        ]

    if "key: MEMINFO_MEM_TOTAL" in raw[i]:
        ts = getTs(raw[i-3]);       o['CPU memory']['ts'].append(ts)
        mtotal = getV(raw[i+1]);    o['CPU memory']['total'].append(mtotal)
        mfree = getV(raw[i+5]);     o['CPU memory']['free'].append(mfree)
        mbuffer = getV(raw[i+9]);   o['CPU memory']['buffer'].append(mbuffer)
        mcached = getV(raw[i+13]);  o['CPU memory']['cached'].append(mcached)
        mswap = getV(raw[i+17]);    o['CPU memory']['swap'].append(mswap)
        continue

    if "battery {" in raw[i] and "charge_counter_uah:" in raw[i+1]:
        ts = getTs(raw[i-1]);       o['battery']['ts'].append(ts)
        bcharge = getV(raw[i+1]);   o['battery']['charge'].append(bcharge)
        bpercent = getF(raw[i+2]);  o['battery']['percent'].append(bpercent)
        bcurrent = getV(raw[i+3]);  o['battery']['current'].append(bcurrent)
        continue

    if "gpu_mem_total {" in raw[i] and "pid: 0" in raw[i+2]:
        ts = getTs(raw[i-2]);       o['GPU memory']['ts'].append(ts)
        size = getV(raw[i+3]);      o['GPU memory']['size'].append(size)
        continue

    if "gpu_frequency {" in raw[i]:
        ts = getTs(raw[i-2]);       o['GPU frequency']['ts'].append(ts)
        freq = getV(raw[i+2]);      o['GPU frequency']['freq'].append(freq)
        continue

    if "gpu_counter_event {" in raw[i] and "counters {" in raw[i+1]:
        ts = getTs(raw[i-1]);       o['GPU counters']['ts'].append(ts)
        c1 = getF(raw[i+3]);        o['GPU counters']['clocks'].append(c1)
        c3 = getF(raw[i+7]);        o['GPU counters']['utilization'].append(c3)
        c104 = getF(raw[i+11]);     o['GPU counters']['bus'].append(c104)
        c145 = getF(raw[i+15]);     o['GPU counters']['read'].append(c145)
        c146 = getF(raw[i+19]);     o['GPU counters']['write'].append(c146)
        continue

with open(outFile, "w+") as f:
    f.write(json.dumps(o, indent=' '))