import socket
import numpy as np
from time import sleep
import multiprocessing as mp
from biosiglive.interfaces.pytrigno_interface import PytrignoClient
from biosiglive.interfaces.vicon_interface import ViconClient
from biosiglive.processing.utils import NumpyQueue
from biosiglive.streaming.connection import Server
from biosiglive.interfaces.bitalino_interface import BitalinoClient
from biosiglive.processing.data_processing import OfflineProcessing

class RunServer():

    def __init__(self, with_connection=False, sensorkit=None, bluetooth_address=None, acq_channels=[]):
        
        self.sensorkit = sensorkit
        self.with_connection = with_connection
        self.bluetooth_address = bluetooth_address
        self.acq_channels = acq_channels
        self.device_sampling_rate = 1000
        self.streaming_rate = 100
        self.server_acquisition_rate = 10
        self.n_electrode = len(acq_channels)

        manager = mp.Manager()
        self.__emg_queue_in = manager.Queue()
        self.__emg_queue_out = manager.Queue()
        self.__event_emg = mp.Event()
        self.__process = mp.Process

    def run_sensor_acquisition(self):

        print("Starting Sensor Acquisition...")

        if self.with_connection:
            
            if self.sensorkit == 'bitalino':
                try:
                    sensor_interface = BitalinoClient(ip=self.bluetooth_address)
                    sensor_interface.add_device(
                        "Bitalino", rate=self.device_sampling_rate, system_rate=self.server_acquisition_rate, acq_channels=self.acq_channels)
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
                    sensor_interface.add_device("Vicon", rate=self.device_sampling_rate, system_rate=self.server_acquisition_rate)
                except:
                    raise RuntimeError("Could not create Vicon connection.")
            
            if self.sensorkit == 'pytrigno':
                try:
                    sensor_interface = PytrignoClient()
                    sensor_interface.add_device("Pytrigno", range=(0, self.n_electrode), rate=self.server_acquisition_rate)
                except:
                    raise RuntimeError("Could not create Pytrigno connection.")

                

        while True:

            if not self.with_connection:
                emg_tmp = np.random.randint(1024, size=(self.n_electrode, self.server_acquisition_rate)) # data range [0.0, 1024)
                emg_tmp = (emg_tmp/(2**10)-0.5)*3.3/1009*1000
            else:
                if self.sensorkit == 'bitalino':
                    try:
                        # get_device_data returns np with the bitalino data collected in the shape (len(acq_channels), self.server_acquisition_rate)
                        emg_tmp = sensor_interface.get_device_data(device_name="Bitalino")[0]
                        emg_tmp = (emg_tmp/(2**10)-0.5)*3.3/1009*1000  # convert to mV
                    except:
                        # TODO: Sometimes we get stuck in a "reconnecting loop"
                        # perhaps there should be a way of handling this.
                        try:
                            print("\nReconnecting Bitalino...\n")
                            sleep(5)
                            sensor_interface.close()
                            sleep(10)
                            sensor_interface = BitalinoClient(ip=self.bluetooth_address)
                            sensor_interface.add_device(
                                "Bitalino", rate=self.device_sampling_rate, system_rate=self.server_acquisition_rate, acq_channels=self.acq_channels)
                            sensor_interface.start_acquisition()
                        except:
                            continue
                
                if self.sensorkit == 'vicon':
                    sensor_interface.get_frame()
                    emg_tmp = sensor_interface.get_device_data(device_name="Vicon")[0]
                
                if self.sensorkit == 'pytrigno':
                    emg_tmp = sensor_interface.get_device_data(device_name="Pytrigno")[0]
            
            # STEP 1 - Put DICT into Queue IN
            self.__emg_queue_in.put_nowait({"emg_tmp": emg_tmp})


    def run_emg_processing(self):

        print("Starting EMG Processing...")

        emg_processing = OfflineProcessing()
        emg_processing.ma_win = 100
        emg_processing.bpf_lcut = 10
        emg_processing.bpf_hcut = 400
        emg_processing.lpf_lcut = 5.0
        emg_processing.lp_butter_order = 4
        emg_processing.bp_butter_order = 4

        emg_raw = NumpyQueue(max_size=1000, queue=np.zeros(shape=(self.n_electrode, 1000)), base_value=0)
        
        while True:
            try:
                # STEP 2 - Take DICT from Queue IN
                emg_data = self.__emg_queue_in.get_nowait()
                is_working = True
            except:
                is_working = False

            if is_working:
                emg_tmp = np.array(emg_data["emg_tmp"])
                emg_raw.enqueue(emg_tmp)
                emg_proc = emg_processing.process_emg(data=emg_raw.queue, frequency=self.device_sampling_rate, ma=True)
                # STEP 3 - Put DICT into Queue OUT
                self.__emg_queue_out.put({"emg_proc": emg_proc[:,-self.streaming_rate:]}) # Only send n streaming_rate samples
                # STEP 4 - Set event to let other process know it is ready
                self.__event_emg.set()

    def run_streaming(self):

        print("Starting Streaming...")

        server = Server(ip="localhost", port=5005, type='TCP')
        server.start()
        connected = False

        while True:
            
            if not connected:
                try: 
                    connection = server.client_listening()
                    connected = True
                except socket.timeout:
                    pass
            
            # STEP 5 - Wait for event
            self.__event_emg.wait()
            # STEP 6 - Take DICT from Queue OUT
            data = self.__emg_queue_out.get_nowait()
            # STEP 7 - Release lock
            self.__event_emg.clear()
            #print("Step -- 7")
            data_to_send = {}
            data_to_send["emg_proc"] = data["emg_proc"]
            data_to_send["n_electrode"] = self.n_electrode
            data_to_send["sampling_rate"] = self.device_sampling_rate
            data_to_send["system_rate"] = self.server_acquisition_rate
            
            if connected:
                try:
                    message = server.receive_message(connection)
                    print(message)
                    if message['command'] == ['emg']:
                        server.send_data(data_to_send, connection, message)
                    elif message['command'] == ['close']:
                        # TODO: Change so it does not send all data, but sends something.
                        server.send_data(data_to_send, connection, message)
                        connection.close()
                    else:
                        raise ValueError("Unkown message command.")
                except:
                    connection.close()
                    connected = False
                    print("\nClosing connection... \nListening to new client...\n")

    def run(self):

        print("\nStarting Server...\n")

        # TODO: include LiveData plots
        # process(name="reader", target=LiveData.save_streamed_data, args=(self,))]
        processes = []
        processes.append(self.__process(name="acquire_emg", target=RunServer.run_sensor_acquisition, args=(self,)))
        processes.append(self.__process(name="process_emg", target=RunServer.run_emg_processing, args=(self,)))
        processes.append(self.__process(name="stream_emg",  target=RunServer.run_streaming, args=(self,)))

        for p in processes:
            p.start()
        for p in processes:
            p.join()


if __name__ == '__main__':

    # Verify if user wants real device connected
    with_connection = None
    while with_connection not in ['y', 'n']:
        with_connection = input(
            "\nWith device connected? (y, or n for random data): ")
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
                print("\nThe macAddress variable on Windows can be \"XX:XX:XX:XX:XX:XX\" or \"COMX\" \n while on Mac OS can be \"/dev/tty.BITalino-XX-XX-DevB\"")
                # TODO: remove shortcut from main application
                bluetooth_address = input(
                    "\nBitalino bluetooth address (leave empty if \"/dev/tty.BITalino-7E-19-DevB\"): ")
                if bluetooth_address == "":
                    bluetooth_address = "/dev/tty.BITalino-7E-19-DevB"

    # Set acquisition channels (number of sensors)
    acq_channels = None
    while acq_channels == None:
        acq_channels = input("\nEnter list of acquisition channels (e.g. for A1 A2 A3, write 1 2 3): ").split(" ")
        try:
            acq_channels = [int(c)-1 for c in acq_channels]
            if not all(channel >= 0 and channel <= 6 for channel in acq_channels):
                print("\nInvalid acquisition channels (make sure they are separated by a space...)")
                acq_channels = None
        except:
            acq_channels = None

    # Run server with information provided
    local_server = RunServer(with_connection, what_device, bluetooth_address, acq_channels)
    local_server.run()