from biosiglive.streaming.connection import Server
from biosiglive.streaming.client import Message
from biosiglive.interfaces.bitalino_interface import BitalinoClient
from biosiglive.processing.mappEMG import Mapper
from biosiglive.processing.mappEMG import EMGprocess
from biosiglive.processing.mappEMG import Emitter
import numpy as np


if __name__ == '__main__':
    
    server = Server(ip="localhost", port=5000, type='TCP')
    server.start()

    print("\nThe macAddress variable on Windows can be \"XX:XX:XX:XX:XX:XX\" or \"COMX\" \n while on Mac OS can be \"/dev/tty.BITalino-XX-XX-DevB\"")
    address_bitalino = input("\nBitalino Address (leave empty if \"/dev/tty.BITalino-7E-19-DevB\"): ")
    if address_bitalino == "":
        address_bitalino = "/dev/tty.BITalino-7E-19-DevB"
    try:
        bitalino_interface = BitalinoClient(ip=address_bitalino)
    except:
        print("Could not create Bitalino Client. Possibly bad address")

    #### set acquisition channels ####
    acq_channels = input("\nEnter list of acquisition channels (e.g. for A1 A2 A3, write 1 2 3): ").split(" ")
    #acq_channels = acq_channels.split(" ")
    for i in range(len(acq_channels)):
        acq_channels[i] = int(acq_channels[i]) - 1
    
    n = len(acq_channels)

    #### initializing weights ####
    weights_raw = input("\nAttribute weights between 0 and 1 to each sensor (e.g for A1 A2 A3, write 0.45 1 0): ").split(" ")
    while len(weights_raw) != n:
        print("\nNumber of weights does not correspond to number of channels")
        weights_raw = input("\nAttribute weights between 0 and 1 to each sensor (e.g for A1 A2 A3, write 0.45 1 0): ").split(" ")
    
    weights = np.empty((1,n))
    for i, w in enumerate(weights_raw):
        weights[0][i] = float(w)

    #### set sampling rate ####
    rate = int(input("\nEnter sampling rate (1, 10, 100, or 1000): ")) # 2000
    system_rate = rate//20 # 100
    if system_rate == 0:
        system_rate = 1
    
    #### initializing post processor ####
    post_processor = EMGprocess()

    #### initializing mapper ####
    mapper = Mapper(n,system_rate) 

    #### initializing phones to which we send the haptics ####
    emitter = Emitter()
    n_devices = input('\nHow many devices with the haptics app would you like to connect? ')
    n = 1
    while n != int(n_devices)+ 1:
        ip = input(f'\nIP of device number {n} (e.g: XXX.XXX.X.X): ')
        port = input(f'\nPORT of device number {n} (e.g: 2222): ')
        ip = str(ip)
        port = int(port)
        try:
            emitter.add_device_client(ip,port)
            n = n + 1
        except:
            print("Invalid IP or PORT, try again...")


    
    # def add_device(self, name: str = None, rate: int = 1000, system_rate: int = 100, acq_channels: list = [1,2,3,4,5,6]):
    bitalino_interface.add_device("Bitalino", rate=rate, system_rate=system_rate, acq_channels=acq_channels)

    bitalino_interface.start_acquisition()
    print("\nStart streaming")

    # Stream data indefinetly until error occurs
    # TO DO: investigate errors in bitalino. They occur quite often and need to be handled, mock data, average, or zero.
    while True:

      data_tmp = bitalino_interface.get_device_data(device_name="Bitalino")[0]
        
      data = {"emg_proc": data_tmp, "norm_emg": False}
      server.client_listening(data)