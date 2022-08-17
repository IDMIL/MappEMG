#!/bin/bash
read -p "Do you already have a virtual environment you would like to use (y/n)? If you do not know what is a virtual environment, simply press 'n' " yn
##### if yes, then just activate the venv and install the reqs #####

if [[ "$yn" == "y" ]]; then 
    read -p "What's the name of the virtual environment? " venv

elif [[ "$yn" == "n" ]]; then
    pip3 install virtualenv
    virtualenv mappemg_venv
    venv="mappemg_venv"
    
fi

pip install --upgrade pip #upgrading pip

if [[ "$OSTYPE" == "darwin"* ]]; then # Mac OSX
    source $venv/bin/activate

elif [[ "$OSTYPE" == "msys" ]]; then
    # Lightweight shell and GNU utilities compiled for Windows (part of MinGW)
    source $venv/Scripts/activate

fi     

pip install -r requirements.txt

python setup.py install

# elif [[ "$OSTYPE" == "cygwin" ]]; then
#         # POSIX compatibility layer and Linux environment emulation for Windows
# elif [[ "$OSTYPE" == "msys" ]]; then
#         # Lightweight shell and GNU utilities compiled for Windows (part of MinGW)
# elif [[ "$OSTYPE" == "win32" ]]; then
#         # I'm not sure this can happen.
# elif [[ "$OSTYPE" == "freebsd"* ]]; then
#         # ...
# else
#         # Unknown.

