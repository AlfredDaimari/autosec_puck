//
// Created by lakhan on 7/12/22.
//

#include "concat.h"
#include "bitbuffer.h"
#include <string.h>

void concat_bits(uint8_t *bitrow, unsigned bitlen, int *st, char *str)
{
        int ibitlen = (int) bitlen;
        int bit;
        int st_np = *st;
        for (bit = 0; bit < ibitlen; bit++) {
                if (bitrow[bit / 8] & (0x80 >> (bit % 8))) {
                        str[bit + st_np] = '1';
                } else {
                        str[bit + st_np] = '0';
                }
        }
        *st = *st + bitlen;
}

void concat_gap(int gap, int *st, char *str)
{
        int st_np = *st;
        char gap_to_string[50];
        (void) memset(gap_to_string, 0, sizeof(gap_to_string));
        (void) sprintf(gap_to_string, "%d", gap);
        int jlen = sizeof(gap_to_string) / sizeof(gap_to_string[0]);
        int j;

        for (j = 0; j < jlen; j++) {
                if (gap_to_string[j] == '\0') {
                        break;
                }
                str[st_np + j] = gap_to_string[j];
        }
        *st = *st + j;
}

void concat_name(char *name, int len, int st, char *str)
{
        int i = 0;
        for (i = 0; i < len; i++) {
                str[st + i] = name[i];
        }
}
