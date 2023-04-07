from functools import partial
import multiprocessing
import numpy as np
from scapy.all import *
from scapy.layers.inet import *
from scapy.layers.ntp import *
import signal
from tqdm import tqdm

from .blackbox import Blackbox


def _ignore_sigint():
    signal.signal(signal.SIGINT, signal.SIG_IGN)


def _query_worker(field_dict, timeouts, server_ip, delay_between):
    """Modified from:
    https://github.com/ampmap-cmu/ampmap/blob/main/src/libs/blackbox.py
    """
    if field_dict["mode"] == 6:
        # in control mode 6
        payload = NTPPrivate()
    elif field_dict["mode"] == 7:
        # in private mode 7
        payload = NTPControl()
    else:
        # in normal mode
        payload = NTPHeader()

    for fid, val in field_dict.items():
        setattr(payload, fid, val)

    request = IP(dst=server_ip)/UDP(sport=random.randint(5000, 65535), dport=123)/payload

    for timeout in timeouts:
        response, unans = sr(request, multi=True, timeout=timeout, verbose=0)
        if response is not None:
            time.sleep(delay_between)
            response_len = sum([len(x[1]) for x in response])
            return float(response_len) / float(len(request))

        print("No response for {} seconds: {}".format(timeout, field_dict))
        sys.stdout.flush()
        time.sleep(timeout)

    print("No response: {}".format(field_dict))
    sys.stdout.flush()
    return 0


class NTPBlackbox(Blackbox):
    def __init__(self, server_ip,
                 timeouts=[0.01, 0.05, 1.0, 2.0, 4.0, 8.0],
                 num_process=1,
                 delay_between=0.02):
        self._server_ip = server_ip
        self._timeouts = timeouts
        self._num_process = num_process
        self._delay_between = delay_between

        self._pool = multiprocessing.Pool(
            processes=self._num_process,
            initializer=_ignore_sigint)

    def query(self, field_dict_inputs):
        amplifications = []
        for amplification in tqdm(self._pool.imap(
                partial(_query_worker,
                        msg_type=self._msg_type,
                        timeouts=self._timeouts,
                        server_ip=self._server_ip,
                        delay_between=self._delay_between),
                field_dict_inputs),
                total=len(field_dict_inputs)):
            amplifications.append(amplification)
        return np.asarray(amplifications)
