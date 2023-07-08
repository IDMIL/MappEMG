import bitalino
from typing import Union
import numpy as np
from ..enums import DeviceType, InverseKinematicsMethods, InterfaceType, \
    RealTimeProcessingMethod, OfflineProcessingMethod
from .generic_interface import GenericInterface
from biosiglive.file_io.save_and_load import load



class BitalinoClient(GenericInterface):
    def __init__(self, ip: str = None, system_rate: float = 100, data_path: str = None):
        # The macAddress variable on Windows can be "XX:XX:XX:XX:XX:XX" or "COMX"
        # while on Mac OS can be "/dev/tty.BITalino-XX-XX-DevB"
        self.address = "/dev/tty.BITalino-XX-XX-DevB" if not ip else ip
        self.devices = []
        self.client = None
        self.rate = 1000
        self.system_rate = 10
        self.acq_channels = [0, 1, 2, 3, 4, 5]
        super().__init__(system_rate=system_rate, interface_type=InterfaceType.Custom)
        self.offline_data = None
        if data_path:
            self.offline_data = load(data_path)
        self.device_data_key = []
        self.marker_data_key = []
        self.c = 0
        self.d = 0

    def add_device(
            self,
            name: str = None,
            rate: int = 1000,
            system_rate: int = 50,
            nb_channels: int = 0,
            device_type: Union[DeviceType, str] = DeviceType.Emg,
            data_buffer_size: int = None,
            acq_channels: list = [0, 1, 2, 3, 4, 5],
            device_range: tuple = None,
            device_data_file_key: str = None,
            processing_method: Union[RealTimeProcessingMethod, OfflineProcessingMethod] = None,
            **process_kwargs,
    ):

        """
        Add a device to the Bitalino client.
        Parameters
        ----------1
        name : str
            Name of the device.
        rate : float
            Rate of the device.
        n_samples : int
            number of samples taken when pulling data.
        """

        self.rate = rate
        self.system_rate = system_rate
        self.acq_channels = acq_channels
        nb_channels = len(acq_channels)
        device_tmp = self._add_device(
            nb_channels, device_type, name, rate, device_range, processing_method, **process_kwargs
        )
        if data_buffer_size:
            device_tmp.data_window = data_buffer_size

        # bitalino devices do not need a type, at least for now
        # new_device = Device(name, rate=rate, system_rate=system_rate, acq_channels=acq_channels)
        self.devices.append(device_tmp)
        self.client = bitalino.BITalino(self.address)

        if self.offline_data is not None:
            if not device_data_file_key:
                raise ValueError("You need to specify the device data file key.")
        self.device_data_key.append(device_data_file_key)

    def remove_device(self):
        """
        Remove a device from the Bitalino client.
        Parameters
        ----------
        name : str
            Name of the device to be removed.
        """
        self.devices.pop()

    def close(self):
        self.client.close()

    def start_acquisition(self):
        self.client.start(self.rate, self.acq_channels)

    def stop_acquisition(self):
        self.client.stop()

    def get_device_data(self, device_name: Union[str, list] = "all", channel_names: str = None, **kwargs):
        """
        Get data from the device.
        Parameters
        ----------
        device_name : str
            Name of the device.
        *args
            Additional argument.

        Returns
        -------
        data : list
            Data from the device.
        """
        devices = []
        all_device_data = []

        if device_name and not isinstance(device_name, list):
            device_name = [device_name]

        if device_name != "all":
            for d, device in enumerate(self.devices):
                if device.name and device.name == device_name[d]:
                    devices.append(device)
        else:
            devices = self.devices

        for d, device in enumerate(devices):
            if self.offline_data:
                device.new_data = self.offline_data[self.device_data_key[d]][
                                  : device.nb_channels, self.c: self.c + device.sample
                                  ]
                if abs(self.c + device.sample - self.offline_data[self.device_data_key[d]].shape[1]) > device.sample:
                    self.c = self.c + device.sample
                else:
                    self.c = 0
            else:
                device.new_data = np.random.rand(device.nb_channels, device.sample)
            try:
                device.new_data = np.array(self.client.read(nSamples=device.sample), dtype=float)
                device.new_data = np.delete(device.new_data, [0, 1, 2, 3, 4], 1)
                device.new_data = device.new_data.T

                device.append_data(device.new_data)
                all_device_data.append(device.new_data)

            except:
                raise RuntimeError("Error in getting data from bitalino device.")

        return all_device_data