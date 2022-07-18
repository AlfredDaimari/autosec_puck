//
// Created by Alfred Daimari on 7/12/22.
//

#include "decoder.h"
#include "toyota_innova.h"
#include "concat.h"

int check_for_toyota(bitbuffer_t *bitbuffer)
{
        if (bitbuffer->bits_per_row[0] > 236 && bitbuffer->bits_per_row[0] < 242) {
                return 1;
        }

        return 0;
}

void create_toyota_bit_pk(bitbuffer_t *bitbuffer, char *str)
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

        char toyota[18] = {"toyota_innova"};
        concat_name(toyota, 14, st, str);
}
