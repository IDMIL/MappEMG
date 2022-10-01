"""
This file is part of biosiglive. it is an example to see how to use biosiglive to compute the maximal voluntary
 contraction from EMG signals.
"""

from time import strftime, time, sleep
from biosiglive.processing.data_processing import OfflineProcessing
from biosiglive.gui.plot import Plot
import os
import numpy as np
import pandas as pd
import datetime

from biosiglive.streaming.client import Client, Message


class ComputeMvc:
    def __init__(self, output_file: str = None,
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
        with_connection : bool
            If True, the program will try to connect to the device.
        """
        # Set MVC output file name
        current_time = strftime("%Y%m%d-%H%M")
        self.output_file = f"_{current_time}.csv" if not output_file else output_file

        # Set server connection parameters
        self.server_ip = server_ip
        self.server_port = server_port

        # Set frequency and acquisition parameters depending on connection
        self.with_connection = with_connection
        if self.with_connection:
            
            client = Client(server_ip=server_ip, port=server_port)
            message = Message(command=['emg'], nb_frame_to_get=1)
            client.connect()
            data = client.get_data(message) # Get number of electrodes from server
            self.n_electrodes = np.array(data['emg_proc']).shape[0]
            # Close connection
            message = Message(command=['close'])
            client.get_data(message)
            
            print("Total of {} electrodes connected".format(self.n_electrodes))
            muscle_names = []
            for i in range(self.n_electrodes):
                muscle_names.append(input("Give a name to muscle #{}: ".format(i+1)))
            self.muscle_names = muscle_names
            self.frequency = data['sampling_rate'][0]
            self.acquisition_rate = data['system_rate'][0]
            self.effective_rate = self.frequency/self.acquisition_rate

        else:
            self.muscle_names = ['a', 'b']
            self.n_electrodes = 2
            self.frequency = 1000
            self.acquisition_rate = 10
            self.effective_rate = self.frequency/self.acquisition_rate

        self.first_trial = True
        self.try_name = ""
        self.try_list = []

        # Delete tmp file if it still exists
        self._delete_tmp()

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
            var, duration = self._init_trial()
            
            # Get data from mvc trial
            trial_emg = self._mvc_trial(duration, var)
            # Plot the raw emg data collected
            self._plot_trial(trial_emg)

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
                df = pd.DataFrame(trial_emg.T, columns = self.muscle_names)
                df.insert(0, 'trial_index', list(range(0, trial_emg.shape[1])))
                df.insert(0, 'trial_name', self.try_name)
                df.to_csv('df_trial_tmp.csv', mode='a', index=False, header=self.first_trial) # append trial to temp csv
                if self.first_trial == True:
                    self.first_trial = False

                # if quit, save trial and delete tmp
                if task == "q":
                    mvc = self._save_trial()
                    self._delete_tmp()
                    return mvc

            elif task == "r":
                # Do not save trial and continue 
                trial_emg = None

    def _init_trial(self):
        """
        Initialize the trial.

        Returns
        -------
        var : float
            The current iteration.
        duration : float
            The duration of the trial.
        """

        try_name = input("Please enter a name of your trial (string) then press enter or press enter.\n")
        while try_name in self.try_list:
            try_name = input("This name is already used. Please chose an other name.\n")

        if try_name == "":
            self.try_name = f"MVC_{self.try_number}"
        else:
            self.try_name = f"{try_name}"
        self.try_number += 1

        self.try_list.append(self.try_name)
        t = input(
            f"Ready to start trial: {self.try_name}, with muscles :{self.muscle_names}. "
            f"Press enter to begin your MVC or enter a number of seconds."
        )
        try:
            float(t)
            iter = float(t) * (self.effective_rate)
            var = int(iter)
            duration = True
        except ValueError:
            var = -1
            duration = False
        return var, duration

    def _mvc_trial(self, duration: float, var: float):
        """
        Run the MVC trial.

        Parameters
        ----------
        duration : float
            The duration of the trial.
        var : float
            The current iteration.

        Returns
        -------
        trial_emg : numpy.ndarray
            The EMG data of the trial.
        """
        data = None
        if self.with_connection is True:
            type_of_data = ["emg"]
            message = Message(command=type_of_data,
                      nb_frame_to_get=self.acquisition_rate)
            client = Client(server_ip=self.server_ip, port=self.server_port, type="TCP")
        
        dummy = 0
        connected = False
        nb_frame = 0
        if var == -1:
            print("\nTrial is running...\nPlease press 'Ctrl+C' to finsish trial.\n")
        while True:
            try:
                if self.with_connection is True:
                    if not connected:
                        client.connect()
                        connected = True
                    if connected:
                        client_data = client.get_data(message)
                        emg = np.array(client_data['emg_proc'])
                        data_tmp = emg
                else:
                    data_tmp = np.random.randint(1024, size=(self.n_electrodes, int(self.acquisition_rate)))
                    data_tmp = (data_tmp/(2**10)-0.5)*3.3/1009*1000
                
                # Get data streamed from server
                if dummy == 0:
                    a = datetime.datetime.now() # timing check purposes
                    print("Got data from server at time", a)
                    dummy = 1
                
                tic = time()

                data = data_tmp if nb_frame == 0 else np.append(data, data_tmp, axis=1)
                nb_frame += 1
                time_to_sleep = (1 / (self.effective_rate)) - (time() - tic)

                if time_to_sleep > 0:
                    sleep(time_to_sleep)
                else:
                    print(f"Delay of {abs(time_to_sleep)}.")

                if duration:
                    if nb_frame == int(var):
                        print("\nStop acquiring from server...")
                        b = datetime.datetime.now() # timing check purposes
                        print("Got data from server at time", b)
                        c = b - a
                        print("acquiring data took", c.total_seconds())
                        print("n of frames: ", nb_frame)
                        print(data.shape)
                        return data

            except KeyboardInterrupt:
                print("\nStop acquiring from server...")
                b = datetime.datetime.now() # timing check purposes
                print("Got data from server at time", b)
                c = b - a
                print("acquiring data took", c.total_seconds())
                print("n of frames: ", nb_frame)
                print(data.shape)
                return data


    def _plot_trial(self, raw_data: np.ndarray = None):
        """
        Plot the trial.

        Parameters
        ----------
        raw_data : numpy.ndarray
            The raw EMG data of the trial.
        """
        data = raw_data
        legend = ["Processed MVC trial"]
        nb_column = 4 if raw_data.shape[0] > 4 else raw_data.shape[0]
        plot_comm = "y"
        print(f"Trial {self.try_name} terminated. ")
        while plot_comm != "n":
            plot_comm = input(f"Would you like to plot your trial ? 'y'/'n'")
            if plot_comm == "y":

                legend = legend * raw_data.shape[0]
                x = np.linspace(0, raw_data.shape[1] / (self.effective_rate), raw_data.shape[1])
                print("Close the plot windows to continue.")
                Plot().multi_plot(data,
                                    nb_column=nb_column,
                                    y_label="Activation level (mV)",
                                    x_label="Time (s)",
                                    legend=legend,
                                    subplot_title=self.muscle_names,
                                    figure_name=self.try_name,
                                    x=x)

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
            print("Temp file already deleted")

if __name__ == "__main__":

    # Ask if the data will come from the server of ir random
    with_connection = None
    while with_connection not in ['y', 'n']:
        with_connection = input("\nDo MVC with real data from server? (y, or n for random data): ")
    mvc_with_connection = True if with_connection == 'y' else False

    server_ip = None
    server_port = None
    if mvc_with_connection:
        server_ip="localhost"
        server_port=5005
        # Verify if user wants to change ip or port
        change_ip_or_port = None
        while change_ip_or_port != '':
            print("\nClient will connect to server on IP:'{}' and PORT:'{}'".format(server_ip, server_port))
            change_ip_or_port = input("\tTo change IP -- Press 1 and 'Enter'\n\tTo change PORT -- Press 2 and 'Enter'\n\tTo continue -- Leave empty and press 'Enter': ")
            if change_ip_or_port == '1':
                server_ip = input("New IP address: ")
            elif change_ip_or_port == '2':
                try:
                    server_port = int(input("New PORT: "))
                except:
                    print("Invalid PORT")

    MVC = ComputeMvc(
        with_connection=mvc_with_connection,
        server_ip=server_ip,
        server_port=server_port
    )
    
    list_mvc = MVC.run()
    print(list_mvc)