"""
This file is part of biosiglive. it is an example to see how to use biosiglive to compute the maximal voluntary
 contraction from EMG signals.
"""

from time import strftime
from biosiglive.processing.data_processing import OfflineProcessing
from biosiglive.gui.plot import LivePlot, Plot
from time import time, sleep
import os
import numpy as np
import pandas as pd

from biosiglive.streaming.client import Client, Message


class ComputeMvc:
    def __init__(self, output_file: str = None,
                 muscle_names: list = None,
                 with_connection: bool = True,
                 server_ip: str = None,
                 server_port: int = None
                 ):
        """
        Initialize the class.

        Parameters
        ----------
        server_ip : str
            The ip of the server.
        server_port : int
            The port of the server.
        output_file : str
            The path of the output file.
        muscle_names : list
            The list of the muscle names.
        frequency : float
            The frequency of the device.
        acquisition_rate : float
            The acquisition rate of the acquisition.
        mvc_windows : int
            size of the window to compute the mvc.
        with_connection : bool
            If True, the program will try to connect to the device.
        range_muscle : tuple
            The range of the muscle to compute the mvc.
        """
        # Set MVC output file name
        current_time = strftime("%Y%m%d-%H%M")
        self.output_file = f"_{current_time}.csv" if not output_file else output_file

        # Set server connection parameters
        self.server_ip = server_ip # "localhost" or None
        self.server_port = server_port # 5002 or None

        # Set muscle information
        self.muscle_names = muscle_names
        self.nb_muscles = len(self.muscle_names)

        # Set frequency and acquisition parameters depending on connection
        self.with_connection = with_connection
        if self.with_connection:
            message = Message(command=["emg"],
                      read_frequency=100,
                      nb_frame_to_get=1,
                      get_raw_data=False,
                      mvc_list=None)

            client = Client(server_ip=self.server_ip, port=self.server_port, type="TCP")
            data = client.get_data(message)
            sleep(1)
            self.frequency = data['sampling_rate'][0]
            self.acquisition_rate = data['system_rate'][0]
        else:
            self.frequency = 1000
            self.acquisition_rate = 50

        self.show_data = False
        self.plot_app, self.rplt, self.layout, self.app, self.box = None, None, None, None, None
        self.is_processing_method = False
        self.try_number = 0

        self.emg_processing = None
        self.moving_average, self.low_pass, self.custom = None, None, None

        self.first_trial = True
        self.try_name = ""
        self.try_list = []
        self.emg_interface = None

        # Delete tmp file if it still exists
        self._delete_tmp()

    def set_processing_method(self,
                              moving_average: bool = True,
                              low_pass: bool = False,
                              custom: bool = False,
                              custom_function: callable = None,
                              bandpass_frequency: tuple = (10, 425),
                              lowpass_frequency: float = 5,
                              lowpass_order: int = 4,
                              butterworth_order: int = 4,
                              ma_window: int = 200,
                              ):
        """
        Set the emg processing method.

        Parameters
        ----------
        moving_average : bool
            If True, the emg data will be processed with a moving average.
        low_pass : bool
            If True, the emg data will be processed with a low pass filter.
        custom : bool
            If True, the emg data will be processed with a custom function.
        custom_function : callable
            The custom function. Input : raw data, device frequency Output : processed data.
        bandpass_frequency : tuple
            The frequency of the bandpass filter.
        lowpass_frequency : float
            The frequency of the low pass filter.
        lowpass_order : int
            The order of the low pass filter.
        butterworth_order : int
            The order of the butterworth filter.
        ma_window : int
            The size of the moving average window.
        """

        self.moving_average = moving_average
        self.low_pass = low_pass
        self.custom = custom
        if [moving_average, custom, low_pass].count(True) > 1:
            raise ValueError("Only one processing method can be selected")
        if custom and not custom_function:
            raise ValueError("custom_function must be defined")
        if custom:
            self.emg_processing = custom_function
        else:
            emg_processing = OfflineProcessing()
            emg_processing.bpf_lcut = bandpass_frequency[0]
            emg_processing.bpf_hcut = bandpass_frequency[1]
            emg_processing.lpf_lcut = lowpass_frequency
            emg_processing.lp_butter_order = lowpass_order
            emg_processing.bp_butter_order = butterworth_order
            emg_processing.ma_win = ma_window
            self.emg_processing = emg_processing.process_emg
        self.is_processing_method = True

    def run(self, show_data: bool = False):
        """
        Run the MVC program.

        Parameters
        ----------
        show_data: bool
            If True, the data will be displayed in a plot.
        """
        self.show_data = show_data
        self.try_number = 0
        while True:
            if show_data:
                self.rplt, self.layout, self.app, self.box = self._init_live_plot(multi=True)
            nb_frame, var, duration = self._init_trial()
            c = 0
            trial_emg = self._mvc_trial(duration, nb_frame, var)
            # Get processed_emg from the trial_emg
            # processed_emg, raw_emg = self._process_emg(trial_emg) #COMMENTING OUT: TRYING WITHOUT PROCESSING
            # Plot the processed and raw emgs
            # self._plot_trial(raw_emg, processed_emg) #COMMENTING OUT: TRYING WITHOUT PROCESSING

            task = input(
                "Press 'c' to do another MVC trial, 'r' to repeat this trial, or 'q' to quit.\n"
            )

            while task != "c" and task != "r" and task != "q":
                print(f"Invalid entry ({task}). Please press 'c', 'r', or 'q' (in lowercase).")
                task = input(
                    "Press 'c' to do an other MVC trial," 
                    " 'r' to do again the MVC trial or 'q' then enter to quit.\n"
                )

            if task == "c" or "q":

                # Save emg processed to csv file
                # df = pd.DataFrame(processed_emg.T, columns = self.muscle_names) #COMMENTING OUT: TRYING WITHOUT PROCESSING
                df = pd.DataFrame(trial_emg.T, columns = self.muscle_names) # REPLACES LINE ABOVE, USES RAW DATA INSTEAD OF PROCESSED
                # df.insert(0, 'trial_index', list(range(0, processed_emg.shape[1]))) #COMMENTING OUT: TRYING WITHOUT PROCESSING
                df.insert(0, 'trial_index', list(range(0, trial_emg.shape[1]))) # REPLACES LINE ABOVE, USES RAW DATA INSTEAD OF PROCESSED
                df.insert(0, 'trial_name', self.try_name)
                df.to_csv('df_trial_tmp.csv', mode='a', index=False, header=self.first_trial) # append
                if self.first_trial == True:
                    self.first_trial = False

                if task == "q":
                    mvc = self._save_trial()
                    self._delete_tmp()
                    return mvc

            elif task == "r":
                # Do not save trial and continue
                # processed_emg, raw_emg = None, None #COMMENTING OUT: TRYING WITHOUT PROCESSING
                trial_emg = None

    def _init_trial(self):
        """
        Initialize the trial.

        Returns
        -------
        nb_frame : int
            The number of frames of the trial.
        var : float
            The current iteration.
        duration : float
            The duration of the trial.
        """

        try_name = input("Please enter a name of your trial (string) then press enter or press enter.\n")
        while try_name in self.try_list:
            try_name = input("This name is already used. Please chose and other name.\n")

        if try_name == "":
            self.try_name = f"MVC_{self.try_number}"
        else:
            self.try_name = f"{try_name}"
        self.try_number += 1

        self.try_list.append(self.try_name)
        t = input(
            f"Ready to start trial: {self.try_name}, with muscles :{self.muscle_names}. "
            f"Press enter to begin your MVC. or enter a number of seconds."
        )
        nb_frame = 0
        try:
            float(t)
            iter = float(t) * (self.frequency/self.acquisition_rate)
            var = int(iter)
            duration = True
        except ValueError:
            var = -1
            duration = False
        return nb_frame, var, duration

    def _mvc_trial(self, duration: float, nb_frame: int, var: float):
        """
        Run the MVC trial.
        Parameters
        ----------
        duration : float
            The duration of the trial.
        nb_frame : int
            The number of frames of the trial.
        var : float
            The current iteration.

        Returns
        -------
        trial_emg : numpy.ndarray
            The EMG data of the trial.
        """
        data = None
        if self.with_connection is True:
            # TODO: get e message to read info from server first, then moddify message
            # create message
            type_of_data = ["emg"]
            message = Message(command=type_of_data,
                      read_frequency=self.frequency,
                      nb_frame_to_get=self.acquisition_rate,
                      get_raw_data=False,
                      mvc_list=None)

        while True:
            try:
                if nb_frame == 0:
                    print(
                        "Trial is running please press 'Ctrl+C' when trial is ended "
                        "(it will not end the program)."
                    )

                if self.with_connection is True:
                    # Create a client to connect to server
                    client = Client(server_ip=self.server_ip, port=self.server_port, type="TCP")
                    # Get data streamed from server
                    client_data= client.get_data(message)
                    #time.sleep(1)
                    emg = np.array(client_data['emg_server'])
                    data_tmp = emg
                else:
                    data_tmp = np.random.random((self.nb_muscles, int(self.acquisition_rate)))
                tic = time()

                data = data_tmp if nb_frame == 0 else np.append(data, data_tmp, axis=1)
                
                self._update_live_plot(data, nb_frame)
                nb_frame += 1

                time_to_sleep = (1 / self.acquisition_rate) - (time() - tic)

                if time_to_sleep > 0:
                    sleep(time_to_sleep)
                else:
                    print(f"Delay of {abs(time_to_sleep)}.")

                if duration:
                    if nb_frame == var:
                        if self.with_connection is True:
                            print("\nStop acquiring from server...")
                        return data

            except KeyboardInterrupt:
                if self.with_connection is True:
                    print("\nStop acquiring from server...")
                if self.show_data is True:
                    self.app.disconnect()
                    try:
                        self.app.closeAllWindows()
                    except RuntimeError:
                        pass
                return data

    def _plot_trial(self, raw_data: np.ndarray = None, processed_data: np.ndarray = None):
        """
        Plot the trial.

        Parameters
        ----------
        raw_data : numpy.ndarray
            The raw EMG data of the trial.
        processed_data : numpy.ndarray
                The processed EMG data of the trial.
        """
        data = raw_data
        legend = ["Raw"]
        nb_column = 4 if raw_data.shape[0] > 4 else raw_data.shape[0]
        n_p = 0
        plot_comm = "y"
        print(f"Trial {self.try_name} terminated. ")
        while plot_comm != "n":
            if n_p != 0:
                plot_comm = input(f"Would you like to plot again ? 'y'/'n'")

            if plot_comm == "y":
                plot = input(
                    f"Press 'pr' to plot your raw trial,"
                    f" 'p' to plot your processed trial, 'b' to plot both or 'c' to continue,"
                    f" then press enter."
                )
                while plot != "p" and plot != "pr" and plot != "c" and plot != "b":
                    print(f"Invalid entry ({plot}). Please press 'p', 'pr', 'b',  or 'c' (in lowercase).")
                    plot = input(
                        f"Press 'pr' to plot your raw trial,"
                        f"'p' to plot your processed trial or 'c' to continue then press enter."
                    )

                if plot != "c":
                    if plot == "p":
                        data = processed_data
                        legend = ["Processed"]
                    elif plot == "b":
                        data = [raw_data, processed_data]
                        legend = ["Raw", "Processed"]
                    legend = legend * raw_data.shape[0]
                    x = np.linspace(0, raw_data.shape[1] / self.frequency, raw_data.shape[1])
                    print("Close the plot windows to continue.")
                    Plot().multi_plot(data,
                                      nb_column=nb_column,
                                      y_label="Activation level (v)",
                                      x_label="Time (s)",
                                      legend=legend,
                                      subplot_title=self.muscle_names,
                                      figure_name=self.try_name,
                                      x=x)
                else:
                    pass
                n_p += 1

    def _process_emg(self, data, save_tmp=True):
        """
        Process the EMG data.

        Parameters
        ----------
        data : numpy.ndarray
            The raw EMG data of the trial.
        save_tmp : bool
            If True, the processed data is saved in a temporary file.

        Returns
        -------
        numpy.ndarray
            The processed EMG data of the trial.
        """
        if not self.is_processing_method:
            self.set_processing_method()
        emg_processed = self.emg_processing(data, self.frequency, pyomeca=self.low_pass, ma=self.moving_average)

        return emg_processed, data

    def _init_live_plot(self, multi=True):
        """
        Initialize the live plot.

        Parameters
        ----------
        multi: bool
            If True, the live plot is initialized for multi-threads plot.
        Returns
        -------
        rplt: list of live plot, layout: qt layout, qt app : pyqtapp, checkbox : list of checkbox

        """
        self.plot_app = LivePlot() # multi_process=multi
        self.plot_app.add_new_plot("EMG", "curve", self.muscle_names)
        rplt, layout, app, box = self.plot_app.init_plot_window(plot=self.plot_app.plot[0], use_checkbox=True)
        return rplt, layout, app, box

    def _update_live_plot(self, data, nb_frame):
        """
        Update the live plot.
        Parameters
        ----------
        data: numpy.ndarray
            The EMG data to plot.
        nb_frame: int
            The current frame.
        """
        if self.plot_app is not None:
            plot_data = data if nb_frame*self.acquisition_rate < 5*self.frequency else data[:, -5*self.frequency:]
            self.plot_app.update_plot_window(self.plot_app.plot[0], plot_data, self.app, self.rplt, self.box)

    def get_data(self):
        """
        Get the EMG data from defined emg_interface.
        """
        return self.emg_interface.devices[0].get_device_data(stream_now=True, get_names=True)

    def _save_trial(self):
        """
        Save and end the trial.
        """

        save = input("Press 's' to save the trial data, other key to just return a list of MVC.\n")
        if save != "s":
            save = input("Data will not be saved. " "If you want to save press 's', if not, press enter.\n")

        print("Please wait during data processing (it could take some time)...")
        
        save = True if save == 's' else False

        # Load tmp trials data and make it numpy
        df = pd.read_csv('df_trial_tmp.csv')    # Open csv file
        if save:
            df.to_csv("TRIALS{}".format(self.output_file), index=False, header=True)
        df.drop('trial_index', axis=1, inplace=True)
        df.drop('trial_name', axis=1, inplace=True)
        mvc_trials = df.to_numpy().T # All the trials from tmp file

        mvc = OfflineProcessing.compute_mvc(mvc_trials)
        # Save MVC
        mvc_resh = np.reshape(mvc, (1, len(mvc))) # reshape to properly save DataFrame
        df_mvc = pd.DataFrame(mvc_resh, columns = self.muscle_names)
        df_mvc.to_csv("MVC{}".format(self.output_file), index=False, header=True)

        return mvc

    def _delete_tmp(self):
        """
        Delete the temporary file used to store the trials.
        """
        file = 'df_trial_tmp.csv'
        if (os.path.exists(file) and os.path.isfile(file)):
            os.remove(file)
            print("Temp file deleted")
        else:
            print("ERROR: file not found")

if __name__ == "__main__":

    # Ask if the data will come from the server of ir random
    with_connection = None
    while with_connection not in ['y', 'n']:
        with_connection = input("\nDo MVC with real data from server? (y, or n for random data): ")
    mvc_with_connection = True if with_connection == 'y' else False

    # TODO: Ask for these information before connecting. Right now they are hardcoded.
    # if mvc_with_connection:
    server_ip = "localhost" if mvc_with_connection else None
    server_port = 5004 if mvc_with_connection else None

    # TODO: get number of sensors from the server
    # Define number of muscles and muscle names
    n_electrodes = int(input("\nHow many muscles will be used (e.g. for 2 muscles, write 2): "))
    muscle_names = []
    for i in range(n_electrodes):
        muscle_names.append(input("Give a name to muscle #{}: ".format(i+1)))

    MVC = ComputeMvc(
        with_connection=mvc_with_connection,
        muscle_names=muscle_names,
        server_ip = server_ip,
        server_port = server_port
    )
    
    list_mvc = MVC.run()
    print(list_mvc)