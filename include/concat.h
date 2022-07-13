//
// Created by lakhan on 7/12/22.
//

#ifndef RTL433_CONCAT_H
#define RTL433_CONCAT_H

#include "stdio.h"
#include "bitbuffer.h"

void concat_bits(uint8_t *bitrow, unsigned bitlen, int *st, char *str);

void concat_gap(int gap, int *st, char *str);

void concat_name(char *name, int len, int st, char *str);

#endif //RTL433_CONCAT_H
