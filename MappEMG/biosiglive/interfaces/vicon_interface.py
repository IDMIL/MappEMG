"""
This file is part of biosiglive. It contains a wrapper for the Vicon SDK for Python.
"""

import numpy as np
from .param import *
from typing import Union

try:
    from vicon_dssdk import ViconDataStream as VDS
except ModuleNotFoundError:
    pass


class ViconClient:
    """
    Class for interfacing with the Vicon system.
    """
    def __init__(self, ip: str = "127.0.0.1", port: int = 801, init_now=True):
        """
        Initialize the ViconClient class.
        Parameters
        ----------
        ip: str
            IP address of the Vicon system.
        port: int
            Port of the Vicon system.
        """
        self.address = f"{ip}:{port}"

        self.vicon_client = None
        self.acquisition_rate = None

        if init_now:
            self.init_client()

        self.devices = []
        self.imu = []
        self.markers = []
        self.is_frame = False

    def init_client(self):
        print(f"Connection to ViconDataStreamSDK at : {self.address} ...")
        self.vicon_client = VDS.Client()
        self.vicon_client.Connect(self.address)
        print("Connected to Vicon.")

        # Enable some different data types
        self.vicon_client.EnableSegmentData()
        self.vicon_client.EnableDeviceData()
        self.vicon_client.EnableMarkerData()
        self.vicon_client.EnableUnlabeledMarkerData()
        self.get_frame()

    def add_device(self, name: str, type: str = "emg", rate: float = 2000, system_rate: float = 100):
        """
        Add a device to the Vicon system.
        Parameters
        ----------
        name: str
            Name of the device.
        type: str
            Type of the device.
        rate: float
            Rate of the device.
        system_rate : float
            Rate of the system interface.
        """
        device_tmp = Device(name, type, rate, system_rate)
        if self.vicon_client:
            device_tmp.info = self.vicon_client.GetDeviceOutputDetails(name)
            if system_rate != self.vicon_client.GetFrameRate:
                raise RuntimeError(f"Frequency in Nexus ({self.vicon_client.GetFrameRate}) does not "
                                   f"match the device system rate ({system_rate})")
        else:
            device_tmp.info = None

        self.devices.append(device_tmp)

    def get_device_data(self, device_name: Union[str, list] = "all", channel_names: str = None, *args):
        """
        Get the device data from Vicon.
        Parameters
        ----------
        device_name: str or list
            Name of the device or list of devices names.
        channel_names: str
            Name of the channel.

        Returns
        -------
        device_data: list
            All asked device data.
        """
        devices = []
        all_device_data = []
        if not isinstance(device_name, list):
            device_name = [device_name]

        if device_name != "all":
            for d, device in enumerate(self.devices):
                if device.name == device_name[d]:
                    devices.append(device)
        else:
            devices = self.devices

        for device in devices:
            if not device.infos:
                device.infos = self.vicon_client.GetDeviceOutputDetails(device.name)

            if channel_names:
                device_data = np.zeros((len(channel_names), device.sample))
            else:
                device_data = np.zeros((len(device.infos), device.sample))

            count = 0
            device_chanel_names = []
            for output_name, chanel_name, unit in device.infos:
                data_tmp, _ = self.vicon_client.GetDeviceOutputValues(
                    device.name, output_name, chanel_name
                )
                if channel_names:
                    if chanel_name in channel_names:
                        device_data[count, :] = data_tmp
                        device_chanel_names.append(chanel_name)
                else:
                    device_data[count, :] = data_tmp
                    device_chanel_names.append(chanel_name)
                device.chanel_names = device_chanel_names
                count += 1
            all_device_data.append(device_data)
        return all_device_data

    def get_latency(self):
        return self.vicon_client.GetLatencyTotal()

    def get_frame(self):
        self.is_frame = self.vicon_client.GetFrame()
        while self.is_frame is not True:
            self.is_frame = self.vicon_client.GetFrame()

