<p align="center">
    <img
      src="https://github.com/karlmiko/biosiglive/tree/refactor/MappEmg_pipeline"
      alt="logo"
    />
</p>

`MapEMG` allows the audience to experience the performer’s muscle effort, an essential
component of music performance which is typically unavailable to direct visual
observation. The goal is thus to give the listeners access, through haptic vibrations, to an intimate and non-visible dimension of the musicians’ bodily experience.
The processing pipeline is based on [Emg2haptics](https://github.com/Fiverdug/Emg2haptics) maxMSP code, which has been translated into python. 

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
- [Solving the ocp](#solving-the-ocp)
- [Show the results](#show-the-results)
- [The full example files](#the-full-example-files)

        
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

[Citing](#Citing) -->


# How to install 
`MapEmg` relies on several libraries. The most obvious one is the `pyqt` suite. You can intall them by running the folowing commands :

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
Do MVC with real data from server? (y, or n for random data): 
```
Answer `y` if you would like to use the data acquired by the server or `n` for randomly generated data.

``` bash
How many muscles will be used (e.g. for 2 muscles, write 2): 
```
Answer the number of muscles you are currently measuring the contractions for. That corresponds to the number of channels used.

``` bash
Give a name to muscle #1:  
```
Answer the name you would like to give to your muscle. Try to be as descriptive as possible. If you are targetting more than one muscle, you will have to name those too.

``` bash
Please enter a name of your trial (string) then press enter or press enter.
```
Answer the name you would like to give to the trial. If you do not wish to name it, simply press enter.

Then you should get a message confirming the trial you would like to run

``` bash
Ready to start trial: <trial_name>, with muscles :[<muscle_1>, <muscle_2>]. Press enter to begin your MVC. or enter a number of seconds
```
Either start it directly or enter the number of seconds the MVC trial will take, and do not forget to contract as much as you can to get the maximum value of contraction!

## Solving the ocp
It is now time to see `Ipopt` in action! 
To solve the ocp, you simply have to call the `solve()` method of the `ocp` class
```python
solver = Solver.IPOPT(show_online_optim=True)
sol = ocp.solve(solver)
```
If you feel fancy, you can even activate the online optimization graphs!
However, for such an easy problem, `Ipopt` won't leave you the time to appreciate the realtime updates of the graph...
For a more complicated problem, you may also wish to visualize the objectives and constraints during the optimization 
(useful when debugging, because who codes the right thing the first time). You can do it by calling
```python
ocp.add_plot_penalty(CostType.OBJECTIVES)
ocp.add_plot_penalty(CostType.CONSTRAINTS)
```
or alternatively asks for both at once using
```python
ocp.add_plot_penalty(CostType.ALL)
```
That's it!

## Show the results
If you want to have a look at the animated data, `bioptim` has an interface to `bioviz` which is designed to visualize bioMod files.
For that, simply call the `animate()` method of the solution:
```python
sol.animate()
```

If you did not fancy the online graphs, but would enjoy them anyway, you can call the method `graphs()`:
```python
sol.graphs()
```

If you are interested in the results of individual objective functions and constraints, you can print them using the 
`print_cost()` or access them using the `detailed_cost_values()`:
```python
sol.print_cost()  # For printing their values in the console
sol.detailed_cost_values()  # For adding the objectives details to sol for later manipulations
```

And that is all! 
You have completed your first optimal control program with `bioptim`! 

## The full example files
If you did not completely follow (or were too lazy to!) you will find in this section the complete files described in the Getting started section.
You will find that the file is a bit different from the `example/getting_started/pendulum.py`, but it is merely differences on the surface.

### The pendulum.py file
```python
import biorbd_casadi as biorbd
from bioptim import (
    OptimalControlProgram,
    DynamicsFcn,
    Dynamics,
    Bounds,
    QAndQDotBounds,
    InitialGuess,
    ObjectiveFcn,
    Objective,
)

biorbd_model = biorbd.Model("pendulum.bioMod")
dynamics = Dynamics(DynamicsFcn.TORQUE_DRIVEN)
x_bounds = QAndQDotBounds(biorbd_model)
x_bounds[:, [0, -1]] = 0
x_bounds[1, -1] = 3.14
u_bounds = Bounds([-100, 0], [100, 0])
objective_functions = Objective(ObjectiveFcn.Lagrange.MINIMIZE_TORQUE)
x_init = InitialGuess([0, 0, 0, 0])
u_init = InitialGuess([0, 0])

ocp = OptimalControlProgram(
        biorbd_model,
        dynamics,
        n_shooting=25,
        phase_time=3,
        x_init=x_init,
        u_init=u_init,
        x_bounds=x_bounds,
        u_bounds=u_bounds,
        objective_functions=objective_functions,
    )
    
sol = ocp.solve(show_online_optim=True)
sol.print_cost()
sol.animate()
```
### The pendulum.bioMod file
Here is a simple pendulum that can be interpreted by `biorbd`. 
For more information on how to build a bioMod file, one can read the doc of [biorbd](https://github.com/pyomeca/biorbd).

```c
version 4

// Seg1
segment Seg1
    translations	y
    rotations	x
    ranges  -1 5
            -2*pi 2*pi
    mass 1
    inertia
        1 0 0
        0 1 0
        0 0 0.1
    com 0.1 0.1 -1
    mesh 0.0   0.0   0.0
    mesh 0.0  -0.0  -0.9
    mesh 0.0   0.0   0.0
    mesh 0.0   0.2  -0.9
    mesh 0.0   0.0   0.0
    mesh 0.2   0.2  -0.9
    mesh 0.0   0.0   0.0
    mesh 0.2   0.0  -0.9
    mesh 0.0   0.0   0.0
    mesh 0.0  -0.0  -1.1
    mesh 0.0   0.2  -1.1
    mesh 0.0   0.2  -0.9
    mesh 0.0  -0.0  -0.9
    mesh 0.0  -0.0  -1.1
    mesh 0.2  -0.0  -1.1
    mesh 0.2   0.2  -1.1
    mesh 0.0   0.2  -1.1
    mesh 0.2   0.2  -1.1
    mesh 0.2   0.2  -0.9
    mesh 0.0   0.2  -0.9
    mesh 0.2   0.2  -0.9
    mesh 0.2  -0.0  -0.9
    mesh 0.0  -0.0  -0.9
    mesh 0.2  -0.0  -0.9
    mesh 0.2  -0.0  -1.1
endsegment

    // Marker 1
    marker marker_1
        parent Seg1
        position 0 0 0
    endmarker

    // Marker 2
    marker marker_2
        parent Seg1
        position 0.1 0.1 -1
    endmarker
```

# Examples
In this section, you will find the description of all the examples implemented with bioptim. They are ordered in 
separate files. Each subsection corresponds to the different files, dealing with different examples and topics.
Please note that the examples from the paper (see [Citing](#citing)) can be found in this repo
[https://github.com/s2mLab/BioptimPaperExamples](https://github.com/s2mLab/BioptimPaperExamples).

## Run examples
An GUI to access the examples can be run to facilitate the testing of bioptim
You can either run the file `__main__.py` in the `examples` folder or execute the following command.
```bash
python -m bioptim.examples
```
Please note that `pyqtgraph` must be installed to run this GUI. 

## Getting started
In this subsection, all the examples of the getting_started file are described.

### The custom_bounds.py file
This example is a trivial box sent upward. It is designed to investigate the different
bounds one can define in bioptim.
Therefore, it shows how one can define the bounds, that is the minimal and maximal values
of the state and control variables.

All the types of interpolation are shown : `CONSTANT`, `CONSTANT_WITH_FIRST_AND_LAST_DIFFERENT`, `LINEAR`, `EACH_FRAME`,
`SPLINE`, and `CUSTOM`. 

When the `CUSTOM` interpolation is chosen, the functions `custom_x_bounds_min` and `custom_x_bounds_max` are used to 
provide custom x bounds. The functions `custom_u_bounds_min` and `custom_u_bounds_max` are used to provide custom 
u bounds. 
In this particular example, one mimics linear interpolation using these four functions.

### The custom_constraints.py file
This example is a trivial box that must superimpose one of its corner to a marker at the beginning of the movement
and superimpose the same corner to a different marker at the end.
It is designed to show how one can define its own custom constraints function if the provided ones are not
sufficient.

More specifically this example reproduces the behavior of the `SUPERIMPOSE_MARKERS` constraint.

### The custom_dynamics.py file
This example is a trivial box that must superimpose one of its corner to a marker at the beginning of the movement
and superimpose the same corner to a different marker at the end.
It is designed to show how one can define its own custom dynamics function if the provided ones are not
sufficient.

More specifically this example reproduces the behavior of the `DynamicsFcn.TORQUE_DRIVEN` using a custom dynamics. 

The custom_dynamic function is used to provide the derivative of the states. The custom_configure function is used 
to tell the program which variables are states and controls. 

### The custom_initial_guess.py file
This example is a trivial box that must superimpose one of its corner to a marker at the beginning of the movement
and superimpose the same corner to a different marker at the end.
It is designed to investigate the different way to define the initial guesses at each node sent to the solver.

All the types of interpolation are shown : `CONSTANT`, `CONSTANT_WITH_FIRST_AND_LAST_DIFFERENT`, `LINEAR`, `EACH_FRAME`,
`SPLINE`, and `CUSTOM`. 

When the CUSTOM interpolation is chosen, the `custom_init_func` function is used to custom the initial guesses of the 
states and controls. In this particular example, one mimics linear interpolation. 

### The custom_objectives.py file
This example is a trivial box that tries to superimpose one of its corner to a marker at the beginning of the movement
and superimpose the same corner to a different marker at the end.
It is designed to show how one can define its own custom objective function if the provided ones are not
sufficient.

More specifically this example reproduces the behavior of the `Mayer.SUPERIMPOSE_MARKERS` objective function. 

This example is closed to the example of the custom_constraint.py file. We use the custom_func_track_markers to define 
the objective function. In this example, one mimics the `ObjectiveFcn.SUPERIMPOSE_MARKERS`.

### The custom_parameters.py file 
This example is a clone of the pendulum.py example with the difference that the
model now evolves in an environment where the gravity can be modified.
The goal of the solver it to find the optimal gravity (target = 8 N/kg), while performing the
pendulum balancing task.

It is designed to show how one can define its own parameter objective functions if the provided ones are not
sufficient.

The `my_parameter_function function` is used if one wants to modify the dynamics. In our case, we want to optimize the 
gravity. This function is called right before defining the dynamics of the system. The `my_target_function` function is 
a penalty function. Both these functions are used to define a new parameter, and then a parameter objective function 
linked to this new parameter.

### The custom_phase_transitions.py file 
This example is a trivial multiphase box that must superimpose different markers at beginning and end of each
phase with one of its corner
It is designed to show how one can define its phase transition constraints if the provided ones are not sufficient.

More specifically, this example mimics the behaviour of the most common `PhaseTransitionFcn.CONTINUOUS`

The custom_phase_transition function is used to define the constraint of the transition to apply. This function can be 
used when adding some phase transitions in the list of phase transitions. 

Different phase transisitions can be considered. By default, all the phase transitions are continuous. However, in the 
event that one or more phase transitions is desired to be continuous, it is posible to define and use a function like 
the `custom_phase_transition` function, or directly use `PhaseTransitionFcn.IMPACT`. If a phase transition is desired 
between the last and the first phase, use the dedicated `PhaseTransitionFcn.Cyclic`. 

### The custom_plot_callback.py file
This example is a trivial example using the pendulum without any objective. It is designed to show how to create new
plots and how to expand pre-existing one with new information.

We define the `custom_plot_callback` function, which returns the value(s) to plot. We use this function as an argument of 
`ocp.add_plot`. Let's describe the creation of the plot "My New Extra Plot". `custom_plot_callback` 
takes two arguments, x and the array [0, 1, 3], as you can see below :

```python
ocp.add_plot("My New Extra Plot", lambda x, u, p: custom_plot_callback(x, [0, 1, 3]), plot_type=PlotType.PLOT)
```

We use the plot_type `PlotType.PLOT`. This is a way to plot the first, 
second, and fourth states (ie. `q_Seg1_TransY`, `q_Seg1_RotX` and `qdot_Seg1_RotX`) in a new window entitled "My New 
Extra Plot". Please note that for further information about the different plot types, you can refer to the section 
"Enum: PlotType".

### The example_cyclic_movement.py file 
This example is a trivial box that must superimpose one of its corner to a marker at the beginning of the movement
and superimpose the same corner to a different marker at the end. Moreover, the movement must be cyclic, meaning
that the states at the end and at the beginning are equal. It is designed to provide a comprehensible example of the way
to declare a cyclic constraint or objective function

A phase transition loop constraint is treated as hard penalty (constraint)
if weight is <= 0 [or if no weight is provided], or as a soft penalty (objective) otherwise, as shown in the example below :

```python
phase_transitions = PhaseTransitionList()
if loop_from_constraint:
    phase_transitions.add(PhaseTransitionFcn.CYCLIC, weight=0)
else:
    phase_transitions.add(PhaseTransitionFcn.CYCLIC, weight=10000)
```

`loop_from_constraint` is a boolean. It is one of the parameters of the `prepare_ocp` function of the example. This parameter is a way to determine if the looping cost should be a constraint [True] or an objective [False]. 

### The example_external_forces.py file
This example is a trivial box that must superimpose one of its corner to a marker at the beginning of the movement
and superimpose the same corner to a different marker at the end. While doing so, a force pushes the box upward.
The solver must minimize the force needed to lift the box while reaching the marker in time.
It is designed to show how to use external forces. An example of external forces that depends on the state (for
example a spring) can be found at 'examples/torque_driven_ocp/spring_load.py'

Please note that the point of application of the external forces are defined in the `bioMod` file by the
`externalforceindex` tag in segment and is acting at the center of mass of this particular segment. Please note that
this segment must have at least one degree of freedom defined (translations and/or rotations). Otherwise, the
external_force is silently ignored. 

`Bioptim` expects `external_forces` to be a list (one element for each phase) of
np.array of shape (6, i, n), where the 6 components are [Mx, My, Mz, Fx, Fy, Fz], for the ith force platform
(defined by the `externalforceindex`) for each node n. Let's take a look at the definition of the external forces in 
this example :

```python
external_forces = [
    np.repeat(np.array([[0, 0, 0, 0, 0, -2], [0, 0, 0, 0, 0, 5]]).T[:, :, np.newaxis], n_shooting, axis=2)]
```

`external_forces` is of len 1 because there is only one phase. The array inside it is 6x2x30 since there 
is [Mx, My, Mz, Fx, Fy, Fz] for the two `externalforceindex` for each node (in this example, we take 30 shooting nodes).

### The example_inequality_constraint.py file
This example mimics by essence what a jumper does which is maximizing the predicted height of the
center of mass at the peak of an aerial phase. It does so with a very simple two segments model though.
It is a clone of 'torque_driven_ocp/maximize_predicted_height_CoM.py' using
the option `MINIMIZE_PREDICTED_COM_HEIGHT`. It is different in the sense that the contact forces on ground have
to be downward (meaning that the object is limited to push on the ground, as one would expect when jumping, for
instance). 

Moreover, the lateral forces must respect some `NON_SLIPPING` constraint (that is the ground reaction
forces have to remain inside of the cone of friction), as shown in the part of the code defining the constrainst:

```python
constraints = ConstraintList()
   constraints.add(
   ConstraintFcn.CONTACT_FORCE,
   min_bound=min_bound,
   max_bound=max_bound,
   node=Node.ALL,
   contact_force_idx=1,
   )
constraints.add(
    ConstraintFcn.CONTACT_FORCE,
    min_bound=min_bound,
    max_bound=max_bound,
    node=Node.ALL,
    contact_force_idx=2,
    )
constraints.add(
    ConstraintFcn.NON_SLIPPING,
    node=Node.ALL,
    normal_component_idx=(1, 2),
    tangential_component_idx=0,
    static_friction_coefficient=mu,
    )
```

Let's describe the code above. First, we create a list of consraints. Then, two contact forces are defined, 
respectively with the indexes 1 and 2. The last step is the implementation of the 
non slipping constraint for the two forces defined before.   

This example is designed to show how to use min_bound and max_bound values so they define inequality constraints instead
of equality constraints, which can be used with any `ConstraintFcn`.

### The example_mapping.py file 
An example of mapping can be found at 'examples/symmetrical_torque_driven_ocp/symmetry_by_mapping.py'.
Another example of mapping can be found at 'examples/getting_started/example_inequality_constraint.py'. 

### The example_multiphase.py file
This example is a trivial box that must superimpose one of its corner to a marker at the beginning of the movement and
a the at different marker at the end of each phase. Moreover a constraint on the rotation is imposed on the cube.
It is designed to show how one can define a multiphase optimal control program.

In this example, three phases are implemented. The `long_optim` boolean allows users to choose between solving the precise
optimization or the approximate. In the first case, 500 points are considered and `n_shooting = (100, 300, 100)`. 
Otherwise, 50 points are considered and `n_shooting = (20, 30, 20)`. Three steps are necessary to define the 
objective functions, the dynamics, the constraints, the path constraints, the initial guesses and the control path 
contsraints. Each step corresponds to one phase. 

Let's take a look at the definition of the constraints:

```python
constraints = ConstraintList()
constraints.add(
    ConstraintFcn.SUPERIMPOSE_MARKERS, node=Node.START, first_marker_idx=0, second_marker_idx=1, phase=0
)
constraints.add(ConstraintFcn.SUPERIMPOSE_MARKERS, node=Node.END, first_marker_idx=0, second_marker_idx=2, phase=0)
constraints.add(ConstraintFcn.SUPERIMPOSE_MARKERS, node=Node.END, first_marker_idx=0, second_marker_idx=1, phase=1)
constraints.add(ConstraintFcn.SUPERIMPOSE_MARKERS, node=Node.END, first_marker_idx=0, second_marker_idx=2, phase=2)
```

First, we define a list of constraints, and then we add constraints to the list. At the beginning, marker 0 must 
superimpose marker 1. At the end of the first phase (the first 100 shooting nodes if we solve the precise optimization), 
marker 0 must superimpose marker 2. Then, at the end of the second phase, marker 0 must superimpose marker 1. At the 
end of the last step, marker 0 must superimpose marker 2. Please, note that the definition of the markers is 
implemented in the `bioMod` file corresponding to the model. Further information about the definition of the markers is
available in the `biorbd` documentation.

### The example_optimal_time.py file
Examples of time optimization can be found in 'examples/optimal_time_ocp/'.

### The example_save_and_load.py file
This is a clone of the getting_started/pendulum.py example. It is designed to show how to create and solve a problem,
and afterward, save it to the hard drive and reload it. It shows an example of *.bo method. 

Let's take a look at the most important lines of the example. To save the optimal control program and the solution, use
ocp.save(sol, "pendulum.bo"). To load the optimal control program and the solution, use 
`ocp_load, sol_load = OptimalControlProgram.load("pendulum.bo")`. Then, to show the results, 
simply use `sol_load.animate()`.

### The example_simulation.py file
The first part of this example of a single shooting simulation from initial guesses.
It is not an optimal control program. It is merely the simulation of values, that is applying the dynamics.
The main goal of this kind of simulation is to get a sens of the initial guesses passed to the solver.

The second part of the example is to actually solve the program and then simulate the results from this solution.
The main goal of this kind of simulation, especially in single shooting (that is not resetting the states at each node)
is to validate the dynamics of multiple shooting. If they both are equal, it usually means that a great confidence
can be held in the solution. Another goal would be to reload fast a previously saved optimized solution.

### The pendulum.py file
This is another way to present the pendulum example of the 'Getting started' section. 

## Muscle driven OCP
In this file, you will find four examples about muscle driven optimal control programs. The two first refer to traking 
examples. The two last refer to reaching tasks. 

### The muscle_activations_tracker.py file
This is an example of muscle activation/skin marker or state tracking.
Random data are created by generating a random set of muscle activations and then by generating the kinematics
associated with these data. The solution is trivial since no noise is applied to the data. Still, it is a relevant
example to show how to track data using a musculoskeletal model. In real situation, the muscle activation
and kinematics would indeed be acquired via data acquisition devices.

The difference between muscle activation and excitation is that the latter is the derivative of the former.

The generate_data function is used to create random data. First, a random set of muscle activation is generated, as 
shown below:
`U = np.random.rand(n_shooting, n_mus).T`

Then, the kinematics associated with these data are generated by numerical integration, using 
`scipy.integrate.solve_ivp`. 

To implement this tracking task, we use the ObjectiveFcn.Lagrange.TRACK_STATE objective function in the case of a state 
tracking, or the `ObjectiveFcn.Lagrange.TRACK_MARKERS` objective function in the case of a marker tracking. We also use 
the `ObjectiveFcn.Lagrange.TRACK_MUSCLES_CONTROL` objective function. The user can choose between marker or state 
tracking thanks to the string `kin_data_to_track` which is one of the `prepare_ocp` function parameters. 

### The muscle_excitations_tracker.py file
This is an example of muscle excitation(EMG)/skin marker or state tracking.
Random data are created by generating a random set of EMG and then by generating the kinematics associated with these
data. The solution is trivial since no noise is applied to the data. Still, it is a relevant example to show how to
track data using a musculoskeletal model. In real world, the EMG and kinematics would indeed be acquired via
data acquisition devices.

There is no huge difference with the precedent example. Some dynamic equations make the link between muscle activation
and excitation. 

### The static_arm.py file
This is a basic example on how to use `biorbd` model driven by muscle to perform an optimal reaching task.
The arms must reach a marker placed upward in front while minimizing the muscles activity.

For this reaching task, we use the `ObjectiveFcn.Mayer.SUPERIMPOSE_MARKERS` objective function. At the end of the 
movement, marker 0 and marker 5 should superimpose. The weight applied to the `SUPERIMPOSE_MARKERS` objective function 
is 1000. Please note that the bigger this number, the greater the model will try to reach the marker. 

Please note that using show_meshes=True in the animator may be long due to the creation of a huge `CasADi` graph of the
mesh points.

### The static_arm_with_contact.py file
This is a basic example on how to use biorbd model driven by muscle to perform an optimal reaching task with a
contact dynamics.
The arms must reach a marker placed upward in front while minimizing the muscles activity.

The only difference with the precedent example is that we use the arm26_with_contact.bioMod model and the 
`DynamicsFcn.MUSCLE_ACTIVATIONS_AND_TORQUE_DRIVEN_WITH_CONTACT` dynamics function instead of 
`DynamicsFcn.MUSCLE_ACTIVATIONS_AND_TORQUE_DRIVEN`.

Please note that using show_meshes=True in the animator may be long due to the creation of a huge `CasADi` graph of the
mesh points.

## Muscle driven with contact
All the examples in muscle_driven_with_contact are merely to show some dynamics and prepare some OCP for the tests.
It is not really relevant and will be removed when unitary tests for the dynamics will be implemented.

### The contact_forces_inequality_constraint_muscle.py file
In this example, we implement inequality constraints on two contact forces. It is designed to show how to use min_bound 
and max_bound values so they define inequality constraints instead of equality constraints, which can be used with 
any ConstraintFcn.

In this case, the dynamics function used is `DynamicsFcn.MUSCLE_ACTIVATIONS_AND_TORQUE_DRIVEN_WITH_CONTACT`.

### The contact_forces_inequality_constraint_muscle_excitations.py file
In this example, we implement inequality constraints on two contact forces. It is designed to show how to use `min_bound` 
and `max_bound` values so they define inequality constraints instead of equality constraints, which can be used with any 
`ConstraintFcn`.

In this case, the dynamics function used is `DynamicsFcn.MUSCLE_EXCITATIONS_AND_TORQUE_DRIVEN_WITH_CONTACT` instead of 
`DynamicsFcn.MUSCLE_ACTIVATIONS_AND_TORQUE_DRIVEN_WITH_CONTACT` used in the precedent example. 

### The muscle_activations_contacts_tracker.py file 
In this example, we track both muscle controls and contact forces, as it is defined when adding the two objective 
functions below, using both `ObjectiveFcn.Lagrange.TRACK_MUSCLES_CONTROL` and 
`ObjectiveFcn.Lagrange.TRACK_CONTACT_FORCES` objective functions. 

```python
objective_functions = ObjectiveList()
objective_functions.add(ObjectiveFcn.Lagrange.TRACK_MUSCLES_CONTROL, target=muscle_activations_ref)
objective_functions.add(ObjectiveFcn.Lagrange.TRACK_CONTACT_FORCES, target=contact_forces_ref)
```

Let's take a look at the structure of this example. First, we load data to track, and we generate data using the 
`data_to_track.prepare_ocp` optimization control program. Then, we track these data using `muscle_activation_ref` and 
`contact_forces_ref` as shown below:

```python
ocp = prepare_ocp(
    biorbd_model_path=model_path,
    phase_time=final_time,
    n_shooting=ns,
    muscle_activations_ref=muscle_activations_ref[:, :-1],
    contact_forces_ref=contact_forces_ref,
)
```

## Optimal time OCP
In this section, you will find four examples showing how to play with time parameters.  

### The multiphase_time_constraint.py file
This example is a trivial multiphase box that must superimpose different markers at beginning and end of each
phase with one of its corner. The time is free for each phase.
It is designed to show how one can define a multi-phase ocp problem with free time. 

In this example, the number of phases is 1 or 3. prepare_ocp function takes `time_min`, `time_max` and `final_time` as 
arguments. There are arrays of length 3 in the case of a 3-phase problem. In the example, these arguments are defined 
as shown below:

```python
final_time = [2, 5, 4]
time_min = [1, 3, 0.1]
time_max = [2, 4, 0.8]
ns = [20, 30, 20]
ocp = prepare_ocp(final_time=final_time, time_min=time_min, time_max=time_max, n_shooting=ns)
```

We can make out different time constraints for each phase, as shown in the code below:

```python
constraints.add(ConstraintFcn.TIME_CONSTRAINT, node=Node.END, min_bound=time_min[0], max_bound=time_max[0], phase=0)
if n_phases == 3:
    constraints.add(
        ConstraintFcn.TIME_CONSTRAINT, node=Node.END, min_bound=time_min[1], max_bound=time_max[1], phase=1
    )
    constraints.add(
        ConstraintFcn.TIME_CONSTRAINT, node=Node.END, min_bound=time_min[2], max_bound=time_max[2], phase=2
    )
```

### The pendulum_min_time_Lagrange.py file
This is a clone of the example/getting_started/pendulum.py where a pendulum must be balance. The difference is that
the time to perform the task is now free and minimized by the solver, as shown in the definition of the objective 
function used for this example:

```python
objective_functions = ObjectiveList()
objective_functions.add(ObjectiveFcn.Lagrange.MINIMIZE_TIME, weight=1)
```

Please note that a weight of -1 will maximize time. 

This example shows how to define such an optimal
control program with a Lagrange criteria (integral of dt).

The difference between Mayer and Lagrange minimization time is that the former can define bounds to
the values, while the latter is the most common way to define optimal time. 

### The pendulum_min_time_Mayer.py file
This is a clone of the example/getting_started/pendulum.py where a pendulum must be balance. The difference is that
the time to perform the task is now free and minimized by the solver, as shown in the definition of the objective 
function used for this example: 

```python
objective_functions = ObjectiveList()
objective_functions.add(ObjectiveFcn.Mayer.MINIMIZE_TIME, weight=weight, min_bound=min_time, max_bound=max_time)
```

Please note that a weight of -1 will maximize time. 

This example shows how to define such an optimal
control program with a Mayer criteria (value of `final_time`).

The difference between Mayer and Lagrange minimization time is that the former can define bounds to
the values, while the latter is the most common way to define optimal time.

### The time_constraint.py file
This is a clone of the example/getting_started/pendulum.py where a pendulum must be balance. The difference is that
the time to perform the task is now free for the solver to change. This example shows how to define such an optimal
control program. 

In this example, a time constraint is implemented:

```python
constraints = Constraint(ConstraintFcn.TIME_CONSTRAINT, node=Node.END, min_bound=time_min, max_bound=time_max)
```

## Symmetrical torque driven OCP
In this section, you will find an example using symmetry by constraint and another using symmetry by mapping. In both 
cases, we simulate two rodes. We must superimpose a marker on one rod at the beginning and another marker on the
same rod at the end, while keeping the degrees of freedom opposed. 

The difference between the first example (symmetry_by_mapping) and the second one (symmetry_by_constraint) is that one 
(mapping) removes the degree of freedom from the solver, while the other (constraints) imposes a proportional 
constraint (equals to -1) so they are opposed.
Please note that even though removing a degree of freedom seems a good idea, it is unclear if it is actually faster when
solving with `IPOPT`.

### The symmetry_by_constraint.py file
This example imposes a proportional constraint (equals to -1) so that the rotation around the x axis remains opposed 
for the two rodes during the movement. 

Let's take a look at the definition of such a constraint:

```python
constraints.add(ConstraintFcn.PROPORTIONAL_STATE, node=Node.ALL, first_dof=2, second_dof=3, coef=-1)
```

In this case, a proportional constraint is generated between the third degree of freedom defined in the `bioMod` file 
(`first_dof=2`) and the fourth one (`second_dof=3`). Looking at the cubeSym.bioMod file used in this example, we can make 
out that the dof with index 2 corresponds to the rotation around the x axis for the first segment `Seg1`. The dof 
with index 3 corresponds to the rotation around the x axis for the second segment `Seg2`. 

### The symmetry_by_mapping.py file
This example imposes the symmetry as a mapping, that is by completely removing the degree of freedom from the solver 
variables but interpreting the numbers properly when computing the dynamics.

A `BiMapping` is used. The way to understand the mapping is that if one is provided with two vectors, what
would be the correspondence between those vector. For instance, `BiMapping([None, 0, 1, 2, -2], [0, 1, 2])`
would mean that the first vector (v1) has 3 components and to create it from the second vector (v2), you would do:
v1 = [v2[0], v2[1], v2[2]]. Conversely, the second v2 has 5 components and is created from the vector v1 using:
v2 = [0, v1[0], v1[1], v1[2], -v1[2]]. For the dynamics, it is assumed that v1 is what is to be sent to the dynamic
functions (the full vector with all the degrees of freedom), while v2 is the one sent to the solver (the one with less
degrees of freedom).

The `BiMapping` used is defined as a problem parameter, as shown below:

```python
all_generalized_mapping = BiMapping([0, 1, 2, -2], [0, 1, 2])
```

## Torque driven OCP
In this section, you will find different examples showing how to implement torque driven optimal control programs.

### The maximize_predicted_height_CoM.py file
This example mimics by essence what a jumper does which is maximizing the predicted height of the
center of mass at the peak of an aerial phase. It does so with a very simple two segments model though.
It is designed to give a sense of the goal of the different MINIMIZE_COM functions and the use of
`weight=-1` to maximize instead of minimizing.

Let's take a look at the definition of the objetive functions used for this example to better understand how to 
implement that:

```python
objective_functions = ObjectiveList()
if objective_name == "MINIMIZE_PREDICTED_COM_HEIGHT":
    objective_functions.add(ObjectiveFcn.Mayer.MINIMIZE_PREDICTED_COM_HEIGHT, weight=-1)
elif objective_name == "MINIMIZE_COM_POSITION":
    objective_functions.add(ObjectiveFcn.Lagrange.MINIMIZE_COM_POSITION, axis=Axis.Z, weight=-1)
elif objective_name == "MINIMIZE_COM_VELOCITY":
    objective_functions.add(ObjectiveFcn.Lagrange.MINIMIZE_COM_VELOCITY, axis=Axis.Z, weight=-1)
```

Another interesting point of this example is the definition of the constraints. Thanks to the `com_constraints` boolean, 
the user can easily choose to apply constraints on the center of mass. Here is the definition of the constraints for our 
example:

```python
constraints = ConstraintList()
if com_constraints:
    constraints.add(
        ConstraintFcn.TRACK_COM_VELOCITY,
        node=Node.ALL,
        min_bound=np.array([-100, -100, -100]),
        max_bound=np.array([100, 100, 100]),
    )
    constraints.add(
        ConstraintFcn.TRACK_COM_POSITION,
        node=Node.ALL,
        min_bound=np.array([-1, -1, -1]),
        max_bound=np.array([1, 1, 1]),
    )
```

This example is designed to show how to use `min_bound` and `max_bound` values so they define inequality constraints 
instead of equality constraints, which can be used with any `ConstraintFcn`. This example is closed to the 
example_inequality_constraint.py file you can find in 'examples/getting_started/example_inequality_constraint.py'.

### The spring_load.py file 
This trivial spring example targets to have the highest upward velocity. It is however only able to load a spring by
pulling downward and afterward to let it go so it gains velocity. It is designed to show how one can use the external
forces to interact with the body.

This example is closed to the custom_dynamics.py file you can find in 'examples/getting_started/custom_dynamics.py'. 
Indeed, we generate an external force thanks to the custom_dynamic function. Then, we configure the dynamics with 
the `custom_configure` function. 

### The track_markers_2D_pendulum.py file

This example uses the data from the balanced pendulum example to generate the data to track.
When it optimizes the program, contrary to the vanilla pendulum, it tracks the values instead of 'knowing' that
it is supposed to balance the pendulum. It is designed to show how to track marker and kinematic data.

Note that the final node is not tracked. 

In this example, we use both `ObjectiveFcn.Lagrange.TRACK_MARKERS` and `ObjectiveFcn.Lagrange.TRACK_TORQUE` objective 
functions to track data, as shown in the definition of the objective functions used in this example:

```python
objective_functions = ObjectiveList()
objective_functions.add(
    ObjectiveFcn.Lagrange.TRACK_MARKERS, axis_to_track=[Axis.Y, Axis.Z], weight=100, target=markers_ref
)
objective_functions.add(ObjectiveFcn.Lagrange.TRACK_TORQUE, target=tau_ref)
```

This is a good example of how to load data for tracking tasks, and how to plot data. The extra parameter 
`axis_to_track` allows users to specify the axes on which to track the markers (x and y axes in this example).
This example is closed to the example_save_and_load.py and custom_plotting.py files you can find in the 
examples/getting_started repository. 

### The track_markers_with_torque_actuators.py file

This example is a trivial box that must superimpose one of its corner to a marker at the beginning of the movement
and superimpose the same corner to a different marker at the end. It is a clone of
'getting_started/custom_constraint.py' 

It is designed to show how to use the `TORQUE_ACTIVATIONS_DRIVEN` which limits
the torque to [-1; 1]. This is useful when the maximal torque are not constant. Please note that this dynamic then
to not converge when it is used on more complicated model. A solution that defines non-constant constraints seems a
better idea. An example of which can be found with the `bioptim` paper.

Let's take a look at the structure of the code. First, tau_min, tau_max and tau_init are respectively initialized 
to -1, 1 and 0 if the integer `actuator_type` (which is a parameter of the `prepare_ocp` function) equals to 1. 
In this particular case, the dynamics function used is `DynamicsFcn.TORQUE_ACTIVATIONS_DRIVEN`. 

### The trampo_quaternions.py file

This example uses a representation of a human body by a trunk_leg segment and two arms.
It is designed to show how to use a model that has quaternions in their degrees of freedom.

## Track
In this section, you will find the description of two tracking examples. 

### The track_marker_on_segment.py file
This example is a trivial example where a stick must keep a corner of a box in line for the whole duration of the
movement. The initial and final position of the box are dictated, the rest is fully optimized. It is designed
to show how one can use the tracking function to track a marker with a body segment.

In this case, we use the `ConstraintFcn.TRACK_MARKER_WITH_SEGMENT_AXIS` constraint function, as shown below in the 
definition of the constraints of the problem:

```python
constraints = ConstraintList()
constraints.add(
ConstraintFcn.TRACK_MARKER_WITH_SEGMENT_AXIS, node=Node.ALL, marker_idx=1, segment_idx=2, axis=Axis.X
)
```

Here, we minimize the distance between the marker with index 1 ans the x axis of the segment with index 2. We align 
the axis toward the marker. 

### The track_segment_on_rt.py file
This example is a trivial example where a stick must keep its coordinate system of axes aligned with the one
from a box during the whole duration of the movement. The initial and final position of the box are dictated,
the rest is fully optimized. It is designed to show how one can use the tracking RT function to track
any RT (for instance Inertial Measurement Unit [IMU]) with a body segment.

To implement this tracking task, we use the `ConstraintFcn.TRACK_SEGMENT_WITH_CUSTOM_RT` constraint function, which 
minimizes the distance between a segment and an RT. The extra parameters `segment_idx: int` and `rt_idx: int` must be 
passed to the Objective constructor.

## Moving estimation horizon
In this section, we perform mhe on the pendulum example.

### The mhe.py file
In this example, mhe (Moving Horizon Estimation) is applied on a simple pendulum simulation. Data are generated (states,
controls, and marker trajectories) to simulate the movement of a pendulum, using `scipy.integrate.solve_ivp`. These data
are used to perform mhe.

In this example, 500 shooting nodes are defined. As the size of the mhe window is 10, 490 iterations are performed to
solve the complete problem.

For each iteration, the new marker trajectory is taken into account so that a real time data acquisition is simulated.
For each iteration, the list of objectives is updated, the problem is solved with the new frame added to the window,
the oldest frame is discarded with the `warm_start_mhe function`, and it is saved. The results are plotted so that
estimated data can be compared to real data. 

## Acados
In this section, you will find three examples to investigate `bioptim` using `acados`. 

### The cube.py file
This is a basic example of a cube which have to reach a target at the end of the movement, starting from an initial 
position, and minimizing states and torques. This problem is solved using `acados`. 

### The pendulum.py file 
A very simple yet meaningful optimal control program consisting in a pendulum starting downward and ending upward
while requiring the minimum of generalized forces. The solver is only allowed to move the pendulum sideways.

This simple example is a good place to start investigating `bioptim` using `acados` as it describes the most common
dynamics out there (the joint torque driven), it defines an objective function and some boundaries and initial guesses.

### The static_arm.py file
This is a basic example on how to use biorbd model driven by muscle to perform an optimal reaching task.
The arm must reach a marker while minimizing the muscles activity and the states. We solve the problem using both 
`acados` and `ipotpt`.

# Citing
If you use `bioptim`, we would be grateful if you could cite it as follows:
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
