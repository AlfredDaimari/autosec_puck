from struct import *
from rflib import *
from keyfob import KeyFobPacket
from time import sleep


class RfSender:
    """
    This class is for initialising an RF device
    """

    def __init__(self) -> None:
        self.device = RfCat()

    def send_message(self, rfmsg: object, mod_msg: list) -> None:
        """
        Send a message using the rf device \n
        :param rfmsg: instance of class RfMessage
        :param mod_msg: [[packets to send][amount of time to wait before sending message]]
        """
        self.device.setModeIDLE()

        self.device.setMdmModulation(rfmsg.modulation)
        self.device.setFreq(rfmsg.frequency)
        self.device.makePktFLEN(rfmsg.packet_length)
        self.device.setMdmSyncMode(0)  # Disable sync word and preamble as this is not used by remote
        self.device.setMdmDRate(rfmsg.baud_rate)  # This sets the modulation
        self.device.setModeTX()  # This is the transmitter mode

        for i in range(len(mod_msg[0])):
            try:
                sleep(mod_msg[1][i])
                self.device.RFxmit(mod_msg[0][i])
            except:
                print("Error in sending message!")
                return

        self.device.setModeIDLE()
        print("Message sent!")


class RfMessage:
    """
    Create an rf message to be sent using RfSender \n
    """

    def __init__(self, msg: object, mod_type: str, baud_rate: int, pk_len: int, dev: object, freq=433920000) -> None:
        """
        Create RfMessage \n
        :param msg: the message to send
        :param mod_type: the modulation type to use for the message
        :param baud_rate: message baud_rate
        :param pk_len: the length of the packet,
        :param dev: the rf device (yardstick) (should be an instance of class RfSender)
        :param freq:  the frequency in which to send the packet in
        """
        if not isinstance(msg, KeyFobPacket):
            raise TypeError("msg is not an instance of KeyFobPacket")

        self.message = msg
        self.frequency = freq
        self.modulation_type = mod_type
        self.baud_rate = baud_rate
        self.packet_length = pk_len
        self.dev = dev

    def __create_dispatchable_message(self) -> list:
        """
        Will create a dispatchable message, along with wait times
        :return: returns [[array of  packets to send][amount of time to wait send the next message]]
        """
        self.message.convert_to_decimal()
        pkt_arr = []
        time_arr = []
        for i in range(len(self.message)):
            packed_msg = pack(">Q", self.message.packets[i])
            pkt_arr.append(packed_msg)
            time_arr.append(self.message.time_to_prev_pk(i))

        return [pkt_arr, time_arr]

    def send(self) -> None:
        """
        sends message using the yardstick
        """
        dsp_msg = self.__create_dispatchable_message()
        self.dev.send_message(self, dsp_msg)
