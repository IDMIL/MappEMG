<!-- <p align="center">
    <img
      src="https://github.com/karlmiko/biosiglive/tree/refactor/MappEmg_pipeline"
      alt="logo"
    />
</p> -->

![alt text](https://github.com/karlmiko/biosiglive/blob/main/images/MappEmg_pipeline.png)

`MappEMG` allows the audience to experience the performer's muscle effort, an essential component of music performance typically unavailable for direct visual observation. The goal is thus to give the listeners access, through haptic vibrations, to an intimate and non-visible dimension of the musicians' bodily experience.

There are three steps to get MappEMG up and running:
First, connect the acquisition device (Bitalino or Delsys) to your local machine. Then, initiate the server, responsible for constantly acquiring data from the sensor device, processing it, and streaming it to either a client or an MVC trial. Finally, initiate a client connection to the server. The client will post-process the EMG data and emit it to the Happtics IOS mobile app.

For more information on the project, check out [this](https://nime.pubpub.org/pub/kmn0rbyp/release/1) paper!
<!-- The processing pipeline is based on [Emg2haptics](https://github.com/Fiverdug/Emg2haptics) maxMSP code, which has been translated into python.  -->

# Table of Contents  

[How to install](#how-to-install)
 - [The dependencies with Anaconda](#from-conda-forge)
 - [The dependencies with pip](#from-pip)
 - [The setup](#installation)

[How to run](#how-to-run)
- [Running the server](#running-the-server)
- [Running an MVC trial](#running-an-mvc-trial)
- [Show the results](#show-the-results)

[Citing](#Citing)

# How to install 
`MappEMG` relies on several dependencies. If you do not want to install everything seperatly, run the installation script using the command
```bash
source installation.sh
```
You will be prone to say if you already have a virtual environment you would like to use. If you do, press `y` and simply enter its name. If you do not, just press `n` (your new venv will be called `mappemg_venv`)

If you are running into issues or want to install everything yourself, refer to the sub-sections [below](#from-conda-forge)

## From Conda Forge
```bash
conda install -cconda-forge pyqtgraph 
```

## From Pip
```bash
pip install PyQt5 python-osc
pip install scipy
pip install numpy
pip install typing
pip install python-osc
pip install matplotlib
pip install bitalino
pip install pandas
```

## Installation

Once you have downloaded `biosiglive`, navigate to the root folder and (assuming your environment is loaded if needed), you can type the following command:
```bash 
python setup.py install
```
Assuming everything went well, that is it! 
You can already enjoy MappEMGing!


<!-- ### Dependencies
`MappEmg` relies on several libraries. 
The most obvious one is the `biorbd` suite (including indeed `biorbd` and `bioviz`), but some extra more are required.
Due to the amount of different dependencies, it would be tedious to show how to install them all here. 
The user is therefore invited to read the relevant documentations. 

Here is a list of all direct dependencies (meaning that some dependencies may require other libraries themselves):
- [Python](https://www.python.org/)
- [numpy](https://numpy.org/)
- [scipy](https://scipy.org/)
- [packaging](https://packaging.python.org/)
- [setuptools](https://pypi.org/project/setuptools/)
- [matplotlib](https://matplotlib.org/)
- [pandas](https://pandas.pydata.org/)
- [pyomeca](https://github.com/pyomeca/pyomeca)
- [CasADi](https://web.casadi.org/)
- [rbdl-casadi](https://github.com/pyomeca/rbdl-casadi) compiled with the CasADi backend
- [tinyxml](http://www.grinninglizard.com/tinyxmldocs/index.html)
- [biorbd](https://github.com/pyomeca/biorbd)
- [vtk](https://vtk.org/)
- [PyQt](https://www.riverbankcomputing.com/software/pyqt)
- [bioviz](https://github.com/pyomeca/bioviz)
- [graphviz](https://graphviz.org/)
- [`Ipopt`](https://github.com/coin-or/Ipopt)
- [`Acados`](https://github.com/acados/acados)
- [pyqtgraph](https://www.pyqtgraph.org/)

and optionally:
- [The linear solvers from the HSL Mathematical Software Library](http://www.hsl.rl.ac.uk/index.html) -->


# How to run
This is a section dedicated on how to properly run the program. There are two parts, running the server in order to acquire data from the device, and running the client to stream data from the server and convert it into haptics.
For all of these steps, make sure you are in your virtual environment!

## Running the server

To run the server, simply run the file `server.py` in the MappEMG directory. 
You will then have a little menu that will resemble the following:

``` bash
Client will connect to server on IP:'localhost' and PORT:'5005'
        To change IP -- Press 1 and 'Enter'
        To change PORT -- Press 2 and 'Enter'
        To continue -- Leave empty and press 'Enter': 
``` 
These are the parameters on which you would like to host the server. Follow the instructions if you would like to change the parameters. If you would like to continue press Enter.

The next question is:
``` bash
>> With device connected? (y, or n for random data): 
```
Answer `y` if you would like to connect a device (such as a Bitalino or Delsys), or `n` if you would just like to use randomly generated data

``` bash
>> Enter list of acquisition channels (e.g. for A1 A2 A3, write 1 2 3): 
```
Answer which acquisition channels you are using. On the Bitalino device, you can check at the back of the device next to the port, it is written there in small. For Delsys, they correspond to the sensor management menu numbers, not the number of the sensor from the box. 
Reply according to the number of sensors you are using of course.

``` bash
>> Plot data in real-time? (y or n): 
```
If you would like to plot your data real-time, you can select that option by pressing `y`


The prompt should then show:

``` bash
Starting Server...

Starting EMG Processing...
Starting Sensor Acquisition...
Starting Streaming...
```

The server is now running and continuously acquiring data


## Running an MVC trial

To run an MVC trial, the server should be running. So if that is not the case, please refer to the section [above](#running-the-server).

To start the trial, while the server is running, open another terminal and run `MVC_trial.py` in the MappEMG directory. Note that if you are using VS code you should run it with the "run without debugging" option from the above menu.

Once `MVC_trial.py` is running, you should answer the questions from the prompt:

``` bash
>> Do MVC with real data from server? (y, or n for random data): 
```
Answer `y` if you would like to use the data acquired by the server or `n` for randomly generated data.

``` bash
>> How many muscles will be used (e.g. for 2 muscles, write 2): 
```
Answer the number of muscles you are currently measuring the contractions for. That corresponds to the number of channels used.

``` bash
>> Give a name to muscle #1:  
```
Answer the name you would like to give to your muscle. Try to be as descriptive as possible. If you are targetting more than one muscle, you will have to name those too.

``` bash
>> Please enter a name of your trial (string) then press enter or press enter.
```
Answer the name you would like to give to the trial. If you do not wish to name it, simply press enter.

Then you should get a message confirming the trial you would like to run

``` bash
>> Ready to start trial: <trial_name>, with muscles :[<muscle_1>, <muscle_2>]. Press enter to begin your MVC. or enter a number of seconds
```
Either start it directly or enter the number of seconds the MVC trial will take, and do not forget to contract as much as you can to get the maximum value of contraction!

The questions you will get after are really straightforward, they are there if you would like to plot your trial. Simply follow the instructions in the prompt.

## Running the client

In order to start processing your EMG data, you should start running a client. To do so, firstly make sure that the server is running. To accomplish that you can refer to [this](#running-the-server) part of the read me.
Once the server is running, you should run the `client.py` file, which is under the MappEMG directory. Run it in a new terminal. Note that if you are using VS code you should run it with the "run without debugging" option from the above menu.

Once `client.py` is running, you should answer the questions from the prompt:

``` bash
Client will connect to server on IP:'localhost' and PORT:'5005'
        To change IP -- Press 1 and 'Enter'
        To change PORT -- Press 2 and 'Enter'
        To continue -- Leave empty and press 'Enter': 
```
These are the parameters on which you would like to host the client. Follow the instructions if you would like to change those. If you would like to continue press Enter.

``` bash
>> Do you want to load real MVC values? ('y' or 'n' for random): 
```
Press `y` if you would like to load real MVC value you have collected earlier on (to do that check out [this](#running-an-mvc-trial) section). If you would like to load random values then press `n`.

If you clicked on `n` skip this part, if you clicked on `y` you will be prompted to answer:
``` bash
>> Input name of the MVC .csv file (for example "MVC_20220707-1915.csv"): 
```
where you simply should imput the name of the MVC file you collected earlier on. For example "MVC_20220707-1915.csv".

Then you will be asked if you would like to connect a device to the pipeline. This can only work if you have the haptics app installed. NOTE: YOUR HOST AND DEVICES SHOULD BE CONNECTED TO THE SAME WIFI
``` bash
>> How many devices with the haptics app would you like to connect? 
```
Answer 0 if you do not want to connect a device, or any positive integer for the number of devices you would like to connect. 

``` bash
>> IP of device number 1 (e.g: XXX.XXX.X.X):
``` 
Enter the IP of your device (which you can find at the top of the haptics app or in your wifi settings).

``` bash
>> PORT of device number 1 (e.g: 2222):
```
Enter the port of your device (which you can find at the top of the haptics app or in your wifi settings).

``` bash
>> Attribute weights between 0 and 1 to each sensor (e.g for A1 A2 A3, write 0.45 1 0):
```
Here is a way to visualize what the weights refer to, it is simply a way to compute a weighted mean for each of the acquisition channels:
![alt text](https://github.com/karlmiko/biosiglive/blob/main/images/emg_weights.png)

Meaning each EMG sensor you have connected can have a weight attributed to it. Weight 1 is 100% of the weight, while 0 is none.

That's it! Your devices should start vibrating. If it is not the case you might have to restart your haptics app and the client!

To stop the client, press `^C` in the terminal in which it is running


# Citing
If you use `MappEMG`, we would be grateful if you could cite this paper: https://nime.pubpub.org/pub/kmn0rbyp/release/1?readingCollection=bb45043c
