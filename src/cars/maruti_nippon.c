//
// Created by Alfred Daimari on 7/12/22.
//

#include "maruti_nippon.h"
#include "decoder.h"
#include "concat.h"

int check_for_maruti_nippon(bitbuffer_t *bitbuffer)
{
        //(void) fprintf(stderr, "%d - %d", bitbuffer->bits_per_row[0], bitbuffer->bits_per_row[1]);
        if (bitbuffer->bits_per_row[0] < 27 && bitbuffer->bits_per_row[0] > 18 && bitbuffer->bits_per_row[1] < 208 &&
            bitbuffer->bits_per_row[1] > 196) {
                return 1;
        }

        return 0;
}
// TODO: make a concatenating gap function

void create_maruti_nippon_bit_pk(bitbuffer_t *bitbuffer, char *str)
{
        int st = 0;
        for (int row = 0; row < bitbuffer->num_rows; row++) {
                concat_bits(bitbuffer->bb[row], bitbuffer->bits_per_row[row], &st, str);
                str[st] = ':';
                st += 1;

                concat_gap(bitbuffer->gaps_per_row[row], &st, str);
                str[st] = '-';
                st += 1;

        }

        char maruti[18] = {"maruti_nippon"};
        concat_name(maruti, 14, st, str);
}
