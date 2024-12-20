# setup.py
import subprocess
import sys
import os
import time
from tqdm import tqdm
from colorama import Fore, Back, Style, init

def ensure_package_installed(package_name):
    """
    Ensures a package is installed. Installs it if not present.
    """
    try:
        __import__(package_name)
    except ImportError:
        print(Fore.RED + f"✘ Package {package_name} not found. Installing...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])

# Ensure required dependencies are installed
required_packages = ["nltk", "tqdm", "colorama"]
for package in required_packages:
    ensure_package_installed(package)

# Proceed with setup
import nltk
from tqdm import tqdm
from colorama import Fore, Back, Style, init

def install_requirements():
    """
    Install dependencies from requirements.txt with a single progress bar.
    """
    init(autoreset=True)

    print(Back.BLUE + Fore.WHITE + Style.BRIGHT + "\n  Installing Python Dependencies  \n")
    print(Fore.CYAN + Style.BRIGHT + "-" * 50 + "\n")

    requirements_file = "requirements.txt"
    if not os.path.exists(requirements_file):
        print(Fore.RED + "✘ requirements.txt not found!")
        return

    with open(requirements_file, "r") as file:
        requirements = [line.strip() for line in file if line.strip() and not line.startswith("#")]

    with tqdm(total=len(requirements), desc="Installing packages", 
             bar_format="{desc}: {percentage:3.0f}%|{bar:30}| {n_fmt}/{total_fmt}", 
             colour="green", position=0, leave=True) as pbar:
        
        # Use carriage return to overwrite previous line
        print_status = lambda msg: print(f"\033[K{msg}", end="\r")
        
        for requirement in requirements:
            package = requirement.strip()
            if package:
                try:
                    result = subprocess.run(
                        [sys.executable, "-m", "pip", "install", package],
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        text=True,
                    )
                    
                    if result.returncode == 0:
                        print_status(Fore.GREEN + f"✔ Installed: {package}")
                    elif "already satisfied" in result.stdout:
                        print_status(Fore.YELLOW + f"✔ Already installed: {package}")
                    else:
                        print_status(Fore.RED + f"✘ Error installing {package}: {result.stderr.strip()}")
                    
                    pbar.update(1)
                    
                except Exception as e:
                    print_status(Fore.RED + f"✘ Failed to process {package}: {str(e)}")
                    pbar.update(1)

    print("\n" + Fore.CYAN + Style.BRIGHT + "-" * 50)
    print(Back.GREEN + Fore.WHITE + Style.BRIGHT + "  Dependency Installation Complete!  ")
    print(Fore.CYAN + Style.BRIGHT + "-" * 50 + "\n")

def setup_nltk():
    """
    Download required NLTK data with a single progress bar.
    """
    init(autoreset=True)

    print(Back.BLUE + Fore.WHITE + Style.BRIGHT + "\n  Setting Up NLTK Data  \n")
    print(Fore.CYAN + Style.BRIGHT + "-" * 50 + "\n")

    required_packages = [
        'punkt',
        'averaged_perceptron_tagger',
        'wordnet',
        'stopwords'
    ]

    with tqdm(total=len(required_packages), desc="Downloading NLTK packages",
             bar_format="{desc}: {percentage:3.0f}%|{bar:30}| {n_fmt}/{total_fmt}",
             colour="cyan", position=0, leave=True) as pbar:
        
        print_status = lambda msg: print(f"\033[K{msg}", end="\r")
        
        downloader = nltk.downloader.Downloader()
        for package in required_packages:
            print_status(Fore.CYAN + f"Processing: {package}")
            
            if downloader.is_installed(package):
                print_status(Fore.YELLOW + f"✔ {package} is already installed. Skipping.")
            else:
                print_status(Fore.BLUE + f"Downloading {package}...")
                try:
                    nltk.download(package, quiet=True)
                    print_status(Fore.GREEN + f"✔ Successfully downloaded {package}")
                except Exception as e:
                    print_status(Fore.RED + f"✘ Failed to download {package}: {str(e)}")
            
            pbar.update(1)

    print("\n" + Fore.CYAN + Style.BRIGHT + "-" * 50)
    print(Back.GREEN + Fore.WHITE + Style.BRIGHT + "  NLTK Setup Complete!  ")
    print(Fore.CYAN + Style.BRIGHT + "-" * 50 + "\n")

if __name__ == "__main__":
    try:
        install_requirements()
        setup_nltk()
    except Exception as e:
        print(Fore.RED + f"✘ Setup failed: {str(e)}")

# python setup.py