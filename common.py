# This library provides common funtionality utilized by othe modules

import subprocess as sp
import psutil

def getCpuTemperature() -> float:
    """
    Reads current SoC temperature from VideoCore command tool.
    Returns cpu temperature in grad celcius with one floating point digit.
    """
    res = sp.getoutput("vcgencmd measure_temp|egrep -o '[0-9]*\.[0-9]*'")
    if res != '':
        return float(res)
    return 0.0

def getCpuLoad() -> float:
    """
    Reads actual cpu load.
    Returns cpu load in percentage with one floating point digit.
    """
    return psutil.cpu_percent(None)

def getIP() -> str:
    """
    Read own IP address.
    Returns IPv4 address as a string.
    """
    return sp.getoutput("hostname -I | cut -d' ' -f1")

def getTotalRam() -> float:
    """
    Reads total RAM.
    Returns total RAM amount in Gi.
    """
    res = sp.getoutput("free -m | awk 'NR==2 {printf \"%s\", $2}'")
    if res != '':
        return round(float(res) / 1000, 1)
    return 0.0

def getUsedRam() -> float:
    """
    Reads used RAM.
    Returns used RAM amount in Gi.
    """
    res = sp.getoutput("free -m | awk 'NR==2 {printf \"%s\", $3}'")
    if res != '':
        return round(float(res) / 1000, 1)
    return 0.0

def getTotalSd() -> float:
    """
    Reads total sd card memory.
    Returns total sd card memory in Gi.
    """
    res = sp.getoutput("df -m | grep -w '/dev/root' | awk '{printf \"%s\", $2}'")
    if res != '':
        return round(float(res) / 1000, 1)
    return 0.0

def getUsedSd() -> float:
    """
    Reads used sd card memory.
    Return used sd card memory in Gi.
    """
    res = sp.getoutput("df -m | grep -w '/dev/root' | awk '{printf \"%s\", $3}'")
    if res != '':
        return round(float(res) / 1000, 1)
    return 0.0

def getTotalUsb() -> float:
    """
    Reads total usb card memory.
    Return total usb card memory in Gi.
    """
    res = sp.getoutput("df -m | grep -w '/dev/sda1' | awk '{printf \"%s\", $2}'")
    if res != '':
        return round(float(res) / 1000, 1)
    return 0.0

def getUsedUsb() -> float:
    """
    Reads used usb card memory.
    Return used usb card memory in Gi.
    """
    res = sp.getoutput("df -m | grep -w '/dev/sda1' | awk '{printf \"%s\", $3}'")
    if res != '':
        return round(float(res) / 1000, 1)
    return 0.0
