import pyxid
from psychopy import core
from ctypes import windll


def send_trigger(n=1, port=0x0000D100):
    """Send a trigger ``n`` to the parallel port.

    Parameters
    ----------
    n : int
        Trigger to be sent.
    port : port address
        Adress of the parallel port.

    Returns
    -------
    ``True`` in case of success, ``False`` otherwise.

    """
    try:
        windll.inpout32.Out32(port, n)
        core.wait(0.01)
        windll.inpout32.Out32(port, 0)
        return True
    except Exception:
        print 'Error sending trigger'
        return False


try:
    p = windll.inpout32
    print 'inpout32.dll found.'
except Exception:
    raise RuntimeError('inpout32.dll not found.')


# get a list of all attached XID devices
devices = pyxid.get_xid_devices()

dev = devices[0]
if not dev.is_response_device():
    raise RuntimeError('No response device found.')


dev.reset_base_timer()
dev.reset_rt_timer()

while True:
    dev.poll_for_response()
    if dev.response_queue_size() > 0:
        response = dev.get_next_response()

        if response['pressed']:
            send_trigger(response['key'])