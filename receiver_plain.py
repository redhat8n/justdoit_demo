#!/usr/bin/env python3
# coding: utf8

"""
Receiver
Client for receiving messages
"""

import time
import zmq
import gpgio
import config

DEBUG = False

class ListenClient(object):
    def __init__(self):
        self.context = zmq.Context()
        self.sock = self.context.socket(zmq.REQ)
        dest = "tcp://{}:{}".format(config.SERVER_HOSTNAME, config.SERVER_PORT)
        self.sock.connect(dest)

    def fetch_message(self, index):
        packet = "fetchmessage\n{}".format(index)
        if DEBUG: print("Fetching message {}... ".format(index))
        self.sock.send_string(packet)  # Use send_string to send a string
        response = self.sock.recv()
        if response == b"NOMESSAGE":  # Compare with bytes literal
            if DEBUG: print("no message yet")
            return None
        else:
            if DEBUG: print("message received")
            return response

    def fetch_messages_since(self, last_index):
        new_messages = []
        msg = self.fetch_message(last_index + 1)
        while msg is not None:
            last_index += 1
            new_messages.append((last_index, msg))
            msg = self.fetch_message(last_index + 1)
        return new_messages


c = ListenClient()
last_message_index = -1

while True:
    time.sleep(1)
    new_messages = c.fetch_messages_since(last_message_index)
    for (index, message) in new_messages:
        try:
            print(message.decode('utf-8'))  # Decode message bytes
        except gpgio.DecryptionError:
            print("ERROR: Failed to decrypt message.")
        print("\n------------------------------\n\n")
        last_message_index = index

