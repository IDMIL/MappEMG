
from os import system
import numpy as np
from biosiglive.interfaces.bitalino_interface import BitalinoClient
from biosiglive.processing.data_processing import RealTimeProcessing
from biosiglive.gui.plot import LivePlot
from time import sleep, time


if __name__ == '__main__':

    print("\nWelcome to the Bitalino example...")
    print("\nThe macAddress variable on Windows can be \"XX:XX:XX:XX:XX:XX\" or \"COMX\" \n while on Mac OS can be \"/dev/tty.BITalino-XX-XX-DevB\"")
    address_bitalino = input("\nBitalino Address (leave empty if \"/dev/tty.BITalino-1E-10-DevB\"): ")
    if address_bitalino == "":
        address_bitalino = "/dev/tty.BITalino-7E-19-DevB"
    try:
        bitalino_interface = BitalinoClient(ip=address_bitalino)
    except:
        print("Could not create Bitalino Client. Possibly bad address")
    
    # set acquisition channels
    acq_channels = input("\nEnter list of acquisition channels (e.g. for A1 A2 A3, write 1 2 3): ").split(" ")
    #acq_channels = acq_channels.split(" ")
    for i in range(len(acq_channels)):
        acq_channels[i] = int(acq_channels[i]) - 1
    
    # set sampling rate
    rate = int(input("\nEnter sampling rate (1, 10, 100, or 1000): ")) # 2000
    system_rate = rate//20 # 100
    if system_rate == 0:
        system_rate = 1
    
    # def add_device(self, name: str = None, rate: int = 1000, system_rate: int = 100, acq_channels: list = [1,2,3,4,5,6]):
    bitalino_interface.add_device("Bitalino", rate=rate, system_rate=system_rate, acq_channels=acq_channels)

    print()
    while True:

        data = bitalino_interface.get_device_data(device_name="Bitalino")
        print(data)

