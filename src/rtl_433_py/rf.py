import threading
from time import sleep
from typing import List
from struct import *
from rflib import *
from keyfob import KeyFobPacket


class YDSendPacketEvent(threading.Event):
    """
    this class is used to synchronize the two threads when there is a sending event going on \n
    -----
    Attributes: \n
    self.status: False (not sending), True (sending)
    """

    def __init__(self):
        threading.Event.__init__(self)
        self.status = False

    def set_sending(self) -> None:
        """
        starts sending event \n
        stops sending event in 0.25 seconds \n
        """
        self.set()
        self.status = True
        self.__set_not_sending()

    def __stop_sending_in_025(self) -> None:
        """
        changes status of event to not sending in 0.25 seconds
        """
        sleep(0.25)
        self.clear()
        self.status = False

    def __set_not_sending(self):
        new_thread = threading.Thread(target=self.__stop_sending_in_025, args=())
        new_thread.start()
        del new_thread


class RfSender:
    """
    This class is for initialising an RF device
    """

    def __init__(self) -> None:
        self.yd_stick = RfCat()  # RfCat()

    def send_message(self, rfmsg: object, mod_msg: List[str]) -> None:
        """
        Send a message using the rf device \n
        :param rfmsg: instance of class RfMessage
        :param mod_msg: [[packets to send][amount of time to wait before sending message]]
        """
        self.yd_stick.setModeIDLE()

        self.yd_stick.setMdmModulation(rfmsg.modulation_type)
        self.yd_stick.setFreq(rfmsg.frequency)
        self.yd_stick.setChannel(rfmsg.channel)
        self.yd_stick.setMdmSyncMode(0)  # Disable sync word and preamble as this is not used by remote
        self.yd_stick.setMdmDRate(rfmsg.baud_rate)  # This sets the modulation
        self.yd_stick.setModeTX()  # This is the transmitter mode

        for msg in mod_msg:
            try:
                print("sending message!")
                self.yd_stick.RFxmit(msg, repeat=5)
                sleep(0.01)
            except:
                print("Error in sending message!")
                return
        self.yd_stick.setModeIDLE()
        print("Message sent!")


class RfMessage:
    """
    Create an rf message to be sent using RfSender \n
    """

    def __init__(self, msg: List[KeyFobPacket], mod_type: str, baud_rate: int, channel: int, yd_stick: RfSender,
                 freq=433920000) -> None:
        """
        Create RfMessage \n
        :param msg: the message to send
        :param mod_type: the modulation type to use for the message
        :param baud_rate: message baud_rate
        :param pk_len: the length of the packet,
        :param dev: the rf device (yardstick) (should be an instance of class RfSender)
        :param freq:  the frequency in which to send the packet in
        """
        if not isinstance(msg[0], KeyFobPacket):
            raise TypeError("msg is not an instance of KeyFobPacket")

        if not isinstance(yd_stick, RfSender):
            raise TypeError("yd_stick is not an instance of RfSender")

        self.message = msg
        self.frequency = freq
        self.modulation_type = mod_type
        self.baud_rate = baud_rate
        self.channel = channel
        self.yd_stick = yd_stick

    def __create_dispatchable_message(self) -> list:
        """
        Will create a dispatchable message, along with wait times
        :return: returns [[array of  packets to send][amount of time to wait send the next message]]

        """
        pkt_arr = []
        for kfb in self.message:
            kfb.convert_to_hex()
            packed_msg = bytes.fromhex(kfb.get_conc_pkt())
            pkt_arr.append(packed_msg)

        # print(pkt_arr)       

        return pkt_arr

    def send(self) -> None:
        """
        sends message using the yardstick
        """
        dsp_msg = self.__create_dispatchable_message()
        self.yd_stick.send_message(self, dsp_msg)