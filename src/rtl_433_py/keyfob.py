#
#    classes for storing bit information
#
#    Copyright (C) 2022 Alfred Daimari
#
#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 2 of the License, or
#    (at your option) any later version.
#

from rflib import *
from typing import List
from termcolor import colored, cprint


# TODO: make code more readable

class BitPack:
    """
    data structure to hold a row of bits \n
    --- \n

    attributes: \n
    bit_pk - a packet of bits \n
    gap_to_prev_bitpk - gap to the previous bit packet sent \n
    --- \n

    methods: \n
    convert_to_hex() \n
    convert_to_binary() \n
    convert_to_binary() \n
    """

    def __init__(self, bit_string: any, gap_to_prev_bitpk: int) -> None:
        """
        Init BitPacket \n
        :param bit_string: a string of bits, duh!
        :param gap_to_prev_bitpk: gap to previous row in bitbuffer, generated by rtl_433
        """
        self.time_to_prev_bitpk = gap_to_prev_bitpk / 250000  # might not need this, remove ?
        self.bit_pk = bit_string
        self.__num_type = 2  # numeral system used to represent the bit_pk

    def __str__(self):
        return self.bit_pk

    def __len__(self) -> int:
        return len(self.bit_pk)

    def bitpk_drop(self, pos: int) -> None:
        """
        drops all bits from pos \n
        :param pos: dropping index
        """
        self.bit_pk = self.bit_pk[:pos]

    def bitpk_pad(self, num0: int) -> None:
        """
        :param num0: number of 0s to pad
        :return: None
        """
        self.bit_pk += ("0" * num0)

    def convert_to_hex(self) -> None:
        """
        Converts binary to hex
        """
        if self.__num_type == 2:
            int_rep = int(self.bit_pk, 2)
            hex_rep = hex(int_rep)
            self.bit_pk = hex_rep[2:]
            self.__num_type = 16

        if self.__num_type == 10:
            hex_rep = hex(self.bit_pk)
            self.bit_pk = hex_rep[2:]
            self.__num_type = 16

    def convert_to_binary(self) -> None:
        """
        Converts to binary
        """
        if self.__num_type == 16:
            int_rep = int(self.bit_pk, 16)
            bin_rep = bin(int_rep)[2:]
            self.bit_pk = bin_rep
            self.__num_type = 2

        if self.__num_type == 10:
            bin_rep = bin(self.bit_pk)[2:]
            self.bit_pk = bin_rep
            self.__num_type = 2

    def convert_to_decimal(self) -> None:
        """
        Converts to decimal
        """
        if self.__num_type == 16:
            int_rep = int(self.bit_pk, 16)
            self.bit_pk = int_rep
            self.__num_type = 10

        if self.__num_type == 2:
            int_rep = int(self.bit_pk, 2)
            self.bit_pk = int_rep
            self.__num_type = 10


class KeyFobPacket:
    """
    data structure to hold a key fob packet \n
    --- \n

    attributes: \n
    packets: instances of BitPackets \n
    pk_recv_time: the time received (unix time ns format)
    """

    def __init__(self, key_bits: List[str], car_name: str, pk_recv_time: int) -> None:
        self.name = car_name
        self.packets = [BitPack(b.split(':')[0], int(b.split(':')[1])) for b in key_bits]
        self.pk_recv_time = pk_recv_time

    def __len__(self):
        return len(self.packets)

    def __str__(self):
        str_ = "\n"
        for i in range(len(self.packets)):
            str_ += self.packets[i].__str__() + f"-----{i + 1} \n"
        return str_

    @classmethod
    def are_same(cls, key_fb1: object, key_fb2: object) -> bool:
        """
        pointless !!
        """
        if (not isinstance(key_fb1, KeyFobPacket)) or (not isinstance(key_fb2, KeyFobPacket)):
            raise TypeError('key_fb1 or key_fb2 are not instances of KeyFobPacket')

        return False

    def time_to_prev_bchunk(self, ind: int) -> float:
        """
        :param ind: the index of the packet in key fobs
        :return: returns the time to prev packet
        """
        return self.packets[ind].time_to_prev_bitpk

    def convert_to_hex(self) -> None:
        """
        Converts bits to hex representation
        """
        for pkt in self.packets:
            pkt.convert_to_hex()

    def convert_to_binary(self) -> None:
        """
        Converts bits to binary representation
        """
        for pkt in self.packets:
            pkt.convert_to_binary()

    def convert_to_decimal(self) -> None:
        """
        Converts bits to decimal representation
        """
        for pkt in self.packets:
            pkt.convert_to_decimal()

    def conc_pkts(self) -> str:
        pass

    def __clean(self):
        pass

    @classmethod
    def filter(cls, key_fb_packet: List[str]) -> List[List[str]]:
        pass


class InnovaKeyFobPacket(KeyFobPacket):
    """
    data structure to hold toyota innova crysta key fob
    """

    def __init__(self, key_bits: List[str], car_name: str, pk_recv_time: int) -> None:
        KeyFobPacket.__init__(self, key_bits, car_name, pk_recv_time)
        self.__clean()

    def __clean(self):
        """
        cleans up the bit_pk for toyota
        :return: None
        """
        if len(self.packets[0]) > 236:
            self.packets[0].bitpk_drop(237)
            self.packets[0].bitpk_pad(3)

    @classmethod
    def filter(cls, key_fb_packet: List[str]) -> List[List[str]]:
        """
        :param key_fb_packet: key fob packet, but without the name
        :return: list of filtered separate key fobs, can be turned into packets
        """
        key_fbs = []
        for kfb in key_fb_packet:
            if len(kfb.split(":")[0]) >= 236:
                key_fbs.append([kfb])
        return key_fbs

    def conc_pkts(self) -> str:
        """
        :return: string of concatenated packets
        """
        return self.packets[0].bit_pk + (
                    "0" * 4)  # rewrite -> try calling this function before convert to hex (4 * 4 = 16)


class MarutiNipponKeyFobPacket(KeyFobPacket):
    """
    data structure to hold maruti nippon key fob
    TODO: needs proper writing
    """

    def __init__(self, key_bits: List[str], car_name: str, pk_recv_time: int) -> None:
        KeyFobPacket.__init__(self, key_bits, car_name, pk_recv_time)
        self.__clean()

    def __clean(self):
        """
        cleans up the bit_pk for toyota
        :return: None
        """
        self.packets[0].bitpk_drop(23)
        self.packets[0].bitpk_pad(1)

        self.packets[1].bitpk_drop(197)
        self.packets[1].bitpk_pad(3)

    @classmethod
    def filter(cls, key_fb_packet: List[str]) -> List[List[str]]:
        return [key_fb_packet]

    def conc_pkts(self) -> str:
        """
        :return: a string of concatenated bits
        """
        str_ = self.packets[0].bit_pk
        str_ += "0" * 4
        str_ += self.packets[1].bit_pk
        return str_
