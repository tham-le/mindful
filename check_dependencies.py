#!/usr/bin/env python3
"""
Check if required Python packages are installed
"""
import sys
import subprocess
import pkg_resources

# List of required packages
required_packages = [
    'flask',
    'flask-cors',
    'sqlalchemy',
    'python-dotenv',
    'flask-jwt-extended',
    'werkzeug',
    'pyjwt'
]

def check_package(package_name):
    """Check if a package is installed"""
    try:
        pkg_resources.get_distribution(package_name)
        return True
    except pkg_resources.DistributionNotFound:
        return False

def main():
    """Main function"""
    print("Checking required Python packages...")
    
    missing_packages = []
    for package in required_packages:
        if not check_package(package):
            missing_packages.append(package)
    
    if missing_packages:
        print("\nThe following packages are missing:")
        for package in missing_packages:
            print(f"  - {package}")
        
        print("\nYou can install them using pip:")
        print(f"  pip install {' '.join(missing_packages)}")
        
        print("\nOr you can run the start.sh script which will set up a virtual environment and install the required packages.")
        return 1
    else:
        print("All required packages are installed!")
        return 0

if __name__ == "__main__":
    sys.exit(main()) 