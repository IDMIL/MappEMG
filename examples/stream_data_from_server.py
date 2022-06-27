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
    # device_host = "192.168.1.211"  # IP address of computer which run trigno device
    n_electrode = 2
    type_of_data = ["emg"] #, "imu"]

    # load MVC data from previous trials.
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
    host_port = 5000
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

    # TO DO: nb_frames_to_get?
    message = Message(command=type_of_data,
                      read_frequency=read_freq,
                      nb_frame_to_get=5,
                      get_raw_data=False,
                      mvc_list=list_mvc)


    client = Client(server_ip=host_ip, port=host_port, type="TCP")

    print("\nStart receiving from server")
    while True:

        # Create a client to connect to server
        client = Client(server_ip=host_ip, port=host_port, type="TCP")
        
        # Get data streamed from server
        data = client.get_data(message)

        time.sleep(1)
        if "emg" in type_of_data:
            emg = np.array(data['emg'])
            print(emg)
            #raw_emg = np.array(data['raw_emg'])

        # if ["imu"] in type_of_data:
        #     if len(np.array(data['imu']).shape) == 3:
        #         accel_proc = np.array(data['imu'])[:, :3, -1:]
        #         gyro_proc = np.array(data['imu'])[:, 3:6, -1:]
        #         raw_accel = np.array(data['raw_imu'])[:, :3, -1:]
        #         raw_gyro = np.array(data['raw_imu'])[:, 3:6, -1:]
        #     else:
        #         accel_proc = np.array(data['imu'])[:, -1:]
        #         gyro_proc = np.array(data['imu'])[:, -1:]
        #         raw_accel = np.array(data['raw_imu'])[:, :3, -1:]
        #         raw_gyro = np.array(data['raw_imu'])[:, 3:6, -1:]

        # if print_data is True:
        #     # if ["imu"] in type_of_data:
        #     #     print(f"Accel data :\n"
        #     #           f"proc : {accel_proc}\n"
        #     #           f"raw : {raw_accel}\n")
        #     #     print(f"Gyro data :\n"
        #     #           f"proc: {gyro_proc}\n"
        #     #           f"raw: {raw_gyro}")




        # if "emg" in type_of_data:
        #     print(f'EMG data: \n'
        #               f'proc: {emg}\n')#                      f'raw: {raw_emg}\n')
        
        
        
        
        #if osc_server is True:

           # if "emg" in type_of_data:
                #emg = np.random.rand(2, 50).tolist() # Bitalino data simulation
                
                # BitalinoClient
                # retrieve data from device
                # send this data, emg

                # 

                # process 
                
                #print(np.shape(emg))
                # emg_proc = emg[:, -1:].reshape(emg.shape[0])
                #osc_client.send_message("/emg/", emg) # send message to the phone

            # if ["imu"] in type_of_data:
            #     accel_proc = accel_proc.reshape(accel_proc.shape[0])
            #     gyro_proc = gyro_proc.reshape(gyro_proc.shape[0])
            #     osc_client.send_message("/accel/", accel_proc.tolist())
            #     osc_client.send_message("/gyro/", gyro_proc.tolist())

        # if save_data is True:
        #     if count == 0:
        #         print("Save data starting.")
        #         count += 1
        #     for key in data.keys():
        #         if key == 'imu':
        #             if len(np.array(data['imu']).shape) == 3:
        #                 data[key] = np.array(data[key])
        #                 data['accel_proc'] = data[key][:n_electrode, :3, :]
        #                 data['gyro_proc'] = data[key][n_electrode:, 3:6, :]
        #             else:
        #                 data[key] = np.array(data[key])
        #                 data['accel_proc'] = data[key][:n_electrode, :]
        #                 data['gyro_proc'] = data[key][n_electrode:, :]
        #         else:
        #             data[key] = np.array(data[key])
        #     add_data_to_pickle(data, data_path)
