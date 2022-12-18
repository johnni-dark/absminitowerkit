import os
import sys
import time
import datetime
from pathlib import Path
from datetime import datetime
from demo_opts import get_device
from luma.core.render import canvas
from PIL import ImageFont
import psutil
import subprocess as sp
from subprocess import check_output
from re import findall

def bytes2human(n):
    """
    >>> bytes2human(10000)
    '9K'
    >>> bytes2human(100001221)
    '95M'
    """
    symbols = ('K', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y')
    prefix = {}
    for i, s in enumerate(symbols):
        prefix[s] = 1 << (i + 1) * 10
    for s in reversed(symbols):
        if n >= prefix[s]:
            value = int(float(n) / prefix[s])
            return '%s%s' % (value, s)
    return "%sB" % n



def cpu_usage():
    # load average
    av1, av2, av3 = os.getloadavg()
    return "Ld:%.1f %.1f %.1f " % (av1, av2, av3)


def clock():
    #date time
    today = datetime.today()
    return ( today.strftime("%d.%m.%Y-%H:%M") )


def get_temp():
    temp = check_output(["vcgencmd","measure_temp"]).decode("UTF-8")
    return "Temp CPU:+"+ (findall("\d+\.\d+",temp)[0])+ "°C"



def uptime_usage():
    # Ip
    ip = sp.getoutput("hostname -I").split(' ')[0]
    return "IP:%s" % (ip)
    

def mem_usage():
    usage = psutil.virtual_memory()
    return "Mem: %s %.0f%%" \
        % (bytes2human(usage.used), 100 - usage.percent)


def disk_usage(dir):
    usage = psutil.disk_usage(dir)
    return "SD:  %s %.0f%%" \
        % (bytes2human(usage.used), usage.percent)


def network(iface):
    stat = psutil.net_io_counters(pernic=True)[iface]
    return "%s: Tx%s, Rx%s" % \
           (iface, bytes2human(stat.bytes_sent), bytes2human(stat.bytes_recv))


def stats(device):
    # use custom font
    font_path = '/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf'
    font2 = ImageFont.truetype(font_path, 11)

    with canvas(device) as draw:

        if device.height >= 32:
            draw.text((0, 24), mem_usage(), font=font2, fill="white")

        if device.height >= 64:
            draw.text((0, 36), disk_usage('/'), font=font2, fill="white")
            try:
                draw.text((0, 12), get_temp(), font=font2, fill="white")
                draw.text((0, 1), clock(), font=font2, fill="white")
                draw.text((0, 48), uptime_usage(), font=font2, fill="white")

            except KeyError:
                # no wifi enabled/available
                pass


device = get_device()

while True:
    stats(device)
    time.sleep(5)
