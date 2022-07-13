//
// Created by Alfred Daimari on 7/12/22.
//

#include "decoder.h"
#include "toyota_innova.h"

int check_for_toyota(bitbuffer_t *bitbuffer)
{
        if (bitbuffer->bits_per_row[0] < 230) {
                return 0;
        }

        return 1;
}

void create_toyota_bit_pk(bitbuffer_t *bitbuffer, char *str)
{

}
