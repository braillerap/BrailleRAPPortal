# BrailleRAPPortal Build Manual


## Prerequisites

 * Python 3.11
 * NodeJs 24.22


## clone the BrailleRAPPortal repo

 ```bash
 git clone --sub-modules https://github.com/braillerap/BrailleRAPPortal.git
 cd BrailleRAPPortal
 ```


## Create a Python virtual environment

 ```bash
 Python -m venv venv
 ```

## Activate the python environment

**On Windows systems**
 ```bash
 ./venv/Scripts/activate.ps1
 ```
**On Linux Systems**
 ```bash
 source ./venv/bin/activate
 ```

## Install python dependencies

 ```bash
 pip install -r requirements.txt
  ```

## Install nodejs dependencies

 ```bash
 npm i
 ```

 ## Update submodule and tell git about the good branch

 ```bash
 cd ./reactapp/DesktopBrailleRAP
 git pull origin main
 cd ../..
 
 cd ./reactapp/AccessBrailleRAP
 git pull origin main
 cd ../..

 cd ./reactapp/OpenStreetTouch
 git pull origin main
 cd ../..
 ```
 ## Build the solution

```bash
 npm run fullbuild
```

## Start the web developpement server

```bash
 npm run tailthon
 or
 python portal.py
```