import numpy as np
import pandas as pd
from time import sleep
from MappEMG.processing import Mapper, EMGprocess, Emitter
from biosiglive.processing.data_processing import GenericProcessing
from biosiglive.interfaces.tcp_interface import (
    TcpClient,
    DeviceType,
)

if __name__ == '__main__':

    print("\nClient starting...")

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

    # Get data from server and close connection
    client = TcpClient(server_ip, server_port, read_frequency=100)
    # client.add_device(
    #     1, command_name="other_paras", device_type=DeviceType.Emg, name="Bitalino", rate=100
    # )

    data_otherpara = client.get_data_from_server(
        command=["other_paras"],
        nb_frame_to_get=1,
    )
    system_rate = data_otherpara['other_paras'][2]
    read_freq = data_otherpara['other_paras'][1]
    n_electrode = data_otherpara['other_paras'][0]

    # client.add_device(
    #     1, command_name="close", device_type=DeviceType.Emg, name="close", rate=100
    # )
    # client.get_data_from_server(
    #     command=["close"],
    #     nb_frame_to_get=1,
    # )


    # Load MVC data from previous trials or random
    load_mvc = None
    while load_mvc not in ['y', 'n']:
        load_mvc = input("\nDo you want to load real MVC values? ('y' or 'n' for random): ")

    if load_mvc == 'n':
        list_mvc = np.random.rand(n_electrode, 1).tolist()
    else:
        mvc_file = input("\nInput name of the MVC .csv file (for example \"MVC_20220707-1915.csv\"): ")
        list_mvc = pd.read_csv(mvc_file)  # Open .csv file
        list_mvc = list_mvc.to_numpy().T.tolist()  # Get MVC in the proper shape
        list_mvc = list_mvc[2:]

    # Asking user if they want to send haptics to phone
    emit = True
    n_devices = None
    while not isinstance(n_devices, int):
        n_devices = input('\nHow many devices with the hAPPtiks app would you like to connect? ')
        try:
            n_devices = int(n_devices)
            if n_devices < 0:
                pass
        except:
            pass

    if n_devices == 0:
        emit = False
    else:

        # Initializing phones to which we send the haptics
        emitter = Emitter()

        n = 1
        while n != int(n_devices) + 1:
            ip = input(f'\nIP of device number {n} (e.g: XXX.XXX.X.X): ')
            port = input(f'\nPORT of device number {n} (e.g: 2222): ')
            try:
                ip = str(ip)
                port = int(port)
                emitter.add_device_client(ip, port)
                n = n + 1
            except ValueError:
                print("\nInvalid IP or PORT, try again...")

        # Initializing mapper
        mapper = Mapper(n_electrode, system_rate)
        mapping = [0.5, 0.5]

        # Initializing weights
        boo = True  # keeps track that all values can be cast to float, basically serves as a while true loop
        weights_raw = ['']  # keeps track no empty string is passed
        while weights_raw == [''] or boo:
            if weights_raw == ['']:  # if empty string is passed
                weights_raw = input(
                    "\nAttribute weights between 0 and 1 to each sensor (e.g for A1 A2 A3, write 0.45 1 0): ").split(
                    " ")
            elif boo:  # boo is always true so that this is always checked
                try:
                    weights_raw = [float(w) for w in weights_raw]
                    if (len(weights_raw) != n_electrode or not (all(float(w) <= 1 for w in weights_raw))):
                        print(
                            "\nNumber of weights does not correspond to number of channels or values are not between 0 and 1...")
                        weights_raw = input(
                            "\nAttribute weights between 0 and 1 to each sensor (e.g for A1 A2 A3 A4, tou can write 1 0.45 1 0.80): ").split(
                            " ")
                    else:
                        break
                except ValueError:
                    print("\nYou must input a valid weight between 0 and 1.")
                    weights_raw = input(
                        "\nAttribute weights between 0 and 1 to each sensor (e.g for A1 A2 A3, write 0.45 1 0): ").split(
                        " ")

        weights = np.empty((1, n_electrode))
        for i, w in enumerate(weights_raw):
            weights[0][i] = float(w)

        amplifier = input(
            "\nAmplify the muscle activity to all sensors (range: 0-2): ").split(" ")

    # Initializing post processor
    post_processor = EMGprocess()
    generic_processing = GenericProcessing()

    print("\nStart receiving from server...\n")

    while True:
        client = TcpClient(server_ip, server_port, read_frequency=system_rate)
        # client.add_device(
        #     1, command_name="emg_proc", device_type=DeviceType.Emg, name="Bitalino", rate=system_rate
        # )

        client_data = client.get_data_from_server(
            command=["emg_proc"],
            nb_frame_to_get=1,
        )
        emg = np.array([client_data["emg_proc"]])
        print("emg", emg)
        emg_amp = []
        for i in range(len(emg)):
            new_emg_amp = [emg[i] * float(amplifier[i])]
            emg_amp.append(new_emg_amp)
        emg = np.array(emg_amp)

        # Post processing data to be emitted
        perc_mvc = generic_processing.normalize_emg(emg, list_mvc)
        post_processor.input(perc_mvc)  # inputting data to be processed
        post_processor.slide()  # smoothing the data
        post_processor.clip()  # clipping data in case it is not between 0 and 1
        data_tmp = post_processor.scale(1)  # for now scaling to 1 as it's random data

        # print(data_tmp)

        if emit:

            # Mapping and emitting to iOS application
            mapper.input(data_tmp)
            weighted_avr = mapper.weighted_average(weights)

            for w in weighted_avr[0]:
                try:
                    mapping_hap = mapper.toFreqAmpl(w)
                    mapping_col = mapper.toRgbBri(w)
                    emitter.sendMessage(mapping_hap, mapping_col)
                    sleep(0.002)
                except TypeError:
                    print("ERROR with toFreqAmpl...")
                    emitter.sendMessage(mapping_hap, mapping_col)
                    sleep(0.002)