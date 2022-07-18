//
// Created by Kahaan on 7/18/22.
//

#include "kia_carrence.h"
#include "decoder.h"
#include "concat.h"

int check_for_kia_carrence(bitbuffer_t *bitbuffer)
{
    //(void) fprintf(stderr, "%d - %d", bitbuffer->bits_per_row[0], bitbuffer->bits_per_row[1]);
    if (bitbuffer->bits_per_row[0] < 372 && bitbuffer->bits_per_row[0] > 360 &&) {
        return 1;
    }

    return 0;
}
// TODO: make a concatenating gap function

void create_kia_carrence_bit_pk(bitbuffer_t *bitbuffer, char *str)
{
    int st = 0;
    for (int row = 0; row < bitbuffer->num_rows; row++) {
        concat_bits(bitbuffer->bb[row], bitbuffer->bits_per_row[row], &st, str);
        str[st] = ':';
        st += 1;

        //concat_gap(bitbuffer->gaps_per_row[row], &st, str);
        //str[st] = '-';
        //st += 1;

    }

    char kia[12] = {"kia_carrence"};
    concat_name(kia, 14, st, str);
}