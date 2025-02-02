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

    gpg = gnupg.GPG()
    passphrase = config.PASSPHRASE  # Ensure you have this configured in your config

    encrypted_data = gpg.encrypt(
        args.message,
        recipients=config.RECIPIENTS,
        sign=config.SIGNER_FINGERPRINT,
        passphrase=passphrase,
        always_trust=True
    )

    if not encrypted_data.ok:
        print("An error occurred during encryption: {}".format(encrypted_data.stderr))
        return

    client = TalkClient()
    try:
        client.send_message(str(encrypted_data))  # Convert encrypted_data to string
    except Exception as e:
        print("An error occurred: {}".format(e))

if __name__ == "__main__":
    main()

