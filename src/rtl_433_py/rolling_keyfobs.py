from time import time_ns as tns
from rf import *
from keyfob import *
from jammer import *


class RollingKeyFobs:
    """"
    queue to hold the rolling key fob
    sends out the first key fob in, when the length is 2
    """

    def __init__(self) -> None:
        self.key_fobs_list = []

        self.yd_stick = RfSender()
        print("the yardstick has been initialized")

        # TODO: configure for raspberry bi
        self.jammer = Jammer("input_file", "mode", "freq", "sample")
        print("the jammer has been initialized")
        self.jammer.start()

    def __len__(self):
        return len(self.key_fobs_list)

    def __str__(self):
        str_ = ""
        for key_fb_list in self.key_fobs_list:
            for key_fb in key_fb_list:
                str_ += str(key_fb) + '--'
            str_ += "\n--  next key fob --  \n"
        return str_

    @property
    def dispatchable(self) -> bool:
        """
        checks if there are two valid key fobs \n
        and if the previous one can be sent or not
        """
        if len(self) > 1:
            cur_time = tns()
            if (cur_time - self.key_fobs_list[-1][-1].pk_recv_time) < 800000000:
                return True

        return False

    def __shift(self):
        """
        remove the first element from key fob
        """
        return self.key_fobs_list.pop(0)

    def send_fi(self) -> None:
        """
        send the first message in the queue
        :param msg: instance of key fob packet
        """
        keyfob_tb_snt = self.__shift()

        print("key fob to be sent")
        for kfb in keyfob_tb_snt:
            print(kfb)

        # TODO: connect with RfMessage
        # rf_message = RfMessage(msg, MOD_2FSK | MANCHESTER, 4000, 230, self.dev)
        # self.jam.stop()
        # rf_message.send()
        # self.jam.start()

        del keyfob_tb_snt

    def push(self, key_fb_packet: list) -> None:
        """
        add a new key fob to list or concatenate with previous key fob \n
        :param key_fb_packet: a list in the form ["bits:gap", "bits:gap", "name_of_car"]
        """

        if len(key_fb_packet) < 2:
            print("key fob packet is not valid. dropping key fob packet")

        cur_time = tns()
        tmp_keyfob_pkt = KeyFobPacket(key_fb_packet[:-1], key_fb_packet[-1], cur_time)

        if len(self.key_fobs_list) == 0:
            self.key_fobs_list = [[tmp_keyfob_pkt]]
        else:
            if self.key_fobs_list[-1][-1].name != tmp_keyfob_pkt.name:
                print("key fob packet is not the same type as previous. dropping key fob packet")

            elif (cur_time - self.key_fobs_list[-1][-1].pk_recv_time) < 1000000000:
                self.key_fobs_list[-1].append(tmp_keyfob_pkt)

            else:
                self.key_fobs_list.append([tmp_keyfob_pkt])
