from .param import *
try:
    import bitalino
    import numpy as np
except ModuleNotFoundError:
    pass


class BitalinoClient:
    def __init__(self, ip: str = None):
        # The macAddress variable on Windows can be "XX:XX:XX:XX:XX:XX" or "COMX"
        # while on Mac OS can be "/dev/tty.BITalino-XX-XX-DevB"
        self.address = "/dev/tty.BITalino-XX-XX-DevB" if not ip else ip
        self.devices = []
        self.client = None
        self.rate = 1000
        self.system_rate = 10
        self.acq_channels = [0,1,2,3,4,5]


    def add_device(self, name: str = None, rate: int = 1000, system_rate: int = 50, acq_channels: list = [0,1,2,3,4,5]):

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

        # bitalino devices do not need a type, at least for now
        new_device = Device(name, rate=rate, system_rate=system_rate, acq_channels=acq_channels)
        self.devices.append(new_device)
        
        self.client = bitalino.BITalino(self.address)

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

    def get_device_data(self, device_name: str = "all", *args):
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

        for device in devices:
            try:
                device_data = np.array(self.client.read(nSamples=device.system_rate), dtype=float)
                device_data = np.delete(device_data, [0, 1, 2, 3, 4], 1)
                device_data = device_data.T

            except:
                raise RuntimeError("Error in getting data from bitalino device.")

            all_device_data.append(device_data)
        
        return all_device_data
