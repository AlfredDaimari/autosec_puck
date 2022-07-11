from rf import *
from keyfob import *


class RollingKeyFobs:
    """"
    data structure to hold the rolling key fobs,
    sends out one key fob when 2 valid key fobs are stored
    """

    def __init__(self, dev: object) -> None:
        """
        :param dev: rf device (instance of RfSender)
        """
        self.key_fobs_list = []
        if not isinstance(dev, RfSender):
            raise TypeError("dev is not an instance of RfSender")
        self.dev = dev

    def __len__(self):
        return len(self.key_fobs_list)

    @property
    def dispatchable(self) -> bool:
        """
        checks if there are two valid key fobs \n
        and if the previous one can be sent or not
        """
        if len(self) > 1:
            if self.key_fobs_list[0].complete and self.key_fobs_list[1].complete:
                return True
            else:
                self.__shift()
                return self.dispatchable
        else:
            return False

    def __shift(self):
        """
        remove the first element from key fob
        """
        return self.key_fobs_list.pop(0)

    def __send(self, msg: object) -> None:
        """
        send a message using the yardstick
        :param msg: instance of key fob packet
        """
        rf_message = RfMessage(msg, MOD_2FSK | MANCHESTER, 4000, 230, self.dev)
        rf_message.send()

    def push(self, bit_string: str, gap_to_prev_bitpk: int) -> None:
        """
        add a new key fob to list or concatenate with previous key fob \n
        :param bit_string: a string of bits
        :param gap_to_prev_bitpk: gap to the previous received string of bits
        """
        tmp_keyfob_pkt = KeyFobPacket(bit_string, gap_to_prev_bitpk)
        apnd_bool = False

        if len(self.key_fobs_list) > 0:
            lst_key_fob = self.key_fobs_list[-1]
            apnd_bool = lst_key_fob.concatenate(tmp_keyfob_pkt)

        if not apnd_bool:
            self.key_fobs_list.append(tmp_keyfob_pkt)

        if self.dispatchable:
            keyfob_tb_snt = self.__shift()
            self.__send(keyfob_tb_snt)
            del keyfob_tb_snt
