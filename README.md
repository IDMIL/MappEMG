<!-- <p align="center">
    <img
      src="https://github.com/karlmiko/biosiglive/tree/refactor/MappEmg_pipeline"
      alt="logo"
    />
</p> -->

![alt text](https://github.com/karlmiko/biosiglive/blob/refactor/MappEMG/MappEmg_pipeline.png?raw=trueg)

`MapEMG` allows the audience to experience the performer’s muscle effort, an essential
component of music performance which is typically unavailable to direct visual
observation. The goal is thus to give the listeners access, through haptic vibrations, to an intimate and non-visible dimension of the musicians’ bodily experience.
The project is organized in the following way: 
Firstly connect your acquisition device to your local machine (can be either Bitalino or Delsys). Then you can run the server which is going to constantly process the data acquired by the sensors and stream it to either a client or an MVC trial. 
The client side will take care of post-processing the emg data, such as normalization using MVC values, mapping the emg values to haptics, and emit this data to the happtics mobile app.

For more information on the project, check out [this]() paper! NOTE TO FELIPE : is there a paper or references I could link here? I only have pdfs...
<!-- The processing pipeline is based on [Emg2haptics](https://github.com/Fiverdug/Emg2haptics) maxMSP code, which has been translated into python.  -->

<!-- ## Status

| Type | Status |
|---|---|
| License | <a href="https://opensource.org/licenses/MIT"><img src="https://img.shields.io/badge/license-MIT-success" alt="License"/></a> |
| Continuous integration | [![Build status](https://ci.appveyor.com/api/projects/status/om07r8jhng61qx7y/branch/master?svg=true)](https://ci.appveyor.com/project/pariterre/bioptim/branch/master) |
| Code coverage | [![codecov](https://codecov.io/gh/pyomeca/bioptim/branch/master/graph/badge.svg?token=NK1V6QE2CK)](https://codecov.io/gh/pyomeca/bioptim) |
| DOI | [![DOI](https://zenodo.org/badge/251615517.svg)](https://zenodo.org/badge/latestdoi/251615517) |

The current status of `bioptim` on conda-forge is

| Name | Downloads | Version | Platforms | MyBinder |
| --- | --- | --- | --- | --- |
| [![Conda Recipe](https://img.shields.io/badge/recipe-bioptim-green.svg)](https://anaconda.org/conda-forge/bioptim) | [![Conda Downloads](https://img.shields.io/conda/dn/conda-forge/bioptim.svg)](https://anaconda.org/conda-forge/bioptim) | [![Conda Version](https://img.shields.io/conda/vn/conda-forge/bioptim.svg)](https://anaconda.org/conda-forge/bioptim) | [![Conda Platforms](https://img.shields.io/conda/pn/conda-forge/bioptim.svg)](https://anaconda.org/conda-forge/bioptim) | [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/pyomeca/bioptim-tutorial/HEAD?urlpath=lab) | -->

<!-- # Try bioptim
Anyone can play with bioptim with a working (but slightly limited in terms of graphics) MyBinder by clicking the following badge

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/pyomeca/bioptim-tutorial/HEAD?urlpath=lab)

As a tour guide that uses this binder, you can watch the `bioptim` workshop that we gave at the CMBBE conference on September 2021 by following this link:
[https://youtu.be/z7fhKoW1y60](https://youtu.be/z7fhKoW1y60) -->

# Table of Contents  
<!-- [Testing bioptim](#try-bioptim) -->

[How to install](#how-to-install)
 - [The dependencies with Anaconda](#from-conda-forge)
 - [The dependencies with pip](#from-pip)
 - [The setup](#installation)

[How to run](#how-to-run)
- [Running the server](#running-the-server)
- [Running an MVC trial](#running-an-mvc-trial)
- [Show the results](#show-the-results)

[Citing](#Citing)

        
<!-- [Examples](#examples)
- [Run examples](#run-examples)
- [Getting started](#getting-started)
- [Muscle driven OCP](#muscle-driven-ocp)
- [Muscle driven with contact](#muscle-driven-with-contact)
- [Optimal time OCP](#optimal-time-ocp)
- [Symmetrical torque driven OCP](#symmetrical-torque-driven-ocp)
- [Torque driven OCP](#torque-driven-ocp)
- [Track](#track)
- [Moving estimation horizon](#moving-estimation-horizon)
- [Acados](#acados)
 -->


# How to install 
`MapEmg` relies on several libraries. The most obvious one is the `pyqt` suite. You can install them by running the following commands :

Note that there are some extra required. Due to the amount of different dependencies, it would be tedious to show how to install them all here. The user is therefore invited to read the relevant documentations.

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
You can already enjoy bioptimizing!


<!-- ### Dependencies
`MapEmg` relies on several libraries. 
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
This is a section dedicated to show how to properly run the program. We recommend using VS code as a visual interface as the details to come will be based on it.

## Running the server

To run the server, simply run the file `open_server.py` in the examples directory. 
The best way to do this is via the execute window in the top menu, and click `execute without debugging`.
You will then have to answer some questions in the prompt which are the following:

``` bash
>> With device connected? (y, or n for random data): 
```
Answer `y` if you would like to connect a device (such as a Bitalino or Delsys), or `n` if you would just like to use randomly generated data

``` bash
>> Enter list of acquisition channels (e.g. for A1 A2 A3, write 1 2 3): 
```
Answer which acquisition channels you are using on the Bitalino device (you can check at the back of the device next to the port, it is written in small). Reply according to the number of sensors you are using of course.

``` bash
>> Enter sampling rate (1, 10, 100, or 1000): 
```
Answer one of the following options. For Bitalino, 1000Hz is recommended.

The prompt should then show:

``` bash
Start streaming...
```

The server is now running and continuously acquiring data


## Running an MVC trial

To run an MVC trial, the server should be running. So if that is not the case, please refer to the section [above](#running-the-server).

To start the trial, while the server is running, run `compute_mvc.py` in the examples directory by going in the above menu -> execute -> execute without debugging. VS code will ask you a question to which you should answer `yes` in order to run both `open_server.py` and `compute_mvc.py` simultaniously.

Once `compute_mvc.py` is running, you should answer the questions from the prompt:

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

## Running the client

In order to start processing your EMG data, you should start running a client. To do so, firtly make sure that the server is running. To accomplish that you can refer to [this](#running-the-server) part of the read me.
Once the server is running, you should run the `stream_data_from_server.py` file, which is under the examples directory. To run it, you should use the execute menu from the top bar and select menu -> execute -> execute without debugging. You will be prompted to answer `yes` to VScode's question on the screen.

Once `stream_data_from_server.py` is running, you should answer the questions from the prompt:

``` bash
>> Connect to host address (leave empty for "localhost"): 
```
Answer the address on which you are hosting the server, if it is locally, press enter and it will automatically be 'localhost', meaning the IP address 127.0.0.1. If you are hosting the server on a different machine, input that new IP address.

``` bash
>> Connect to host port (leave empty for "5005"): 
```
If you are hosting the server locally, press enter and it will automatically set the host port to 5005. If you are hosting on a different machine, enter its port.

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
These correspond to the following weights in the controller portion:
![alt text](https://github.com/karlmiko/biosiglive/blob/refactor/MappEMG/emg_weights.png?raw=true)

Meaning each EMG sensor you have connected can have a weight attributed to it. Weight 1 is 100% of the weight, while 0 is none.

That's it! Your devices should start vibrating. If it is not the case you might have to restart your haptics app and the client!


# Citing
If you use `biosiglive`, we would be grateful if you could cite it as follows:
NOTE TO KARL & FELIPE: gotta change this, lmk what ref we should use
@article {Bioptim2021,
	author = {Michaud, Benjamin and Bailly, Fran{\c c}ois and Charbonneau, Eve and Ceglia, Amedeo and Sanchez, L{\'e}a and Begon, Mickael},
	title = {Bioptim, a Python framework for Musculoskeletal Optimal Control in Biomechanics},
	elocation-id = {2021.02.27.432868},
	year = {2021},
	doi = {10.1101/2021.02.27.432868},
	publisher = {Cold Spring Harbor Laboratory},
	URL = {https://www.biorxiv.org/content/10.1101/2021.02.27.432868v1},
	eprint = {https://www.biorxiv.org/content/10.1101/2021.02.27.432868v1.full.pdf},
	journal = {bioRxiv}
}
