# DataDog Hue

Requires [asdf](https://asdf-vm.com/)

## Setup:

```bash
asdf install # Install Python Version
python -m venv venv # Create a Virtual Env
source ./venv/bin/activate # Activate Virtual Env
pip install -r dev-requirements.txt -r requirements.txt # Install packages
inv update-requirements sync-venv # Update packages to latest and sync updates to the virtual environment
python datadog_hue.py --help
```
