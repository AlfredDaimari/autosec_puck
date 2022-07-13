//
// Created by Alfred Daimari on 7/12/22.
//

#include "decoder.h"
#include "find_car.h"
#include "toyota_innova.h"
#include "maruti_nippon.h"

int (*check_for_car[2])(bitbuffer_t *bitbuffer) = {&check_for_toyota, &check_for_maruti_nippon};

void
(*create_car_bit_pk[2])(bitbuffer_t *bitbuffer, char *str) = {&create_toyota_bit_pk, &create_maruti_nippon_bit_pk};

int find_car(bitbuffer_t *bitbuffer)
{
        int len = sizeof(check_for_car) / sizeof(check_for_car[1]);
        int fn_to_call = -1;
        for (int i = 0; i < len; i++) {
                int fn_ret = (*check_for_car[i])(bitbuffer);
                if (fn_ret == 1) {
                        fn_to_call = i;
                        break;
                }
        }
        return fn_to_call;
}
