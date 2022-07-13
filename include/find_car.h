//
// Created by lakhan on 7/12/22.
//

#ifndef RTL433_FIND_CAR_H
#define RTL433_FIND_CAR_H

#include "decoder.h"

extern int (*check_for_car[2])(bitbuffer_t *bitbuffer);

extern void (*create_car_bit_pk[2])(bitbuffer_t *bitbuffer, char *str);

int find_car(bitbuffer_t *bitbuffer);

#endif //RTL433_FIND_CAR_H
