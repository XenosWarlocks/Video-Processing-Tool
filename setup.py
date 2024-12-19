# setup.py
import nltk
import os

def setup_nltk():
    """
    Download required NLTK data
    """
    print("Setting up NLTK data...")
    
    # Create data directory if it doesn't exist
    nltk_data_dir = os.path.join(os.path.expanduser('~'), 'nltk_data')
    if not os.path.exists(nltk_data_dir):
        os.makedirs(nltk_data_dir)
    
    # Required NLTK downloads
    required_packages = [
        'punkt',
        'averaged_perceptron_tagger',
        'wordnet',
        'stopwords'
    ]
    
    for package in required_packages:
        try:
            print(f"Downloading {package}...")
            nltk.download(package, quiet=True)
            print(f"Successfully downloaded {package}")
        except Exception as e:
            print(f"Failed to download {package}: {str(e)}")

if __name__ == "__main__":
    setup_nltk()