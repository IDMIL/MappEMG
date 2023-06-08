import socket
import numpy as np
import multiprocessing as mp
from biosiglive.interfaces.generic_interface import GenericInterface
from biosiglive.interfaces.pytrigno_interface import PytrignoClient
from biosiglive.interfaces.vicon_interface import ViconClient
from biosiglive.streaming.server import Server
from biosiglive.enums import RealTimeProcessingMethod
from biosiglive.streaming.stream_data import StreamData

from biosiglive.processing.utils import NumpyQueue
from biosiglive.interfaces.bitalino_interface import BitalinoClient
from biosiglive.processing.data_processing import OfflineProcessing
import matplotlib.pyplot as plt


class RunServer():

    def __init__(self, server_ip='localhost',
                 server_port=5005,
                 with_connection=False,
                 with_plot=False,
                 sensorkit=None,
                 bluetooth_address=None,
                 acq_channels=[],
                 device_sampling_rate=1000,
                 size_processing_window=100,
                 server_acquisition_rate=10
                 ):
        """
        Run the server.

        Parameters
        ----------
        sensorkit : string
            The name of the sensorkit interface being used: 'bitalino', 'vicon', 'pytrigno', or None.
        with_connection : bool
            Determine if the server acquired real data from a sensorkit (True) or not (False).
        with_plot : bool
            Determine if the server plots data in real-time (True) or not (False).
        bluetooth_address : string
            The macAddress variable to connect the Bitalino sensorkit.
            On Windows it can be "XX:XX:XX:XX:XX:XX" or "COMX"
            while on Mac OS can be "/dev/tty.BITalino-XX-XX-DevB")
        acq_channels : list
            List of integers containing the channels to which the sensorkits should pull data.
            For bitalino, it has to be a list of all sensors [0, ..., 6].
            For pytrigno/vicon, it is a range [0, 16].
        device_sampling_rate : int
            Frequency of the device acquiring data. Recommended frequency of 1000 Hz.
        size_processing_window : int
            Size of the processing window.
        server_acquisition_rate : int
            Number of samples acquired from device per pull.
        """

        self.server_ip = server_ip
        self.server_port = server_port
        self.sensorkit = sensorkit
        self.with_connection = with_connection
        self.with_plot = with_plot
        self.bluetooth_address = bluetooth_address
        self.acq_channels = acq_channels
        self.device_sampling_rate = device_sampling_rate
        self.size_processing_window = size_processing_window
        self.server_acquisition_rate = server_acquisition_rate
        self.n_electrode = len(acq_channels)

        manager = mp.Manager()
        self.__emg_queue_in = manager.Queue()
        self.__emg_queue_out = manager.Queue()
        self.__event_emg = mp.Event()
        self.__process = mp.Process

    def _plot_trial(self, raw_data, proc_data):
        """
        Plot the trial.

        Parameters
        ----------
        raw_data : numpy.ndarray
            The raw EMG data of the trial.
        """
        # processed_data = self.processing.process_emg(data=raw_data, frequency=self.frequency, ma=True)
        nb_column = 1
        plot_comm = "y"

        frequency = 1000
        acquisition_rate = 10
        effective_rate = frequency / acquisition_rate

        legend = ["Raw"]
        x = np.linspace(0, len(raw_data) / (effective_rate), len(raw_data))
        # x = np.linspace(0, len(proc_data) / (effective_rate), len(proc_data))
        print("Close the plot windows to continue.")
        plt.plot(x, raw_data)
        # plt.plot(x, proc_data)

        plt.show()

    def run_sensor_acquisition(self):

        print("Starting Sensor Acquisition...")

        if self.with_connection:

            if self.sensorkit == 'bitalino':
                try:
                    sensor_interface = BitalinoClient(ip=self.bluetooth_address)
                    sensor_interface.add_device(
                        "Bitalino", rate=self.device_sampling_rate, system_rate=self.server_acquisition_rate,
                        acq_channels=self.acq_channels, device_data_file_key="emg",
                        process_method = RealTimeProcessingMethod.ProcessEmg)
                except:
                    raise RuntimeError(
                        "Could not create Bitalino connection. Make sure you bluetooth is activated and you have the correct bitalino address.")
                try:
                    sensor_interface.start_acquisition()
                except:
                    raise RuntimeError("Could not start acquisition Bitalino connection.")

            if self.sensorkit == 'vicon':
                try:
                    sensor_interface = ViconClient()
                    sensor_interface.add_device("Vicon", rate=self.device_sampling_rate,
                                                system_rate=self.server_acquisition_rate)
                except:
                    raise RuntimeError("Could not create Vicon connection.")

            if self.sensorkit == 'pytrigno':
                try:
                    sensor_interface = PytrignoClient()
                    sensor_interface.add_device("Pytrigno", range=(0, self.n_electrode - 1),
                                                rate=self.device_sampling_rate)
                except:
                    raise RuntimeError("Could not create Pytrigno connection.")

        server = Server(ip=self.server_ip, port=self.server_port, server_type='TCP')
        server.start()
        connected = False
        print(self.server_ip, self.server_port)

        while True:

            if not self.with_connection:
                emg_tmp = np.random.randint(1024, size=(
                self.n_electrode, self.server_acquisition_rate))  # data range [0.0, 1024)
                emg_tmp = (emg_tmp / (2 ** 10) - 0.5) * 3.3 / 1009 * 1000
            else:
                if self.sensorkit == 'bitalino':
                    emg_tmp = sensor_interface.get_device_data(device_name="Bitalino")[0]
                    emg_tmp = (emg_tmp / (2 ** 10) - 0.5) * 3.3 / 1009 * 1000  # convert to mV


                if self.sensorkit == 'vicon':
                    sensor_interface.get_frame()
                    emg_tmp = sensor_interface.get_device_data(device_name="Vicon")[0]

                if self.sensorkit == 'pytrigno':
                    emg_tmp = sensor_interface.get_device_data(device_name="Pytrigno")[0]

                processing = OfflineProcessing(data_rate=self.device_sampling_rate, processing_window=self.size_processing_window)
                emg_proc = processing.process_emg(np.array(emg_tmp))
                # emg_proc_to_send = emg_proc
                emg_proc_to_send = np.reshape(np.average(emg_proc[:, -self.size_processing_window:], axis=1),
                                              (self.n_electrode, 1))

            # if not connected:
            try:
                connection, message = server.client_listening()
                # connected = True
            except socket.timeout:
                pass

            self.__event_emg.clear()
            data_to_send = {}
            data_to_send["emg_proc"] = emg_proc_to_send[0]
            data_to_send["emg_raw_all"] = emg_tmp
            data_to_send["other_paras"] = np.array([self.n_electrode, self.device_sampling_rate, self.server_acquisition_rate])
            data_to_send["close"] = [0]

            # if connected:
            try:
                server.send_data(data_to_send, connection, message)
            # elif message['command'] == ['close']:
            #     connection.close()
            # else:
            #     raise ValueError("Unkown message command.")

            except:

                connection.close()
                    # connected = False
                #     print("\nClosing connection... \nListening to new client...\n")


    def run(self):

        print("\nStarting Server...\n")

        processes = []
        processes.append(self.__process(name="acquire_emg", target=RunServer.run_sensor_acquisition, args=(self,)))
        # processes.append(self.__process(name="process_emg", target=RunServer.run_emg_processing, args=(self,)))
        # processes.append(self.__process(name="stream_emg", target=RunServer.run_streaming, args=(self,)))

        for p in processes:
            p.start()
        for p in processes:
            p.join()


if __name__ == '__main__':

    print("\nStarting Server Setup...")

    # Define server's ip and port
    server_ip = '127.0.0.1'
    server_port = 5005
    # Verify if user wants to change ip or port
    change_ip_or_port = None
    while change_ip_or_port != '':
        print("\nClient will connect to server on IP:'{}' and PORT:'{}'".format(server_ip, server_port))
        change_ip_or_port = input(
            "\tTo change IP -- Press 1 and 'Enter'\n\tTo change PORT -- Press 2 and 'Enter'\n\tTo continue -- Leave empty and press 'Enter': ")
        if change_ip_or_port == '1':
            server_ip = input("New IP address: ")
        elif change_ip_or_port == '2':
            try:
                server_port = int(input("New PORT: "))
            except:
                print("Invalid PORT")

    # Verify if user wants real device connected
    with_connection = None
    while with_connection not in ['y', 'n']:
        with_connection = input("\nWith device connected? (y, or n for random data): ")
    with_connection = True if with_connection == 'y' else False

    # Verify which real device they want
    what_device = None
    bluetooth_address = None
    if with_connection:
        while what_device not in ['bitalino', 'vicon', 'pytrigno']:
            what_device = input("\nWhat device? (bitalino, vicon, or pytrigno): ")

        # Read bitalino bluetooth address if there is a connection
        if what_device == 'bitalino':
            if with_connection:
                print(
                    "\nThe macAddress variable on Windows can be \"XX:XX:XX:XX:XX:XX\" or \"COMX\" \n while on Mac OS can be \"/dev/tty.BITalino-XX-XX-DevB\"")
                # TODO: remove shortcut from main application
                bluetooth_address = input(
                    "\nBitalino bluetooth address (leave empty if \"20:19:07:00:7E:19\"): ")
                if bluetooth_address == "":
                    bluetooth_address = "20:19:07:00:7E:19"

    # Set acquisition channels (number of sensors)
    acq_channels = None
    while acq_channels == None:
        acq_channels = input("\nEnter list of acquisition channels (e.g. for A1 A2 A3, write 1 2 3): ").split(" ")
        try:
            acq_channels = [int(c) - 1 for c in acq_channels]
            if not all(channel >= 0 and channel <= 6 for channel in acq_channels):
                print("\nInvalid acquisition channels (make sure they are separated by a space...)")
                acq_channels = None
        except:
            acq_channels = None

    # Check if user wants to plot data in real-time (might decrease performance)
    with_plot = None
    while with_plot not in ['y', 'n']:
        with_plot = input(
            "\nPlot data in real-time? (y or n): ")
    with_plot = True if with_plot == 'y' else False

    # Run server with information provided
    local_server = RunServer(with_connection=with_connection,
                             server_ip=server_ip,
                             server_port=server_port,
                             with_plot=with_plot,
                             sensorkit=what_device,
                             bluetooth_address=bluetooth_address,
                             acq_channels=acq_channels,
                             device_sampling_rate=1000,  # you can change the device sampling rate here
                             size_processing_window=100,
                             server_acquisition_rate=100
                             )
    local_server.run()