import re
import zmq

SERVER_PORT = 8387

class Server(object):
    def __init__(self):
        self.context = zmq.Context()
        self.sock = self.context.socket(zmq.REP)
        self.sock.bind('tcp://*:{}'.format(SERVER_PORT))
        print("Server listening on port {}".format(SERVER_PORT))

        self.messages = []

    def listen(self):
        while True:
            msg = self.sock.recv()
            msg_str = msg.decode('utf-8')  # Decode bytes to string
            mtype = re.match("(.*)\n", msg_str).groups()[0]
            if mtype == "send":
                self._receive_message(msg_str[len("send\n"):])
                self.sock.send(b"OK")  # Send response as bytes
            elif mtype == "fetchmessage":
                index = re.match(".*\n(.*)", msg_str).groups()[0]
                index = int(index)
                self.sock.send(self._fetch_message(index).encode('utf-8'))  # Send response as bytes
            else:
                print("Unrecognized message type: {}".format(mtype))

    def _receive_message(self, msg):
        print("Message received.")
        print('\n'.join(["> " + line for line in msg.split('\n')]))
        self.messages.append(msg)

    def _fetch_message(self, index):
        print("Client asked for message {}".format(index))
        if index < len(self.messages):
            print("  responding with message.")
            return self.messages[index]
        else:
            print("  responding NOMESSAGE.")
            return "NOMESSAGE"

s = Server()
s.listen()
