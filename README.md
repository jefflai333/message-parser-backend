# Message Parser
## More info about the steps can be found at https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/
# Step 0: Download Facebook Data
## Go to Settings -> Your Facebook Information -> Download Your Information
### You can choose what to download, but you have to download Messages in HTML format for this parser to work
# Step 1: Install Python 
Go to https://www.python.org/downloads/ and install the latest version of Python 
# Step 2: Confirm that you have pip
## Windows:
`py -m pip --version`
### Note: if you want to make sure pip is up to date, run:
`py -m pip install --upgrade pip`
## Linux + Mac:
`python3 -m pip --version`
### Note: if you want to make sure pip is installed, run:
`python3 -m pip install --user --upgrade pip`
# Step 3: Install Virtualenv
## Windows:
`py -m pip install --user virtualenv`
## Linux + Mac:
`python3 -m pip install --user virtualenv`
# Step 4: Create a GitHub account (if you don't already have one)
Go to https://github.com/join?source=login to create one
# Step 5: Get this repository locally on your computer
## Option 1: Install GitHub Desktop
Follow instructions at https://docs.github.com/en/desktop/contributing-and-collaborating-using-github-desktop/adding-and-cloning-repositories/cloning-a-repository-from-github-to-github-desktop
## Option 2: Install Git
### Go to the directory you would like to clone the repository at (use cd PATH_NAME) and run
`git clone https://github.com/jefflai333/Message_Parser.git`
# Step 6: Create a virtual environment
## Go to the directory where the repository is located (use cd PATH_NAME) and run:
## Windows:
`py -m venv env`
## Linux + Mac:
`python3 -m venv env`
# Step 7: Activate the virtual environment
## Windows:
`.\env\Scripts\activate`
### To confirm it worked:
`where python
.../env/bin/python.exe`
## Linux + Mac:
`source env/bin/activate`
### To confirm it worked:
`which python
.../env/bin/python`
#### Note: To leave the virtual environemnt, run `deactivate`
# Step 8: Install Dependencies
## Windows:
`py -m pip install -r requirements.txt`
## Linux + Mac:
`python3 -m pip install -r requirements.txt`
# Step 6: Run Script
## Windows:
`py Message_Stats.py --path YOUR_PATH_FOR_FB_DATA_HERE`
## Linux + Mac:
`python3 Message_Stats.py --path YOUR_PATH_FOR_FB_DATA_HERE`
