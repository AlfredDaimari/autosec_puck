//
// Created by Kahaan on 7/18/22.
//

#ifndef RTL433_KIA_CARRENCE_H
#define RTL433_KIA_CARRENCE_H

#include "decoder.h"

int check_for_kia_carrence(bitbuffer_t *bitbuffer);

void create_kia_carrence_bit_pk(bitbuffer_t *bitbuffer, char *str);

#endif //RTL433_KIA_CARRENCE_H