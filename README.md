#Etcher Explorer vs 0.04
# Etcher Explorer is a computer system's multi-tool. It includes a text editor, compression management, encryption of resting files, a password vault, cpu control, etc.

# IMPORTANT:!! Rename /dir/of/prog to '~/Etcher_Explorerer' !!:IMPORTANT

# Ensure python3.12, python3-pip, pipenv, and setuptools is installed on the system and create the virtual environment:
sudo apt-get install python3-full python3-pip python3-venv 

# Once the virt env is loaded run pip command to install pipenv
pip install pipenv

# Run Setup file
pipenv run python3 setup.py install
# This handles most of the systems configuration.

# Ensure permissions. Replace {filename} with the individual .py filenames in the programs directory:
sudo chmod +x {filename}

