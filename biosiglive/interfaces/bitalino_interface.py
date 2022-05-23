from .param import *
try:
    import bitalino
except ModuleNotFoundError:
    pass


class BitalinoClient:
    def __init__(self, ip: str = None):
        # The macAddress variable on Windows can be "XX:XX:XX:XX:XX:XX" or "COMX"
        # while on Mac OS can be "/dev/tty.BITalino-XX-XX-DevB"
        self.address = "127.0.0.1" if not ip else ip
        self.devices = []
        # self.imu = []
        self.client = None

    def add_device(self, name: str = None, rate: int = 1000, system_rate: int = 100, acq_channels: list = [1,2,3,4,5,6]):

    # def __init__(self, name: str = None, type: str = "emg", rate: float = 2000, system_rate: float = 100, channel_names: list = None):
    
        """
        Add a device to the Bitalino client.
        Parameters
        ----------
        name : str
            Name of the device.
        rate : float
            Rate of the device.
        n_samples : int
            number of samples taken when pulling data.
        """
        # bitalino devices do not need a type, at least for now
        new_device = Device(name, ratre=rate, system_rate=system_rate, acq_channels=acq_channels)
        self.devices.append(new_device)
        
        self.client = bitalino.BITalino(self.address)
        self.client.start(rate, acq_channels)

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
                device_data = self.client.read(device.system_rate)
            except:
                raise RuntimeError(f"Error in getting data from bitalino device.")            
            all_device_data.append(device_data)
        
        return all_device_data

    def get_markers_data(self, marker_names: list = None, subject_name: str = None):
        raise RuntimeError("It's not possible to get markers data from bitalino.")

    def get_force_plate_data(self):
        raise RuntimeError("It's not possible to get force plate data from bitalino.")

    @staticmethod
    def init_client():
        pass

    @staticmethod
    def get_latency():
        return 0

    @staticmethod
    def get_frame():
        return True

