from ast import Raise
from logging import raiseExceptions
from os import system
from biosiglive.streaming.connection import Server
from biosiglive.interfaces.bitalino_interface import BitalinoClient
import numpy as np
import threading
from time import sleep

# mutex
LOCK = threading.Lock()

# data_tmp initialization
data_tmp = np.zeros((1, 1))

# Bitalino thread
def run_bitalino_acquisition(address_bitalino, rate, system_rate, acq_channels):

    global data_tmp

    try:
        bitalino_interface = BitalinoClient(ip=address_bitalino)
        bitalino_interface.add_device("Bitalino", rate=rate, system_rate=system_rate, acq_channels=acq_channels)
        bitalino_interface.start_acquisition()
    except:
        raise RuntimeError("Could not create Bitalino connection. Make sure you bluetooth is activated and you have the correct bitalino address.")

    while True:
        try:
            # get_device_data returns np with the bitalino data collected in the shape (len(acq_channels), system_rate)
            data_tmp_raw = bitalino_interface.get_device_data(device_name="Bitalino")[0]
            LOCK.acquire()
            data_tmp = (data_tmp_raw/(2**10)-0.5)*3.3/1009*1000
            print("Got data")
            LOCK.release()
            sleep(0.1)
        except:
            try:
                print("\nReconnecting Bitalino...\n")
                bitalino_interface.close()
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

    # start bitalino if there is a connection
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

    system_rate = rate//20
    if system_rate == 0: system_rate = 1 

    if with_connection == 'y':
        try:
            bitalino_t = threading.Thread(target=run_bitalino_acquisition, args=(address_bitalino, rate, system_rate, acq_channels))
            bitalino_t.daemon = True
            bitalino_t.start()
        except:
            raise RuntimeError("Failed to create and start Bitalino thread...")
        
    print("\nStart streaming...")

    # karl_tmp = np.array([[0, 1, 2, 3, 4, 5, 6, 7, 8, 9], [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]])

    while True:

        if with_connection == 'n':
            # data_tmp = karl_tmp # np.array(list(range(0, 100)))
            data_tmp = np.random.randint(1024, size=(len(acq_channels), system_rate)) # data range [0.0, 1.0)
            data_tmp = (data_tmp/(2**10)-0.5)*3.3/1009*1000
                
        # create dictionary to send
        LOCK.acquire()
        data = {"emg_server": data_tmp, "n_electrode": n_electrode, "sampling_rate": rate, "system_rate": system_rate}
        print("----- Sent data")
        LOCK.release()
        sleep(0.1)

        try:
            server.client_listening(data)
        except KeyboardInterrupt:
            server.close()
            print("\nClosing server...\n")
            exit(0)
        else:
            continue # in case client_listening failes, try again next loop