"""
This is part of the biosiglive project. It contains the connection class.
"""
import socket
import json
import numpy as np
import struct
from typing import Union
try:
    from pythonosc.udp_client import SimpleUDPClient
except ModuleNotFoundError:
    pass


class Connection:
    """
    This class is used to connect to the biosiglive server.
    """
    def __init__(self, ip: str = "127.0.0.1", ports: Union[int, list] = 50000):
        """
        Initialize the connection.

        Parameters
        ----------
        ip : str
            The ip address of the server.
        ports : int or list
            The port(s) of the server.
        """
        self.ip = ip
        self.ports = [ports] if not isinstance(ports, list) else ports
        self.message_queues = None
        self.buff_size = 32767

    def _prepare_data(self, message: dict, data: dict):
        """
        Prepare the data to send.

        Parameters
        ----------
        message : dict
            The message received from the client.
        data : dict
            The data to prepared.

        Returns
        -------
        prepared data : dict
            The data prepared to be sent.

        """
        
        nb_frames_to_get = message["nb_frames_to_get"] if message["nb_frames_to_get"] else 1

        data_to_prepare = self.__data_to_prepare(data)
        prepared_data = self.__check_and_adjust_dims(data_to_prepare, nb_frames_to_get)

        return prepared_data

    @staticmethod
    def __data_to_prepare(data: dict):
        """
        Prepare the device data to send.

        Parameters
        ----------
        message : dict
            The message received from the client.
        data : dict
            The data to prepared.

        Returns
        -------
        prepared data : dict
            The data prepared to be sent.
        """

        data_to_prepare = {}

        try:
            data_to_prepare["emg_proc"] = data["emg_proc"]
            data_to_prepare["emg_raw_all"] = data["emg_raw_all"]
            data_to_prepare["sampling_rate"] = data["sampling_rate"] 
            data_to_prepare["system_rate"] = data["system_rate"]
            data_to_prepare["n_electrode"] = data["n_electrode"]
        except:
            raise RuntimeError(f"Wrong message format.")

        return data_to_prepare

    @staticmethod
    def __check_and_adjust_dims(data: dict, nb_frames_to_get: int = 1):
        """
        Check and adjust the dimensions of the data to send.

        Parameters
        ----------
        data : dict
            The data to check and adjust.
        nb_frames_to_get : int
            The number of frames to get (default is 1).

        Returns
        -------
        data : dict
            The data checked and adjusted.
        """
    
        for key in data.keys():
            if isinstance(data[key], int):
                data[key] = [data[key]]
            elif key == "emg_proc":
                data[key] = data[key][:, :nb_frames_to_get].tolist()
            elif key == "emg_raw_all":
                data[key] = data[key].tolist()

        return data


class Server(Connection):
    """
    Class to create a server.
    """
    def __init__(self, ip: str = "127.0.0.1", port: int = 50000, type: str = "TCP"):
        """
        Parameters
        ----------
        ip : str
            The ip of the server.
        ports : list
                The ports of the server.
        type : str
            The type of the server.
        """
        self.ip = ip
        self.port = port
        self.type = type
        self.server = None
        self.inputs = None
        self.outputs = None
        self.buff_size = 100000
        super().__init__(ip=ip, ports=port)

    def start(self):
        """
        Start the server.
        """
        # for i, port in enumerate(self.ports):
        if self.type == "TCP":
            self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        elif self.type == "UDP":
            raise RuntimeError(f"UDP server not implemented yet.")
            # self.servers.append(socket.socket(socket.AF_INET, socket.SOCK_DGRAM))
        else:
            raise RuntimeError(f"Invalid type of connexion ({type}). Type must be 'TCP' or 'UDP'.")
        try:
            self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server.settimeout(0.1) # NEW LINE BY KARL
            self.server.bind((self.ip, self.port))
            if self.type != "UDP":
                self.server.listen(10)
                self.inputs = [self.server]
                self.outputs = []
                self.message_queues = {}
        except ConnectionError:
            raise RuntimeError("Unknown error. Server is not listening.")

    def client_listening(self):
        """
        Listen to the client.
        Parameters
        ----------
        data : dict
            Data to send to the client function of message
        """
        connection, ad = self.server.accept()
        return connection

    def receive_message(self, connection):
        return json.loads(connection.recv(self.buff_size))

    def send_data(self, data, connection, message):
        """
        Send the data to the client.
        Parameters
        ----------
        data : dict
            The data to send.
        connection : socket.socket
            The connection to send the data to.
        """
        
        data_to_send = self._prepare_data(message, data)
        encoded_data = json.dumps(data_to_send).encode()
        encoded_data = struct.pack('>I', len(encoded_data)) + encoded_data
        try:
            connection.sendall(encoded_data)
            print(f"data sent: {data_to_send}")
        except ConnectionError:
            pass


class OscClient(Connection):
    """
    Class to create an OSC client.
    """
    def __init__(self, ip: str = "127.0.0.1"):
        self.ports = [51337]
        self.osc = []
        super().__init__(ip=ip, ports=self.ports)

    def start(self):
        """
        Start the client.
        """
        for i in range(len(self.ports)):
            try:
                self.osc.append(SimpleUDPClient(self.ip, self.ports[i]))
                print(f"Streaming OSC {i} activated on '{self.ip}:{self.ports[i]}")
            except ConnectionError:
                raise RuntimeError("Unknown error. OSC client not open.")

    @staticmethod
    def __adjust_dims(data: dict, device_to_send: dict):
        """
        Adjust the dimensions of the data to send.
        Parameters
        ----------
        data : dict
            The data to send.
        device_to_send : dict
            The device type to send the data to (emg or imu).
        Returns
        -------
        The data to send.
        """
        data_to_return = []
        for key in device_to_send:
            if key == "emg":
                emg_proc = np.array(data["emg_proc"])[:, -1:]
                emg_proc = emg_proc.reshape(emg_proc.shape[0])
                data_to_return.append(emg_proc.tolist())
            else:
                raise RuntimeError(f"Unknown device ({key}) to send. Possible devices are 'emg' and 'imu'.")

        return data_to_return

    def send_data(self, data: dict, device_to_send: dict):
        """
        Send the data to the client.
        Parameters
        ----------
        data : dict
            The data to send.
        device_to_send : dict
            The device type to send the data to (emg or imu).
        """

        data = self.__adjust_dims(data, device_to_send)
        for key in device_to_send:
            if key == "emg":
                self.osc[0].send_message("/emg", data[0])
            elif key == "imu":
                idx = 1 if key in "emg" in device_to_send else 0
                self.osc[0].send_message("/imu/", data[idx])
                self.osc[0].send_message("/accel/", data[idx + 1])
                self.osc[0].send_message("/gyro/", data[idx + 2])
            else:
                raise RuntimeError(f"Unknown device ({key}) to send. Possible devices are 'emg' and 'imu'.")