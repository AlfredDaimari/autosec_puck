//
// Created by lakhan on 7/12/22.
//

#ifndef RTL433_MARUTI_NIPPON_H
#define RTL433_MARUTI_NIPPON_H

#include "decoder.h"

int check_for_maruti_nippon(bitbuffer_t *bitbuffer);

void create_maruti_nippon_bit_pk(bitbuffer_t *bitbuffer, char *str);

#endif //RTL433_MARUTI_NIPPON_H
