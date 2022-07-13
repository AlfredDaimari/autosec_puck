#
#    Creates a sender thread, checks if there is a valid key_fob to send every 0.5 seconds
#
#    Copyright (C) 2022 Alfred Daimari
#
#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 2 of the License, or
#    (at your option) any later version.
#

import threading
from rolling_keyfobs import RollingKeyFobs
from time import sleep


class PuckBitsYdSenderThread(threading.Thread):
    """
    Yardstick sender thread \n
    checks every 0.35s if there is a valid key fob to send
    """

    def __init__(self, name: str, lock: threading.RLock, rolling_key_fobs: RollingKeyFobs) -> None:
        """
        :param name: name of thread
        """
        if not isinstance(rolling_key_fobs, RollingKeyFobs):
            raise TypeError("rolling_key_fob is not an instance of RollingKeyFobs")

        t_type = type(threading.RLock())
        if not isinstance(lock, t_type):
            raise TypeError("lock is not an instance of threading.RLock")

        threading.Thread.__init__(self)
        self.name = name
        self.lock = lock
        self.rolling_key_fobs = rolling_key_fobs
        self.shutdown = threading.Event()

    def run(self) -> None:
        while not self.shutdown.is_set():
            self.lock.acquire()
            if self.rolling_key_fobs.dispatchable:
                self.rolling_key_fobs.dequeue_send()
            self.lock.release()
            sleep(0.35)

    def shutdown_thread(self):
        """
        terminate the thread
        """
        self.shutdown.set()
