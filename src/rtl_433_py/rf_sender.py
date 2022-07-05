import time, sys, rflib, struct
from rflib import *
from struct import *


class RfSender:
    """
    This class is for initialising an RF device
    """

    def __init__(self) -> None:
        self.device = RfCat()

    def send_message(self, msg: object) -> None:
        """
        Sends a message using the rf device \n
        :param msg: an object of RfMessage
        """
        if not isinstance(msg, RfMessage):
            raise TypeError("msg is not instance of RfMessage")

        self.device.setMdmModulation(msg.modulation)
        self.device.setFreq(self.frequency)
        self.device.makePktFLEN(self.packet_length)
        self.device.setMdmSyncMode(0)  # Disable syncword and preamble as this is not used by remote
        self.device.setMdmDRate(self.baud_rate)  # This sets the modulation
        # d.setMaxPower
        self.device.setModeTX()  # This is the transmitter mode

        mod_msg = int(self.message, 2)
        packed_msg = pack(">Q", mod_msg)
        packed_msg_len = len(packed_msg)    # ? why is this needed

        try:
            self.device.RFxmit(packed_msg)
            print("Message sent!")
        except:
            print("Error in sending message!")
        self.device.setModeIDLE()


class RfMessage:
    """
    This class is for creating a rf message to be sent using RfSender \n
    """

    def __init__(self, msg: str, mod_type: str, baud_rate: int, pk_len: int, dev:object, freq=433920000) -> None:
        """
        Create RfMessage \n
        :param msg: the message to send
        :param mod_type: the modulation type to use for the message
        :param baud_rate: message baud_rate
        :param pk_len: the length of the packet,
        :param dev: the rf device (yardstick) (should be an instance of class RfSender)
        :param freq:  the frequency in which to send the packet in
        """
        self.message = msg
        self.frequency = freq
        self.modulation_type = mod_type
        self.baud_rate = baud_rate
        self.packet_length = pk_len
        self.dev = dev

        self.__convert_msg_to_hex()

    def __convert_msg_to_hex(self) -> None:
        """
        converts the message to hex
        - Karan Handa
        """
        pass

    def send(self) -> None:
        """
        sends message using the yardstick
        """
        self.dev.send_message(self)


