#!/usr/bin/env python3

import usb.core
import usb.util
import functools

def init():
    # find our device
    dev = usb.core.find(idVendor=0x1a86, idProduct=0x5537)

    # was it found?
    if dev is None:
        raise ValueError('Device not found')

    # get an endpoint instance
    cfg = dev.get_active_configuration()
    intf = cfg[(0,0)]

    ep_in = usb.util.find_descriptor(
        intf,
        custom_match = \
        lambda e: \
            usb.util.endpoint_direction(e.bEndpointAddress) == \
            usb.util.ENDPOINT_IN)
    print(str(ep_in))
    assert ep_in is not None

    ep_out = usb.util.find_descriptor(
        intf,
        custom_match = \
        lambda e: \
            usb.util.endpoint_direction(e.bEndpointAddress) == \
            usb.util.ENDPOINT_OUT)
    print(str(ep_out))

    assert ep_out is not None

    return (ep_in, ep_out)

ep_in, ep_out = init()

def sequence():
    ep_out.write(functools.reduce(lambda a,b: a + b, [i.to_bytes(4, 'little') for i in range(1024)]))

def patterns():
    zeroes()
    ones()
    fives()
    aas()

def aas():
    ep_out.write([0xaa for i in range(4096)])

def fives():
    ep_out.write([0x55 for i in range(4096)])

def ones():
    ep_out.write([0xff for i in range(4096)])

def zeroes():
    ep_out.write([0x00 for i in range(4096)])
