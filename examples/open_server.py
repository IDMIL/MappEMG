from biosiglive.streaming.connection import Server
from biosiglive.streaming.client import Message
import numpy as np


if __name__ == '__main__':
    message = Message()

    server = Server(ip="localhost", port=5000, type='TCP')
    server.start()
    print("\nStart Listening...")
    while True:
        data = {"emg": np.ndarray((2, 50)), "norm_emg": True}
        server.client_listening(data)