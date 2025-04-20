"""
Script to install dependencies for the interview preparation framework.
Supports both pip and conda environments.
"""
import subprocess
import sys
import os
import platform

def is_conda_environment():
    """
    Check if running in a conda environment.
    """
    return os.path.exists(os.path.join(sys.prefix, 'conda-meta'))

def install_dependencies():
    """
    Install the required dependencies.
    """
    # Detect environment
    in_conda = is_conda_environment()
    if in_conda:
        print(f"Detected Conda environment: {sys.prefix}")
    else:
        print("Using standard Python environment")

    print("Installing dependencies for the interview preparation framework...")

    # Check if pip is available
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "--version"])
    except subprocess.CalledProcessError:
        print("Error: pip is not available. Please install pip first.")
        return False

    # Check for Microsoft Visual C++ Build Tools on Windows
    if sys.platform == "win32":
        print("Checking for Microsoft Visual C++ Build Tools...")
        try:
            # Try to import a package that requires C++ compilation
            import numpy
            print("C++ build tools appear to be available.")
        except ImportError:
            try:
                # Try to install a simple package that requires compilation
                subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])
                subprocess.check_call([sys.executable, "-m", "pip", "install", "numpy"])
                print("C++ build tools are available.")
            except subprocess.CalledProcessError:
                print("\nWARNING: Microsoft Visual C++ Build Tools may not be installed.")
                print("Some packages require C++ compilation. If installation fails, please install:")
                print("Microsoft C++ Build Tools: https://visualstudio.microsoft.com/visual-cpp-build-tools/")
                print("During installation, select 'Desktop development with C++'")
                print("After installation, restart your computer and run this script again.\n")
                user_input = input("Do you want to continue with installation anyway? (y/n): ")
                if user_input.lower() != "y":
                    print("Installation aborted.")
                    return False

    # Install dependencies
    try:
        in_conda = is_conda_environment()

        # First, upgrade pip
        print("Upgrading pip...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])

        # Install specific versions of dependencies that might cause conflicts
        print("\nInstalling python-dotenv 1.0.0...")
        if in_conda:
            # Try conda first, fall back to pip if needed
            try:
                subprocess.check_call(["conda", "install", "-y", "python-dotenv=1.0.0"])
            except (subprocess.CalledProcessError, FileNotFoundError):
                print("Falling back to pip for python-dotenv...")
                subprocess.check_call([sys.executable, "-m", "pip", "install", "python-dotenv==1.0.0"])
        else:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "python-dotenv==1.0.0"])

        # Install the rest of the dependencies
        print("\nInstalling remaining dependencies...")
        with open("requirements.txt", "r") as f:
            requirements = f.readlines()

        for req in requirements:
            req = req.strip()
            if req and not req.startswith("python-dotenv") and not req.startswith("langchain-core"):
                print(f"Installing {req}...")
                package_name = req.split("==")[0] if "==" in req else req

                try:
                    if in_conda and package_name not in ["langchain-google-genai"]:
                        # Try conda first for packages that are likely in conda repositories
                        try:
                            conda_req = req.replace("==", "=") if "==" in req else req
                            subprocess.check_call(["conda", "install", "-y", conda_req])
                            print(f"Installed {req} using conda")
                            continue
                        except (subprocess.CalledProcessError, FileNotFoundError):
                            print(f"Conda install failed for {req}, falling back to pip...")

                    # Use pip as fallback or for packages not in conda
                    subprocess.check_call([sys.executable, "-m", "pip", "install", req])
                    print(f"Installed {req} using pip")
                except subprocess.CalledProcessError as e:
                    print(f"Error installing {req}: {e}")
                    if "Microsoft Visual C++" in str(e) or "MSVC" in str(e):
                        print("\nERROR: This package requires Microsoft Visual C++ Build Tools.")
                        print("Please install Microsoft C++ Build Tools from:")
                        print("https://visualstudio.microsoft.com/visual-cpp-build-tools/")
                        print("During installation, select 'Desktop development with C++'")
                        print("After installation, restart your computer and run this script again.")
                        return False
                    else:
                        print("Continuing with other packages...")

        print("\nDependencies installed successfully!")
        print("You can now run the application with: streamlit run app.py")
        return True
    except subprocess.CalledProcessError as e:
        print(f"\nError installing dependencies: {e}")
        if "Microsoft Visual C++" in str(e) or "MSVC" in str(e):
            print("\nERROR: This package requires Microsoft Visual C++ Build Tools.")
            print("Please install Microsoft C++ Build Tools from:")
            print("https://visualstudio.microsoft.com/visual-cpp-build-tools/")
            print("During installation, select 'Desktop development with C++'")
            print("After installation, restart your computer and run this script again.")
        return False

if __name__ == "__main__":
    install_dependencies()
