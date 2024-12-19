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
        print(Fore.YELLOW + f"Installing missing package: {package_name}...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package_name], stdout=subprocess.DEVNULL)
        print(Fore.GREEN + f"✔ {package_name} installed successfully.\n")


# Ensure required dependencies are installed
required_packages = ["nltk", "tqdm", "colorama"]
for package in required_packages:
    ensure_package_installed(package)

# Import after installation to avoid missing dependencies
import nltk


def install_requirements():
    """
    Install dependencies from requirements.txt, skipping already installed ones.
    """
    print(Back.BLUE + Fore.WHITE + Style.BRIGHT + "\n  Installing Python Dependencies  \n")
    print(Fore.CYAN + "-" * 50 + "\n")

    requirements_file = "requirements.txt"
    if not os.path.exists(requirements_file):
        print(Fore.RED + "✘ requirements.txt not found!\n")
        return

    with open(requirements_file, "r") as file:
        requirements = file.readlines()

    for requirement in tqdm(requirements, desc="Processing requirements", bar_format="{l_bar}{bar:30}{r_bar}", colour="cyan"):
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
                    print(Fore.GREEN + f"✔ Installed: {package}")
                elif "already satisfied" in result.stdout:
                    print(Fore.YELLOW + f"✔ Already installed: {package}")
                else:
                    print(Fore.RED + f"✘ Error installing {package}: {result.stderr.strip()}")
            except Exception as e:
                print(Fore.RED + f"✘ Failed to process {package}: {str(e)}")

    print(Fore.CYAN + "\n" + "-" * 50)
    print(Back.GREEN + Fore.WHITE + Style.BRIGHT + "  Dependency Installation Complete!  ")
    print(Fore.CYAN + "-" * 50 + "\n")


def setup_nltk():
    """
    Download required NLTK data with a visually appealing CLI UI.
    """
    init(autoreset=True)

    print(Back.BLUE + Fore.WHITE + Style.BRIGHT + "\n  Setting Up NLTK Data  \n")
    print(Fore.CYAN + "-" * 50 + "\n")

    # Required NLTK downloads
    required_packages = [
        "punkt",
        "averaged_perceptron_tagger",
        "wordnet",
        "stopwords",
    ]

    # Animated processing of packages
    print(Fore.MAGENTA + "Processing packages...\n")
    time.sleep(0.5)  # Small delay for better UI effect

    for package in required_packages:
        print(Fore.CYAN + f"Checking package: {package}")
        with tqdm(total=100, desc=f"Installing {package}", bar_format="{l_bar}{bar:30}{r_bar}", colour="yellow") as pbar:
            try:
                downloader = nltk.downloader.Downloader()
                if downloader.is_installed(package):
                    pbar.update(100)
                    print(Fore.YELLOW + f"✔ {package} is already installed. Skipping.\n")
                else:
                    nltk.download(package, quiet=True)
                    pbar.update(100)
                    print(Fore.GREEN + f"✔ Successfully downloaded {package}.\n")
            except Exception as e:
                print(Fore.RED + f"✘ Failed to download {package}: {str(e)}\n")

    print(Fore.CYAN + "-" * 50)
    print(Back.GREEN + Fore.WHITE + Style.BRIGHT + "  NLTK Setup Complete!  ")
    print(Fore.CYAN + "-" * 50 + "\n")


if __name__ == "__main__":
    try:
        install_requirements()
        setup_nltk()
    except Exception as e:
        print(Fore.RED + f"✘ Setup failed: {str(e)}")
