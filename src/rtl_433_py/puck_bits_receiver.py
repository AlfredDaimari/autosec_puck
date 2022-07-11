#
#    Creates a dbus service, used to read rf bits sent from rtl_433
#     
#    Copyright (C) 2022 Alfred Daimari 
#    
#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 2 of the License, or
#    (at your option) any later version.
# 

# TODO - write a print function for all the classes


import dbus
import dbus.service
from dbus.mainloop.glib import DBusGMainLoop
from datetime import datetime
from rolling_keyfobs import RollingKeyFobs
from rf import RfSender
from jammer import *

DBusGMainLoop(set_as_default=True)
OPATH = "/org/autosec/PuckBitsReceiver"
IFACE = "org.autosec.PuckBitsReceiverInterface"
BUS_NAME = "org.autosec.PuckBitsReceiver"


class PuckBitsReceiver(dbus.service.Object):
    """ For creating a rf bits listener service on dbus"""

    def __init__(self) -> None:
        bus = dbus.SystemBus()
        bus.request_name(BUS_NAME)
        bus_name = dbus.service.BusName(BUS_NAME, bus=bus)
        dbus.service.Object.__init__(self, bus_name, OPATH)
        print("dbus has been initialized")
        self.rf_device = RfSender()
        print("yardstick has been initialized")
        # TODO: configure for raspberry bi
        self.jammer = Jammer("input_file", "mode", "freq", "sample")
        print("Jammer has been initialized")
        self.rolling_key_fobs = RollingKeyFobs(self.rf_device, self.jammer)
        print("rolling key fobs dts has been created")

    @dbus.service.method(dbus_interface=IFACE, in_signature="s", out_signature="s", sender_keyword="sender",
                         connection_keyword="conn")
    def ReceiveBits(self, bits: str, sender=None, conn=None):
        """
        receiver function for bits
        """
        now = datetime.now()
        dt_string = now.strftime("%H:%M:%S %d/%m/%Y")
        print(f"received: ${bits} at ${dt_string}")
        bit_tmp = bits.split(":")
        bit_string = bit_tmp[0]
        gap = int(bit_tmp[1])
        self.rolling_key_fobs.push(bit_string, gap)
