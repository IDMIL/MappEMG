import scipy.io as sio
import time
from biosiglive.streaming.client import Client, Message
import numpy as np
try:
    from pythonosc.udp_client import SimpleUDPClient
except ModuleNotFoundError:
    pass
from biosiglive.io.save_data import add_data_to_pickle

if __name__ == '__main__':

    # Set program variables
    read_freq = 100  # Be sure that it's the same than server read frequency
    n_electrode = 2
    type_of_data = ["emg"]

    # Load MVC data from previous trials.
    # try:
    #     # Read data from the mvc result file (*.mat)
    #     list_mvc = sio.loadmat("MVC_xx_xx_xx22/MVC_xxxx.mat")["MVC_list_max"][0]
    # except IOError:
    #     list_mvc = np.random.rand(n_electrode, 50).tolist()
    #     print(np.shape(list_mvc))

    # Set file to save data
    # output_file = "stream_data_xxx"
    # output_dir = "test_accel"
    # data_path = f"{output_dir}/{output_file}"

    # Run streaming data
    host_ip = 'localhost'
    host_port = 5002
    # osc_ip = "127.0.0.1"
    # osc_port = 5137
    osc_server = True
    save_data = False # True
    # if osc_server is True:
    #     osc_client = SimpleUDPClient(osc_ip, osc_port) # ip and port of the phone
    #     print("Streaming OSC activated")
    print_data = False
    count = 0

    list_mvc = np.random.rand(n_electrode, 1).tolist()

    dummy_message = Message(command=type_of_data,
                      read_frequency=read_freq,
                      nb_frame_to_get=1,
                      get_raw_data=False,
                      mvc_list=list_mvc)
    client = Client(server_ip=host_ip, port=host_port, type="TCP")

    # Get data streamed from server
    data = client.get_data(dummy_message)
    time.sleep(1)
    system_rate = data['system_rate'][0]

    # Number of frames to get comes from the server
    # depending on the device frequency
    message = Message(command=type_of_data,
                      read_frequency=read_freq,
                      nb_frame_to_get=system_rate,
                      get_raw_data=False,
                      mvc_list=list_mvc)

    print("\nStart receiving from server")
    while True:

        # Gets the data from the server.
        # Create a client to get data from server
        client = Client(server_ip=host_ip, port=host_port, type="TCP")
        # Get all the data streamed from server
        data = client.get_data(message)

        # Get only the emg data as a numpy array.
        emg = np.array(data['emg_server']) # you can also get sampling_rate and system_rate
        print(emg) # emg.shape should be (2, 5) with bitalino frequency = 100

        # emg is "data_tmp" from client unprocessed (but already in mV)
        # TO DO: Check if mvc exists and use it if it does.
        # Include here what's in test_bitalino_data.py.

       
