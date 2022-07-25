//
// Created by lakhan on 1/7/22.
//

#include "puck_bits_sender.h"
#include "bitbuffer.h"
#include <stdlib.h>
#include <stdio.h>
#include <stdbool.h>
#include <ctype.h>
#include <dbus/dbus.h>
#include <find_car.h>

const char INTERFACE_NAME[] = "org.autosec.PuckReceiverInterface";
const char BUS_NAME[] = "org.autosec.PuckReceiver";
const char OBJECT_PATH_NAME[] = "/org/autosec/PuckReceiver";
const char METHOD_NAME[] = "ReceiveBits";
const char BITS_SENDER_BUS_NAME[] = "org.autosec.PuckBitsSender";
int DBUS_RET;
DBusConnection *DBUS_CONN;
DBusError err;

// not needed
static void concat_bits(uint8_t const *bitrow, unsigned bit_len, int gap)
{
        /// data format fo#include "bitbuffer.h"38 * 8];
        char str[50 * 238 * 8];
        // appending the bits from bit buffer to array
        for (unsigned bit = 0; bit < bit_len; bit++) {
                if (bitrow[bit / 8] & (0x80 >> (bit % 8))) {
                        str[bit] = '1';
                } else {
                        str[bit] = '0';
                }

        }

        char gap_to_string[50];
        sprintf(gap_to_string, "%d", gap);  // converts int to string

        str[bit_len + 1] = ':';

        //appending the gap to the str
        for (unsigned j = 0; j < sizeof(gap_to_string) / sizeof(gap_to_string[0]); j++) {
                str[bit_len + 2 + j] = gap_to_string[j];
        }
        /// printing the string
        int rt;
        rt = send_bits_to_receiver(str);
        if (rt == -1) {
                fprintf(stderr, "error: could send message to receiver");
        }
}

int send_message_through_dbus(char *const msg)
{
        DBusMessage *dmsg;
        DBusMessageIter args;

        dmsg = dbus_message_new_method_call(BUS_NAME, OBJECT_PATH_NAME, INTERFACE_NAME, METHOD_NAME);
        if (NULL == dmsg) {
                fprintf(stderr, "message null, could not get method call\n");
                return -1;
        } else {
                fprintf(stderr, "dbus message call successful \n");
        }
        // append arguments
        dbus_message_iter_init_append(dmsg, &args);
        if (!dbus_message_iter_append_basic(&args, DBUS_TYPE_STRING, &msg)) {
                fprintf(stderr, "out of memory, could not append messages to args\n");
                return -1;
        } else {
                fprintf(stderr, "dbus message appended to iteration \n");
        }

        // send message and get a handle for a reply
        dbus_connection_send(DBUS_CONN, dmsg, NULL);
        dbus_connection_flush(DBUS_CONN);

        // free message
        dbus_message_unref(dmsg);
        return 0;
}

int send_bits_to_receiver(char *const msg)
{
        int rt = send_message_through_dbus(msg);
        return rt;
}

int init_dbus_connection()
{

        dbus_error_init(&err);
        DBUS_CONN = dbus_bus_get(DBUS_BUS_SYSTEM, &err);
        if (dbus_error_is_set(&err)) {
                fprintf(stderr, "connection error (%s)\n", err.message);
                dbus_error_free(&err);
                return -1;
        } else {
                printf("attached to system bus \n");
        }

        if (DBUS_CONN == NULL) {
                fprintf(stderr, "DBUS_CONN error\n");
                return -1;
        } else {
                printf("received conn is not null \n");
        }

        DBUS_RET = dbus_bus_request_name(DBUS_CONN, BITS_SENDER_BUS_NAME, DBUS_NAME_FLAG_REPLACE_EXISTING, &err);
        if (dbus_error_is_set(&err)) {
                fprintf(stderr, "Name Error (%s)\n", err.message);
                dbus_error_free(&err);
        } else {
                printf("received client bus name\n");
        }

        if (DBUS_REQUEST_NAME_REPLY_PRIMARY_OWNER != DBUS_RET) {
                fprintf(stderr, "DBUS_CONN request name error\n");
                return -1;
        } else {
                printf("process is the primary owner of bus request name\n");
        }
        return 0;
}

void send_puck_bits(bitbuffer_t *bitbuffer)
{
        char str[50 * 238 * 8];
        (void) memset(str, 0, sizeof(str));
        /*
         * will need to improve this, make it more readable
        */

        int fn_index = find_car(bitbuffer);
        (void) fprintf(stderr, "The fn index is %d \n", fn_index);
        if (fn_index != -1) {
                (*create_car_bit_pk[fn_index])(bitbuffer, str);
                (void) send_bits_to_receiver(str);

                if (bitbuffer->num_rows >= BITBUF_ROWS) {
                        fprintf(stderr, "... Maximum number of rows reached. Message is likely truncated.\n");
                }
        }
}
