#!/usr/bin/python3.8

import threading
from rolling_keyfobs import RollingKeyFobs
from puck_bits_receiver import PuckBitsReceiverThread
from puck_bits_sender import PuckBitsYdSenderThread

if __name__ == "__main__":
    rolling_key_fobs = RollingKeyFobs()
    lock = threading.RLock()
    thread1 = PuckBitsReceiverThread("thread1", lock, rolling_key_fobs)
    thread2 = PuckBitsYdSenderThread("thread2", lock, rolling_key_fobs)

    thread1.start()
    thread2.start()

    # wait for both to end
    thread1.join()
    thread2.join()
