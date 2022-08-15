#!/bin/bash
foo=0
read -p "Do you already have a virtual environment you would like to use (y/n)? If you do not know what is a virtual environment, simply press 'n' " yn
##### if yes, then just activate the venv and install the reqs #####
if [[ "$yn" == "y" ]]; then 
    read -p "What's the name of the virtual environment? " venv
    foo=1   
fi

pip install --upgrade pip #upgrading pip

if [[ "$OSTYPE" == "darwin"* ]]; then # Mac OSX
        if [[ "$foo" -eq 0 ]]; then
            pip3 install virtualenv
            virtualenv mappemg_venv
            venv="mappemg_venv"
        fi
        source $venv/bin/activate
        echo $VIRTUAL_ENV
        echo "--------------------"
        echo "--------------------"
        #install reqs

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

