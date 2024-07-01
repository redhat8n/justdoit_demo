#!/usr/bin/env python3
# coding: utf8

"""
Sender
Client for sending messages
"""

import zmq
import gnupg
import config
import argparse

class TalkClient(object):
    def __init__(self):
        self.context = zmq.Context()
        self.sock = self.context.socket(zmq.REQ)
        dest = "tcp://{}:{}".format(config.SERVER_HOSTNAME, config.SERVER_PORT)
        self.sock.connect(dest)
        print("Connected to server at {}".format(dest))

    def send_message(self, msg):
        packet = "send\n{}".format(msg)
        print("Sending message... ")
        self.sock.send_string(packet)  # Use send_string to send a string
        response = self.sock.recv().decode('utf-8')  # Decode response to string
        if response != "OK":
            raise RuntimeError("Message send failed.")
        print("Message received")

def main():
    parser = argparse.ArgumentParser(description='Send an encrypted message to the server.')
    parser.add_argument('message', type=str, help='The message to send')
    args = parser.parse_args()

    client = TalkClient()
    try:
        client.send_message(args.message)  # Convert encrypted_data to string
    except Exception as e:
        print("An error occurred: {}".format(e))

if __name__ == "__main__":
    main()

