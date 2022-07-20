
from ast import Num
from biosiglive.streaming.connection import Server
from biosiglive.interfaces.bitalino_interface import BitalinoClient
import numpy as np
import threading
from biosiglive.processing.data_processing import OfflineProcessing
from time import sleep
from biosiglive.processing.utils import NumpyQueue

### SETTING UP PROCESSOR ###

emg_processing = OfflineProcessing()
emg_processing.bpf_lcut = 10
emg_processing.bpf_hcut = 425
emg_processing.lpf_lcut = 5.0
emg_processing.lp_butter_order = 4
emg_processing.bp_butter_order = 4
emg_processing.ma_win = 100


# Mutex
LOCK = threading.Lock()
# Queue
sample_queue = NumpyQueue()

# Bitalino thread
def run_bitalino_acquisition(address_bitalino, rate, system_rate, acq_channels):

    global sample_queue

    try:
        bitalino_interface = BitalinoClient(ip=address_bitalino)
        bitalino_interface.add_device("Bitalino", rate=rate, system_rate=system_rate, acq_channels=acq_channels)
    except:
        raise RuntimeError("Could not create Bitalino connection. Make sure you bluetooth is activated and you have the correct bitalino address.")
    try:
        bitalino_interface.start_acquisition()
    except:
        raise RuntimeError("Could not start acquisition Bitalino connection.")

    while True:
        try:
            # get_device_data returns np with the bitalino data collected in the shape (len(acq_channels), system_rate)
            data_tmp = bitalino_interface.get_device_data(device_name="Bitalino")[0]
            data_tmp = (data_tmp/(2**10)-0.5)*3.3/1009*1000 # convert to mV
            LOCK.acquire()
            sample_queue.enqueue(data_tmp)
            print("Got data")
            LOCK.release()
            sleep(0.25)
        except:

            # TODO: Sometimes we get stuck in a "reconnecting loop"
            # perhaps there should be a way of handling this.
            try:
                print("\nReconnecting Bitalino...\n")
                sleep(5)
                bitalino_interface.close()
                sleep(10)
                bitalino_interface = BitalinoClient(ip=address_bitalino)
                bitalino_interface.add_device("Bitalino", rate=rate, system_rate=system_rate, acq_channels=acq_channels)
                bitalino_interface.start_acquisition()
            except:
                continue


if __name__ == '__main__':

    server = Server(ip="localhost", port=5005, type='TCP')
    server.start()

    print("\nServer starting...")

    with_connection = None
    while with_connection not in ['y', 'n']:
        with_connection = input("\nWith device connected? (y, or n for random data): ")

    #### read bitalino bluetooth address if there is a connection ####
    if with_connection == 'y':
        print("\nThe macAddress variable on Windows can be \"XX:XX:XX:XX:XX:XX\" or \"COMX\" \n while on Mac OS can be \"/dev/tty.BITalino-XX-XX-DevB\"")
        address_bitalino = input("\nBitalino Address (leave empty if \"/dev/tty.BITalino-7E-19-DevB\"): ")
        if address_bitalino == "":
            address_bitalino = "/dev/tty.BITalino-7E-19-DevB"

    #### set acquisition channels ####
    acq_channels = ['']
    boo = True
    while acq_channels == [''] or boo:
        if acq_channels == ['']:
            acq_channels = input("\nEnter list of acquisition channels (e.g. for A1 A2 A3, write 1 2 3): ").split(" ")
        elif boo: #always true so always checked
            try:
                acq_channels = [int(c) for c in acq_channels]
                if not all(int(channel) > 0 and int(channel) < 7 for channel in acq_channels):
                    print("\nInvalid acquisition channels (make sure they are seperated by a space...)")
                    acq_channels = input("\nEnter list of acquisition channels (e.g. for A1 A2 A3, write 1 2 3): ").split(" ")
                else:
                    break
            except ValueError:
                acq_channels = input("\nEnter list of acquisition channels (e.g. for A1 A2 A3, write 1 2 3): ").split(" ")

    
    n_electrode = len(acq_channels)
    for i in range(n_electrode):
        acq_channels[i] = int(acq_channels[i]) - 1

    #### set sampling rate according to 2000/100 ratio ####
    rate = None
    while rate not in [1,10,100,1000]:
        rate = input("\nEnter sampling rate (1, 10, 100, or 1000): ")
        try:
            rate = int(rate)
        except ValueError:
            print("\nSampling rate must be a valid number.")

    # Define system_rate according to rate
    system_rate = rate//20
    if system_rate == 0: system_rate = 1

    # Set up processing funtion
    emg_processing.ma_win = system_rate
    processor = emg_processing.process_emg

    # Initialize sample queue with correect number of electrodes and full of zeros
    sample_queue.queue = np.ones((n_electrode, 1000))

    #### start bitalino thread ####
    if with_connection == 'y':
        try:
            bitalino_t = threading.Thread(target=run_bitalino_acquisition, args=(address_bitalino, rate, system_rate, acq_channels))
            bitalino_t.daemon = True
            bitalino_t.start()
        except:
            raise RuntimeError("Failed to create and start Bitalino thread...")
        
    print("\nStart streaming...")

    while True:

        if with_connection == 'n':
            data_tmp = np.random.randint(1024, size=(n_electrode, system_rate)) # data range [0.0, 1024)
            data_tmp = (data_tmp/(2**10)-0.5)*3.3/1009*1000
            sample_queue.enqueue(data_tmp)
            print("Random data")

        LOCK.acquire()
        # processing the data
        processed_data_to_send = processor(sample_queue.queue, rate, pyomeca=False, ma=True) # processing from amadeo, ma is moving average/pyomeca is low pass        
        #processed_data_to_send = sample_queue.dequeue(system_rate)
        sample_queue.dequeue(system_rate) # COMMENT OUT IF WANT TO TRY WITHOUT PROCESSING
        LOCK.release()

        # creating data dict
        data = {"emg_server": processed_data_to_send[:,:system_rate], "n_electrode": n_electrode, "sampling_rate": rate, "system_rate": system_rate}
        print("------ sent data: queue size", sample_queue.queue.shape)
        sleep(0.25)

        try:
            server.client_listening(data)
        except KeyboardInterrupt:
            server.close()
            print("\nClosing server...\n")
            exit(0)
        else:
            continue # in case client_listening failes, try again next loop