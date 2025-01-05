import os
import subprocess
from setuptools import setup, Command

class CustomInstallCommand(Command):
    description = 'Custom install command to run shell commands and set up the project environment.'
    user_options = []
    def initialize_options(self):
        """Initialize options."""
        self.packages = None
        self.python_packages = None 
    
    def finalize_options(self):
        """Finalize options."""
        self.packages = ['pipenv', 'cpufrequtils', 'isc-dhcp-client', 'ifupdown']
        self.python_packages = ['cryptography', 'py7zr', 'requests', 'PySide6', 'logging']
    
    def create_desktop_entry(self):
        desktop_entry_content = """[Desktop Entry]
        Name=Etcher Explorer
        Exec=cd ~/Etcher_Explorer && pipenv sync && pipenv run python3 base.py
        Icon=~/Etcher_Explorer/icon.ico
        Terminal=False
        """
        desktop_entry_path = os.path.expanduser("~/.local/share/applications/etched.desktop")

        try:
            with open(desktop_entry_path, 'w') as f:
                f.write(desktop_entry_content)
            subprocess.check_call(['ln', '-s', '~/.local/share/applications/etched.desktop', '~/Desktop/etched.desktop'])
            print(f"Desktop entry created at {desktop_entry_path}")
            print("Application created successfully!")
        except Exception as e:
            print(f"Failed to create desktop entry: {e}")
            
    def run(self):
        try:
            # Install system dependencies
            packages = ['pipenv', 'cpufrequtils', 'isc-dhcp-client', 'ifupdown']
            for package in packages:
                command = f'sudo apt-get install {package} -y || true'
                subprocess.check_call(command, shell=True)
    
            # Initialize virtual environment
            subprocess.check_call('pipenv install', shell=True)
    
            # Install Python dependencies
            python_packages = ['cryptography', 'py7zr', 'requests', 'PySide6', 'logging']
            for pkg in python_packages:
                subprocess.check_call(f'pipenv install {pkg}', shell=True)
    
            # Copy the desktop file
            subprocess.check_call('sudo cp ~/Etcher_Explorer/etcher.desktop ~/.local/share/applications/etcher.desktop', shell=True)
    
            # Create symlink
            subprocess.check_call('ln -s ~/.local/share/applications/etcher.desktop ~/Desktop/etcher.desktop', shell=True)
            
        except subprocess.CalledProcessError as e:
            print(f"An error occurred while running command: {e.cmd}")
            exit(1)
    

setup(
    name='EtcherExplorer',
    version='0.1.0',
    packages=['etcher_explorer'],  # Replace with actual package names
    install_requires=[
        'cryptography', 'py7zr', 'requests', 'PySide6', 'logging'
    ],
    cmdclass={
        'install': CustomInstallCommand,
    },
)
