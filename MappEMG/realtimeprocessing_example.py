from ast import Num
from biosiglive.streaming.connection import Server
from biosiglive.interfaces.bitalino_interface import BitalinoClient
import numpy as np
import threading
from biosiglive.processing.data_processing import OfflineProcessing
from biosiglive.processing.data_processing import RealTimeProcessing
from time import sleep
import matplotlib.pyplot as plt



emg_processing = RealTimeProcessing()
emg_processing.bpf_lcut = 10
emg_processing.bpf_hcut = 425
emg_processing.lpf_lcut = 5.0
emg_processing.lp_butter_order = 4
emg_processing.bp_butter_order = 4
emg_processing.ma_win = 100

n_electrode = input("\nNumber of acquisition channels: ")
system_rate = input("\nFrequency of acquisition: ")

n_electrode = int(n_electrode)
system_rate = int(system_rate)//20

if system_rate == 0: system_rate = 1

# Set up processing funtion
emg_processing.ma_win = system_rate
processor = emg_processing.process_emg
processed_data_to_send = (np.array([]),np.array([])) #setting this up as what was processed before, before it is updated

test_1 = np.random.normal(loc=0.0, scale=0.1, size=(1,50))
processed_data_to_send = processor(processed_data_to_send[0], processed_data_to_send[1], test_1, [1,1], False, False) #real time processing
processed_1 = processed_data_to_send[1]

test_2 = np.random.normal(loc=0.25, scale=0.1, size=(1,50))
processed_data_to_send = processor(processed_data_to_send[0], processed_data_to_send[1], test_2, [1,1], False, False) #real time processing
processed_2 = processed_data_to_send[1]
plt.plot(range(len(processed_2)),processed_2)
plt.show()

test_3 = np.random.normal(loc=0.5, scale=0.05, size=(1,50))
processed_data_to_send = processor(processed_data_to_send[0], processed_data_to_send[1], test_3, [1,1], False, False) #real time processing
processed_3 = processed_data_to_send[1]
plt.plot(range(len(processed_3)),processed_3)

test_4 = np.random.normal(loc=0.25, scale=0.1, size=(1,50))
processed_data_to_send = processor(processed_data_to_send[0], processed_data_to_send[1], test_4, [1,1], False, False) #real time processing
processed_4 = processed_data_to_send[1]
plt.plot(range(len(processed_4)),processed_4)

test_5 = np.random.normal(loc=0.0, scale=0.1, size=(1,50))
processed_data_to_send = processor(processed_data_to_send[0], processed_data_to_send[1], test_5, [1,1], False, False) #real time processing
processed_5 = processed_data_to_send[1]
plt.plot(range(len(processed_5)),processed_5)



# for i in range(5): #5 seconds
#     data_tmp = np.random.randint(1024, size=(n_electrode, system_rate)) # data range [0.0, 1024)
#     data_tmp = (data_tmp/(2**10)-0.5)*3.3/1009*1000
#     print('shape of data tmp: ', data_tmp.shape)
#     processed_data_to_send = processor(processed_data_to_send[0], processed_data_to_send[1], data_tmp, [1,1], False, False) #real time processing
#     #print(len(processed_data_to_send[0][0]),len(processed_data_to_send[0][1]))
#     #print(len(processed_data_to_send[1][0]),len(processed_data_to_send[1][1]))
#     #print(processed_data_to_send)
#     #print('shape of processed: ', processed_data_to_send[0].shape)