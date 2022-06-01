
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
        address_bitalino = "/dev/tty.BITalino-1E-10-DevB"
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

    # vicon_interface.devices[-1].set_process_method(RealTimeProcessing().get_peaks)
    # force_z, force_z_process = [], []
    # if show_cadence:
    #     plot_app = LivePlot()
    #     plot_app.add_new_plot("cadence", "curve", ["force_z_R", "force_z_L", "force_z_R_raw", "force_z_L_raw"])
    #     rplt, window, app, box = plot_app.init_plot_window(plot=plot_app.plot[0], use_checkbox=True)

    # nb_second = 60
    # nb_min_frame = vicon_interface.devices[-1].rate * nb_second
    # time_to_sleep = 1/vicon_interface.devices[-1].system_rate
    # count = 0
    # tic = time()

    # cadence_wanted = 80
    # time = np.linspace(0, np.pi*2 * cadence_wanted/2, 120000)
    # amplitude = np.sin(time)
    # F_r = [i if i > 0 else -i for i in amplitude]
    # F_l = [-i if i < 0 else 0 for i in amplitude]
    # import matplotlib.pyplot as plt
    # plt.plot(F_l)
    # plt.plot(F_r)
    # plt.show()
    # sample = 20
    # c = 0
    # force_z_tmp = np.zeros((2, sample))
    # is_one = [False, False]
    print()
    while True:
        
        data = bitalino_interface.get_device_data(device_name="Bitalino")
        print(data)
        # force_z_tmp = data[0][[2, 8], :]
        # force_z_tmp[0, :], force_z_tmp[1, :] = F_r[c:c + sample], F_l[c:c + sample]
        # plt.plot(force_z_tmp[0, :])
        # plt.plot(force_z_tmp[1, :])
        # plt.show()
        # c = c + sample if c + sample < len(F_r) else 0
        # cadence, force_z_process, force_z, is_one = vicon_interface.devices[0].process_method(new_sample=force_z_tmp,
        #                                                                               signal=force_z,
        #                                                                               signal_proc=force_z_process,
        #                                                                               threshold=0.01,
        #                                                                               nb_min_frame=nb_min_frame,
        #                                                                               is_one=is_one,
        #                                                                               min_peaks_interval=2000
        #                                                                               )
        # if show_cadence:
        #     plot_app.update_plot_window(plot_app.plot[0], np.concatenate((force_z_process, force_z), axis=0), app, rplt, box)

        # if count == 100:
        #     print(f"Mean cadence for the last {nb_second} s is :{cadence}")
        #     count = 0
        #  count += 1
        # sleep(time_to_sleep)

